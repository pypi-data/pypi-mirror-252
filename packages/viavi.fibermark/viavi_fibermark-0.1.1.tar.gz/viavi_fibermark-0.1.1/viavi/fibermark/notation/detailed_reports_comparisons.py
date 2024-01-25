import re
from dataclasses import asdict
from typing import Optional, Union

import pandas as pd
from sqlalchemy.orm import Session
from type_checker.decorators import enforce_strict_types
from viavi.fiberparse.Data.SORData import NatureEventType

from viavi.fibermark.cli_commands.filtering_helpers import FilterOptions
from viavi.fibermark.db_utils.HelperTypesDB import EventProfFormat, EventTypeDatabase
from viavi.fibermark.db_utils.query_helpers import (
    find_algorithm,
    retrieve_ref_ids_measured_by_algorithm,
)
from viavi.fibermark.notation.algo import mark_algo
from viavi.fibermark.notation.comparison import retrieve_detailed_algo_mark
from viavi.fibermark.notation.helpers import (
    ClassificationResult,
    MetricFilter,
    find_diff_events_two_lists,
)
from viavi.fibermark.notation.measure import classifier_stats_measure
from viavi.fibermark.notation.stats_helpers import AlgoMark
from viavi.fibermark.utils.logging import logger


def extract_version_number(algorithm_name: str) -> Optional[str]:
    match = re.search(" \d{2}.\d{2}", algorithm_name)
    if match:
        ver_number = match.group()
        return ver_number
    else:
        logger.warning(
            f"Could not extract version_number from {algorithm_name}, maybe that is normal because you are not"
            " evaluating a FO version, but please check"
        )
        return None


def make_dataframe_report_from_algo_mark(algo_mark: AlgoMark, algorithm_name: str) -> pd.DataFrame:
    dict_algo_mark = asdict(algo_mark.detailed_mark)
    dict_algo_mark.pop("metric_filter")
    dict_algo_mark.update({"Curve not measured": algo_mark.indexes_curves_not_measured_by_alg})
    df_stats_summary = pd.DataFrame.from_dict(dict_algo_mark, orient="index", columns=[f"stats_{algorithm_name}"])
    return df_stats_summary


def detailed_algo_comparison_to_ref(
    session: Session, alg: str, metric_filter: MetricFilter, filter_options: Optional[FilterOptions] = None
) -> None:
    df_comparison = pd.DataFrame(
        columns=[
            "ref-id",
            "classification result",
            "event_type",
            "pos_meters",
            "index_deb",
            "loss",
            "refl",
        ]
    )
    algo_mark = retrieve_detailed_algo_mark(session, alg, metric_filter)
    algorithm_name = find_algorithm(session, alg).name
    logger.info(f"Making detailed comparison to ref for all references in {algorithm_name}")
    if filter_options is None:
        filter_options = FilterOptions(
            [], ["Non-Regression"], []
        )  # Default filter is all pulses, Non-Regression curves
    else:
        logger.info(f"filter for evaluation is {filter_options}")
    reference_ids = retrieve_ref_ids_measured_by_algorithm(session, alg, filter_options)
    for ref_id in reference_ids:
        try:
            logger.info(f"Inspecting reference {ref_id}")
            classification_per_event_type = classifier_stats_measure(session, ref_id, alg, metric_filter)
            for event_type, classification_event_type_measure in classification_per_event_type.items():
                well_found_events, missed_events, not_existing_events_found = classification_event_type_measure
                if len(missed_events) > 0:
                    logger.info(
                        f"For event_type {event_type.name}, missed {len(missed_events)} elems which are {missed_events}"
                    )
                if len(not_existing_events_found) > 0:
                    logger.info(
                        f"For event_type {event_type.name}, Found {len(not_existing_events_found)} that does not exist"
                        f" which are {not_existing_events_found}"
                    )
                for false_neg_event in sorted(missed_events, key=lambda event: event.pos_meters):
                    df_comparison.loc[len(df_comparison)] = {
                        "ref-id": ref_id,
                        "classification_result": ClassificationResult.FN.name,
                    } | false_neg_event.important_info(type(event_type))
                for false_pos_event in sorted(not_existing_events_found, key=lambda event: event.pos_meters):
                    df_comparison.loc[len(df_comparison)] = {
                        "ref-id": ref_id,
                        "classification_result": ClassificationResult.FP.name,
                    } | false_pos_event.important_info(type(event_type))
        except Exception as e:
            logger.fatal(f"For --ref-id {ref_id} does not exist for algorithm, cannot compare due to {e}")
        continue
    excel_filename = f"{algorithm_name} comparison to reference.xlsx"
    with pd.ExcelWriter(excel_filename, engine="xlsxwriter") as writer:
        df_stats_summary = make_dataframe_report_from_algo_mark(algo_mark, algorithm_name)
        algo_version = extract_version_number(algorithm_name)
        if algo_version is not None:
            sheet_name = f"Stats_Summary_{extract_version_number(algorithm_name)}"
        else:
            sheet_name = "Stats_Summary"  # Preventing size of sheet name problems
        df_stats_summary.to_excel(writer, sheet_name=sheet_name)
        df_comparison.to_excel(writer, sheet_name="Detailed_Info")
    logger.info(f"Report has been registered at {excel_filename}")


