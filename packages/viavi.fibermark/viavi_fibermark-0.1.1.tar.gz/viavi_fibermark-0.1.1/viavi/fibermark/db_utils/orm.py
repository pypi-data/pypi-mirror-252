from typing import List, cast

from sqlalchemy import CHAR, Column, Date
from sqlalchemy import Float as Float_org
from sqlalchemy import ForeignKey, Index, String, Text, text
from sqlalchemy.dialects.mysql import INTEGER, LONGBLOB, LONGTEXT, SET
from sqlalchemy.orm import DeclarativeBase, Mapped, relationship  # type: ignore
from sqlalchemy.sql.type_api import TypeEngine

Float = cast(type[TypeEngine[float]], Float_org)


class Base(DeclarativeBase):
    pass


class Algorithm(Base):
    __tablename__ = "algorithm"

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(50), unique=True)

    measures: Mapped[List["Measure"]] = relationship("Measure", back_populates="algorithm")
    marks: Mapped[List["AlgorithmMark"]] = relationship("AlgorithmMark", back_populates="algorithm")


class AlgorithmMark(Base):
    __tablename__ = "algorithm_mark"
    __table_args__ = (Index("one_mark_per_metric_and_algorithm", "algorithm_id", "metric_filter", unique=True),)

    id = Column(INTEGER(11), primary_key=True)
    algorithm_id: Column = Column(ForeignKey("algorithm.id", ondelete="CASCADE", onupdate="CASCADE"), index=True)
    metric_filter = Column(SET("Auto", "All"))
    curve_count_for_mark_calculation = Column(INTEGER(11), nullable=False)
    indexes_curves_not_measured_by_alg = Column(Text)
    nb_false_negatives_splice = Column(INTEGER(11))
    nb_false_positives_splice = Column(INTEGER(11))
    nb_true_positives_splice = Column(INTEGER(11))
    nb_false_negatives_reflection = Column(INTEGER(11))
    nb_false_positives_reflection = Column(INTEGER(11))
    nb_true_positives_reflection = Column(INTEGER(11))
    nb_false_negatives_ghost = Column(INTEGER(11))
    nb_false_positives_ghost = Column(INTEGER(11))
    nb_true_positives_ghost = Column(INTEGER(11))
    nb_false_negatives_fiberend = Column(INTEGER(11))
    nb_false_positives_fiberend = Column(INTEGER(11))
    nb_true_positives_fiberend = Column(INTEGER(11))
    nb_false_negatives_splitter = Column(INTEGER(11))
    nb_false_positives_splitter = Column(INTEGER(11))
    nb_true_positives_splitter = Column(INTEGER(11))
    nb_false_negatives_overall = Column(INTEGER(11))
    nb_false_positives_overall = Column(INTEGER(11))
    nb_true_positives_overall = Column(INTEGER(11))
    f_score_splice = Column(Float)
    f_score_reflection = Column(Float)
    f_score_ghost = Column(Float)
    f_score_overall = Column(Float)
    f_score_fiberend = Column(Float)
    f_score_splitter = Column(Float)

    algorithm: Mapped["Algorithm"] = relationship("Algorithm", backref="algorithm_mark", viewonly=True)


class Reference(Base):
    __tablename__ = "reference"

    id = Column(INTEGER(11), primary_key=True)
    path = Column(String(150))
    module = Column(String(255))
    date = Column(Date)
    pulse_ns = Column(INTEGER(11))
    acq_range_km = Column(Float)
    laser = Column(String(11))
    resolution_cm = Column(INTEGER(11))
    acquisition_time_sec = Column(Float, nullable=False)
    n = Column(Float)
    k = Column(Float)
    category = Column(CHAR(50))
    noise_floor_db = Column(Float)
    md5 = Column(CHAR(32), nullable=False, unique=True)

    measure: Mapped["Measure"] = relationship("Measure", backref="reference")