@enforce_strict_types
def populate_report_df_diff_between_algs(
    df_comparison_alg_2_not_in_alg_1: pd.DataFrame,
    ref_id: int,
    event_type: Union[EventTypeDatabase, NatureEventType],
    events_missed_by_alg_2_not_by_alg_1: set[EventProfFormat],
    events_found_by_alg_2_not_by_alg_1: set[EventProfFormat],
    not_existing_events_found_by_alg_2_not_by_alg_1: list[EventProfFormat],
    alg_1_name: str,
    alg_2_name: str,
) -> pd.DataFrame:
    if len(events_missed_by_alg_2_not_by_alg_1) > 0:
        logger.warning(
            f"For event_type {event_type.name}, {events_missed_by_alg_2_not_by_alg_1} were missed by"
            f" {alg_2_name} and not by {alg_1_name}"
        )
        for false_neg_event in sorted(
            events_missed_by_alg_2_not_by_alg_1,
            key=lambda event: event.pos_meters,
        ):
            df_comparison_alg_2_not_in_alg_1.loc[len(df_comparison_alg_2_not_in_alg_1)] = {
                "ref-id": ref_id,
                f"classification result in {alg_2_name} not in {alg_1_name}": ClassificationResult.FN.name,
            } | false_neg_event.important_info(type(event_type))
    if len(events_found_by_alg_2_not_by_alg_1) > 0:
        logger.warning(
            f"For event_type {event_type.name}, {events_found_by_alg_2_not_by_alg_1} were found by"
            f" {alg_2_name} and not by {alg_1_name}"
        )
        for true_pos_event in sorted(events_found_by_alg_2_not_by_alg_1, key=lambda event: event.pos_meters):
            df_comparison_alg_2_not_in_alg_1.loc[len(df_comparison_alg_2_not_in_alg_1)] = {
                "ref-id": ref_id,
                f"classification result in {alg_2_name} not in {alg_1_name}": ClassificationResult.TP.name,
            } | true_pos_event.important_info(type(event_type))
    if len(not_existing_events_found_by_alg_2_not_by_alg_1) > 0:
        logger.warning(
            f"For event_type {event_type.name}, Events that do not exist :"
            f" {not_existing_events_found_by_alg_2_not_by_alg_1} were found by  {alg_2_name} and not"
            f" by {alg_1_name}"
        )
        for false_pos_event in sorted(
            not_existing_events_found_by_alg_2_not_by_alg_1, key=lambda event: event.pos_meters
        ):
            df_comparison_alg_2_not_in_alg_1.loc[len(df_comparison_alg_2_not_in_alg_1)] = {
                "ref-id": ref_id,
                f"classification result in {alg_2_name} not in {alg_1_name}": ClassificationResult.FP.name,
            } | false_pos_event.important_info(type(event_type))

    return df_comparison_alg_2_not_in_alg_1