class Measure(Base):
    __tablename__ = "measure"
    __table_args__ = (Index("unique_measure_per_algorithm", "algorithm_id", "reference_id", unique=True),)

    id = Column(INTEGER(11), primary_key=True)
    date = Column(Date)
    algorithm_id: Column = Column(ForeignKey("algorithm.id", ondelete="CASCADE", onupdate="CASCADE"))
    reference_id: Column = Column(
        ForeignKey("reference.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False, index=True
    )

    algorithm: Mapped["Algorithm"] = relationship("Algorithm", backref="measure", viewonly=True)
    events: Mapped[List["Event"]] = relationship("Event", back_populates="measure")
    marks: Mapped[List["Mark"]] = relationship("Mark", back_populates="measure")


class Event(Base):
    __tablename__ = "event"
    __table_args__ = (
        Index(
            "prevent_duplicate_same_event", "index_debut_evt", "measure_id", "event_type", unique=True
        ),  # Need to change that with pos_meters
    )

    id = Column(INTEGER(11), primary_key=True)
    measure_id: Column = Column(ForeignKey("measure.id", ondelete="CASCADE", onupdate="CASCADE"), index=True)
    event_type = Column(
        SET(
            "Reflection",
            "FiberEnd",
            "Splice",
            "Ghost",
            "Link",
            "Splitter",
            "Demux",
            "Slope",
            "Splitter_1_2",
            "Splitter_1_4",
            "Splitter_1_8",
            "Splitter_1_16",
            "Splitter_1_32",
            "Splitter_1_64",
            "Splitter_1_128",
            "Splitter_2_2",
            "Splitter_2_4",
            "Splitter_2_8",
            "Splitter_2_16",
            "Splitter_2_32",
            "Splitter_2_64",
            "Splitter_2_128",
            "EndLink",
            "Bend",
            "FiberEndSplitter_2_N",
            "ConnecteurOTDR",
            "Orl",
            "MergedEvent",
            "FirstMergedEvent",
            "MediumMergedEvent",
            "LastMergedEvent",
            "Coupleur_UB_1_99",
            "Coupleur_UB_2_98",
            "Coupleur_UB_3_97",
            "Coupleur_UB_5_95",
            "Coupleur_UB_7_93",
            "Coupleur_UB_10_90",
            "Coupleur_UB_15_85",
            "Coupleur_UB_20_80",
            "Coupleur_UB_25_75",
            "Coupleur_UB_30_70",
            "Coupleur_UB_35_65",
            "Coupleur_UB_40_60",
            "Coupleur_UB_45_55",
            "Coupleur_UB_50_50",
            "Cascaded_UB_Coupleur",
            "Cascaded_Std_Coupleur",
            "NonMesure",
        )
    )
    loss_db = Column(Float)
    reflectance_db = Column(Float)
    bilan_db = Column(Float)
    index_debut_evt = Column(INTEGER(11))
    pos_debut_evt_meters__calculated_ = Column("pos_debut_evt_meters (calculated)", Float)
    index_fin_evt = Column(INTEGER(11))
    type_mesure = Column(String(255), server_default=text("'eEvtType_NonApplicable'"))
    methode_mesure = Column(String(255), server_default=text("'eEvtMethode_NonApplicable'"))
    nature_evt_type_if_sor = Column(String(255), nullable=True)
    measure: Mapped["Measure"] = relationship("Measure", backref="event", viewonly=True)


class Mark(Base):
    __tablename__ = "mark"

    id = Column(INTEGER(11), primary_key=True)
    measure_id: Column = Column(ForeignKey("measure.id", ondelete="CASCADE", onupdate="CASCADE"), index=True)
    treshold_classification_meters = Column(Float)
    metric_filter = Column(SET("All", "Auto"))

    nb_false_negatives_splice = Column(INTEGER(11))
    nb_false_positives_splice = Column(INTEGER(11))
    nb_true_positives_splice = Column(INTEGER(11))
    nb_false_negatives_reflection = Column(INTEGER(11))
    nb_false_positives_reflection = Column(INTEGER(11))
    nb_true_positives_reflection = Column(INTEGER(11))
    nb_false_negatives_ghost = Column(INTEGER(11))
    nb_false_positives_ghost = Column(INTEGER(11))
    nb_true_positives_ghost = Column(INTEGER(11))
    nb_false_negatives_fiberend = Column(INTEGER(11))
    nb_false_positives_fiberend = Column(INTEGER(11))
    nb_true_positives_fiberend = Column(INTEGER(11))
    nb_false_negatives_splitter = Column(INTEGER(11))
    nb_false_positives_splitter = Column(INTEGER(11))
    nb_true_positives_splitter = Column(INTEGER(11))
    nb_false_negatives_overall = Column(INTEGER(11))
    nb_false_positives_overall = Column(INTEGER(11))
    nb_true_positives_overall = Column(INTEGER(11))

    f_score_splice = Column(Float)
    f_score_reflection = Column(Float)
    f_score_ghost = Column(Float)
    f_score_fiberend = Column(Float)
    f_score_splitter = Column(Float)
    f_score_overall = Column(Float)

    measure: Mapped["Measure"] = relationship("Measure", backref="mark", viewonly=True)


class ParsedSorData(Base):
    __tablename__ = "parsed_sor_data"
    __table_args__ = (Index("parsed_sor_data_pk", "reference_id", "fiberparse_ver", unique=True),)

    id = Column(INTEGER(11), primary_key=True)
    reference_id: Column = Column(ForeignKey("reference.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    fiberparse_ver = Column(CHAR(20))
    serialized_data = Column(LONGTEXT)
    binary_dump = Column(LONGBLOB)
    reference: Mapped["Reference"] = relationship("Reference", backref="parsed_sor_data", viewonly=True)