def detailed_algo_comparison(
    session: Session,
    alg_1: str,
    alg_2: str,
    filter_options: Optional[FilterOptions] = None,
    compare_nature_events_only: bool = False,
) -> None:
    algorithm_1_name = find_algorithm(session, alg_1).name
    if filter_options is None:
        filter_options = FilterOptions(
            [], ["Non-Regression"], []
        )  # Default filter is all pulses, Non-Regression curves
    else:
        logger.info(f"filter for evaluation is {filter_options}")
    reference_ids_alg_1 = retrieve_ref_ids_measured_by_algorithm(session, alg_1, filter_options)
    algorithm_2_name = find_algorithm(session, alg_2).name
    reference_ids_alg_2 = retrieve_ref_ids_measured_by_algorithm(session, alg_2, filter_options)
    df_comparison_alg_2_not_in_alg_1 = pd.DataFrame(
        columns=[
            "ref-id",
            f"classification result in {algorithm_2_name} not in {algorithm_1_name}",
            "event_type",
            "pos_meters",
            "index_deb",
            "loss",
            "refl",
        ]
    )
    df_comparison_alg_1_not_in_alg_2 = pd.DataFrame(
        columns=[
            "ref-id",
            f"classification result in {algorithm_1_name} not in {algorithm_2_name}",
            "event_type",
            "pos_meters",
            "index_deb",
            "loss",
            "refl",
        ]
    )
    algo_1_mark = mark_algo(session, alg_1, MetricFilter.All, filter_options)
    algo_2_mark = mark_algo(session, alg_2, MetricFilter.All, filter_options)
    diff_marks = algo_1_mark.detailed_mark - algo_2_mark.detailed_mark
    reference_ids_both_algo_measured = list(set(reference_ids_alg_1) & set(reference_ids_alg_2))
    reference_ids_not_in_both_algo = list(set(reference_ids_alg_1) ^ set(reference_ids_alg_2))
    for ref_id in reference_ids_both_algo_measured:
        try:
            logger.info(f"Inspecting reference {ref_id}")
            classification_per_event_type_alg_1 = classifier_stats_measure(
                session, ref_id, alg_1, MetricFilter.All, compare_nature_events_only
            )
            classification_per_event_type_alg_2 = classifier_stats_measure(
                session, ref_id, alg_2, MetricFilter.All, compare_nature_events_only
            )
            for event_type, alg_1_classification_event_type_measure in classification_per_event_type_alg_1.items():
                alg_1_well_found_events, alg_1_missed_events, alg_1_not_existing_events_found = (
                    alg_1_classification_event_type_measure
                )
                alg_2_well_found_events, alg_2_missed_events, alg_2_not_existing_events_found = (
                    classification_per_event_type_alg_2[event_type]
                )
                events_missed_by_alg_2_not_by_alg_1 = alg_2_missed_events - alg_1_missed_events
                events_missed_by_alg_1_not_by_alg_2 = alg_1_missed_events - alg_2_missed_events
                events_found_by_alg_2_not_by_alg_1 = alg_2_well_found_events - alg_1_well_found_events
                events_found_by_alg_1_not_by_alg_2 = alg_1_well_found_events - alg_2_well_found_events
                not_existing_events_found_by_alg_2_not_by_alg_1 = find_diff_events_two_lists(
                    alg_2_not_existing_events_found, alg_1_not_existing_events_found
                )
                not_existing_events_found_by_alg_1_not_by_alg_2 = find_diff_events_two_lists(
                    alg_1_not_existing_events_found, alg_2_not_existing_events_found
                )
                df_comparison_alg_2_not_in_alg_1 = populate_report_df_diff_between_algs(
                    df_comparison_alg_2_not_in_alg_1,
                    ref_id,
                    event_type,
                    events_missed_by_alg_2_not_by_alg_1,
                    events_found_by_alg_2_not_by_alg_1,
                    not_existing_events_found_by_alg_2_not_by_alg_1,
                    algorithm_1_name,
                    algorithm_2_name,
                )
                df_comparison_alg_1_not_in_alg_2 = populate_report_df_diff_between_algs(
                    df_comparison_alg_1_not_in_alg_2,
                    ref_id,
                    event_type,
                    events_missed_by_alg_1_not_by_alg_2,
                    events_found_by_alg_1_not_by_alg_2,
                    not_existing_events_found_by_alg_1_not_by_alg_2,
                    algorithm_2_name,
                    algorithm_1_name,
                )
        except IndexError:
            logger.fatal(f"Measure/Mark for --ref-id {ref_id} does not exist for both algorithm, cannot compare")
        continue
    logger.warning(
        "Following measures are not in both algorithm measures, thus not took into account for comparison"
        f" {reference_ids_not_in_both_algo}"
    )
    alg_1_version_number = extract_version_number(algorithm_1_name)
    alg_2_version_number = extract_version_number(algorithm_2_name)
    alg_1_unique_ref_ids = set(reference_ids_alg_1)
    alg_2_unique_ref_ids = set(reference_ids_alg_2)
    add_warning_to_report = False
    if len(alg_1_unique_ref_ids - alg_2_unique_ref_ids) != 0 or len(alg_2_unique_ref_ids - alg_1_unique_ref_ids) != 0:
        logger.fatal(
            "Both algorithms do not have the same curves marked, comparison may not make sense \n alg"
            f" {algorithm_1_name} did not measure {alg_2_unique_ref_ids - alg_1_unique_ref_ids}, and alg"
            f" {algorithm_2_name} did not measure {alg_1_unique_ref_ids - alg_2_unique_ref_ids}"
        )
        add_warning_to_report = True
    excel_filename = f"{algorithm_2_name} comparison to {algorithm_1_name}.xlsx"
    with pd.ExcelWriter(excel_filename, engine="xlsxwriter") as writer:
        summary_sheet_name = "Stats_Summary"
        dict_diff_marks = asdict(diff_marks)
        dict_diff_marks.update({"Curve not measured in both algo": reference_ids_not_in_both_algo})
        df_stats_summary = pd.DataFrame.from_dict(
            dict_diff_marks, orient="index", columns=[f"stats_{algorithm_2_name}_minus_{algorithm_1_name}"]
        )
        df_stats_summary.style.to_excel(writer, sheet_name=summary_sheet_name)
        writer.sheets[summary_sheet_name].write(24, 0, "Ref curves used for comparison:")
        writer.sheets[summary_sheet_name].write(24, 1, f"{reference_ids_both_algo_measured}")
        if add_warning_to_report:
            writer.sheets[summary_sheet_name].write(
                25, 1, "Diff Marks is calculated with not measures on the same number of reference ccurve"
            )
        df_stats_summary_alg_1 = make_dataframe_report_from_algo_mark(algo_1_mark, algorithm_1_name)
        df_stats_summary_alg_1.to_excel(writer, sheet_name=summary_sheet_name, startcol=3)
        df_stats_summary_alg_2 = make_dataframe_report_from_algo_mark(algo_2_mark, algorithm_2_name)
        df_stats_summary_alg_2.to_excel(writer, sheet_name=summary_sheet_name, startcol=6)

        if alg_1_version_number is None:
            alg_1_version_number = "alg_1"  # Cannot extract version number
        if alg_2_version_number is None:
            alg_2_version_number = "alg_2"  # Cannot extract version number
        df_comparison_alg_2_not_in_alg_1.to_excel(
            writer, sheet_name=f"Events_FO_{alg_2_version_number}_not_{alg_1_version_number}"
        )
        df_comparison_alg_1_not_in_alg_2.to_excel(
            writer, sheet_name=f"Events_FO_{alg_1_version_number}_not_{alg_2_version_number}"
        )
        logger.info(f"Report has been registered at {excel_filename}")
