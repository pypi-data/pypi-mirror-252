from enum import IntEnum
from typing import Optional, Union

from pydantic import BaseModel
from type_checker.decorators import enforce_strict_types
from viavi.fiberparse.Data.MSORData import MultipulseEvent, mapTableIconToLibelleEvt
from viavi.fiberparse.Data.SORData import (
    Event,
    LibelleEvt,
    MethodeMesure,
    NatureEventType,
    TypeMesure,
)


class EventTypeDatabase(IntEnum):
    ProblemEvent = 0
    Reflection = 1
    FiberEnd = 2
    Splice = 3
    Ghost = 4
    Link = 5
    Splitter = 6
    Demux = 7
    Slope = 8
    Splitter_1_2 = 9
    Splitter_1_4 = 10
    Splitter_1_8 = 11
    Splitter_1_16 = 12
    Splitter_1_32 = 13
    Splitter_1_64 = 14
    Splitter_1_128 = 15
    Splitter_2_2 = 16
    Splitter_2_4 = 17
    Splitter_2_8 = 18
    Splitter_2_16 = 19
    Splitter_2_32 = 20
    Splitter_2_64 = 21
    Splitter_2_128 = 22
    EndLink = 23
    Bend = 24
    FiberEndSplitter_2_N = 25
    ConnecteurOTDR = 26
    Orl = 27
    MergedEvent = 28
    FirstMergedEvent = 29
    MediumMergedEvent = 30
    LastMergedEvent = 31
    Coupleur_UB_1_99 = 32
    Coupleur_UB_2_98 = 33
    Coupleur_UB_3_97 = 34
    Coupleur_UB_5_95 = 35
    Coupleur_UB_7_93 = 36
    Coupleur_UB_10_90 = 37
    Coupleur_UB_15_85 = 38
    Coupleur_UB_20_80 = 39
    Coupleur_UB_25_75 = 40
    Coupleur_UB_30_70 = 41
    Coupleur_UB_35_65 = 42
    Coupleur_UB_40_60 = 43
    Coupleur_UB_45_55 = 44
    Coupleur_UB_50_50 = 45
    Cascaded_UB_Coupleur = 46
    Cascaded_Std_Coupleur = 47
    NonMesure = 48


# Database contains 25 event types currently, thus we return None on a LibelleEvt that does not match to any Database element
# Splitter in Database may match different patterns in the sor/xml data.
# flake8: noqa: C901
def maplibelleEvtsxmlSORToEventdatabase(
    libelle_evt: LibelleEvt,
) -> EventTypeDatabase:
    if libelle_evt == LibelleEvt.eEvtLibelle_Reflectance:
        return EventTypeDatabase.Reflection
    elif libelle_evt in [LibelleEvt.eEvtLibelle_FinFibre, LibelleEvt.eEvtLibelle_Connect_Absent]:
        return EventTypeDatabase.FiberEnd
    elif libelle_evt == LibelleEvt.eEvtLibelle_Epissure:
        return EventTypeDatabase.Splice
    elif libelle_evt == LibelleEvt.eEvtLibelle_Fantome:
        return EventTypeDatabase.Ghost
    elif libelle_evt == LibelleEvt.eEvtLibelle_Amorce:
        return EventTypeDatabase.Link
    elif libelle_evt == LibelleEvt.eEvtLibelle_Demux:
        return EventTypeDatabase.Demux
    elif libelle_evt == LibelleEvt.eEvtLibelle_Pent:
        return EventTypeDatabase.Slope
    elif libelle_evt in [
        LibelleEvt.eEvtLibelle_Coupleur,
        LibelleEvt.eEvtLibelle_Coupleur_X_L,
        LibelleEvt.eEvtLibelle_Coupleur_X_N,
        LibelleEvt.eEvtLibelle_Semi_Coupleur_X_N,
        LibelleEvt.eEvtLibelle_Semi_Coupleur_X_L,
        LibelleEvt.eEvtLibelle_Splitter_Absent_N,
        LibelleEvt.eEvtLibelle_Splitter_Uncertain_N,
        LibelleEvt.eEvtLibelle_Splitter_Last_Event,
        LibelleEvt.eEvtLibelle_Splitter_Last_Event_Wrong_Position,
    ]:
        return EventTypeDatabase.Splitter
    elif libelle_evt in [
        LibelleEvt.eEvtLibelle_Coupleur_1_2_L,
        LibelleEvt.eEvtLibelle_Coupleur_1_2_N,
        LibelleEvt.eEvtLibelle_Semi_Coupleur_1_2_L,
        LibelleEvt.eEvtLibelle_Semi_Coupleur_1_2_N,
    ]:
        return EventTypeDatabase.Splitter_1_2
    elif libelle_evt in [
        LibelleEvt.eEvtLibelle_Coupleur_1_4_L,
        LibelleEvt.eEvtLibelle_Coupleur_1_4_N,
        LibelleEvt.eEvtLibelle_Semi_Coupleur_1_4_L,
        LibelleEvt.eEvtLibelle_Semi_Coupleur_1_4_N,
    ]:
        return EventTypeDatabase.Splitter_1_4
    elif libelle_evt in [
        LibelleEvt.eEvtLibelle_Coupleur_1_8_L,
        LibelleEvt.eEvtLibelle_Coupleur_1_8_N,
        LibelleEvt.eEvtLibelle_Semi_Coupleur_1_8_L,
        LibelleEvt.eEvtLibelle_Semi_Coupleur_1_8_N,
    ]:
        return EventTypeDatabase.Splitter_1_8
    elif libelle_evt in [
        LibelleEvt.eEvtLibelle_Coupleur_1_16_L,
        LibelleEvt.eEvtLibelle_Coupleur_1_16_N,
        LibelleEvt.eEvtLibelle_Semi_Coupleur_1_16_L,
        LibelleEvt.eEvtLibelle_Semi_Coupleur_1_16_N,
    ]:
        return EventTypeDatabase.Splitter_1_16
    elif libelle_evt in [
        LibelleEvt.eEvtLibelle_Coupleur_1_32_L,
        LibelleEvt.eEvtLibelle_Coupleur_1_32_N,
        LibelleEvt.eEvtLibelle_Semi_Coupleur_1_32_L,
        LibelleEvt.eEvtLibelle_Semi_Coupleur_1_32_N,
    ]:
        return EventTypeDatabase.Splitter_1_32
    elif libelle_evt in [
        LibelleEvt.eEvtLibelle_Coupleur_1_64_L,
        LibelleEvt.eEvtLibelle_Coupleur_1_64_N,
        LibelleEvt.eEvtLibelle_Semi_Coupleur_1_64_L,
        LibelleEvt.eEvtLibelle_Semi_Coupleur_1_64_N,
    ]:
        return EventTypeDatabase.Splitter_1_64
    elif libelle_evt in [
        LibelleEvt.eEvtLibelle_Coupleur_1_128_L,
        LibelleEvt.eEvtLibelle_Coupleur_1_128_N,
        LibelleEvt.eEvtLibelle_Semi_Coupleur_1_128_L,
        LibelleEvt.eEvtLibelle_Semi_Coupleur_1_128_N,
    ]:
        return EventTypeDatabase.Splitter_1_128
    elif libelle_evt in [
        LibelleEvt.eEvtLibelle_Coupleur_2_2_L,
        LibelleEvt.eEvtLibelle_Coupleur_2_2_N,
        LibelleEvt.eEvtLibelle_Semi_Coupleur_2_2_L,
        LibelleEvt.eEvtLibelle_Semi_Coupleur_2_2_N,
    ]:
        return EventTypeDatabase.Splitter_2_2
    elif libelle_evt in [
        LibelleEvt.eEvtLibelle_Coupleur_2_4_L,
        LibelleEvt.eEvtLibelle_Coupleur_2_4_N,
        LibelleEvt.eEvtLibelle_Semi_Coupleur_2_4_L,
        LibelleEvt.eEvtLibelle_Semi_Coupleur_2_4_N,
    ]:
        return EventTypeDatabase.Splitter_2_4
    elif libelle_evt in [
        LibelleEvt.eEvtLibelle_Coupleur_2_8_L,
        LibelleEvt.eEvtLibelle_Coupleur_2_8_N,
        LibelleEvt.eEvtLibelle_Semi_Coupleur_2_8_L,
        LibelleEvt.eEvtLibelle_Semi_Coupleur_2_8_N,
    ]:
        return EventTypeDatabase.Splitter_2_8
    elif libelle_evt in [
        LibelleEvt.eEvtLibelle_Coupleur_2_16_L,
        LibelleEvt.eEvtLibelle_Coupleur_2_16_N,
        LibelleEvt.eEvtLibelle_Semi_Coupleur_2_16_L,
        LibelleEvt.eEvtLibelle_Semi_Coupleur_2_16_N,
    ]:
        return EventTypeDatabase.Splitter_2_16
    elif libelle_evt in [
        LibelleEvt.eEvtLibelle_Coupleur_2_32_L,
        LibelleEvt.eEvtLibelle_Coupleur_2_32_N,
        LibelleEvt.eEvtLibelle_Semi_Coupleur_2_32_L,
        LibelleEvt.eEvtLibelle_Semi_Coupleur_2_32_N,
    ]:
        return EventTypeDatabase.Splitter_2_32
    elif libelle_evt in [
        LibelleEvt.eEvtLibelle_Coupleur_2_64_L,
        LibelleEvt.eEvtLibelle_Coupleur_2_64_N,
        LibelleEvt.eEvtLibelle_Semi_Coupleur_2_64_L,
        LibelleEvt.eEvtLibelle_Semi_Coupleur_2_64_N,
    ]:
        return EventTypeDatabase.Splitter_2_64
    elif libelle_evt in [
        LibelleEvt.eEvtLibelle_Coupleur_2_128_L,
        LibelleEvt.eEvtLibelle_Coupleur_2_128_N,
        LibelleEvt.eEvtLibelle_Semi_Coupleur_2_128_L,
        LibelleEvt.eEvtLibelle_Semi_Coupleur_2_128_N,
    ]:
        return EventTypeDatabase.Splitter_2_128
    elif libelle_evt == LibelleEvt.eEvtLibelle_Amorce_End:
        return EventTypeDatabase.EndLink
    elif libelle_evt == LibelleEvt.eEvtLibelle_Bend:
        return EventTypeDatabase.Bend
    elif libelle_evt == LibelleEvt.eEvtLibelle_Fin_Fibre_Splitter_2_N:
        return EventTypeDatabase.FiberEndSplitter_2_N
    elif libelle_evt == LibelleEvt.eEvtLibelle_ConnecteurOtdr:
        return EventTypeDatabase.ConnecteurOTDR
    elif libelle_evt == LibelleEvt.eEvtLibelle_Orl:
        return EventTypeDatabase.Orl
    elif libelle_evt == LibelleEvt.eEvtLibelle_Merged_Event:
        return EventTypeDatabase.MergedEvent
    elif libelle_evt == LibelleEvt.eEvtLibelle_First_Merged_Event:
        return EventTypeDatabase.FirstMergedEvent
    elif libelle_evt == LibelleEvt.eEvtLibelle_Medium_Merged_Event:
        return EventTypeDatabase.MediumMergedEvent
    elif libelle_evt == LibelleEvt.eEvtLibelle_Last_Merged_Event:
        return EventTypeDatabase.LastMergedEvent
    elif libelle_evt in [LibelleEvt.eEvtLibelle_Coupleur_UB_L_1_99, LibelleEvt.eEvtLibelle_Coupleur_UB_N_1_99]:
        return EventTypeDatabase.Coupleur_UB_1_99
    elif libelle_evt in [LibelleEvt.eEvtLibelle_Coupleur_UB_L_2_98, LibelleEvt.eEvtLibelle_Coupleur_UB_N_2_98]:
        return EventTypeDatabase.Coupleur_UB_2_98
    elif libelle_evt in [LibelleEvt.eEvtLibelle_Coupleur_UB_L_3_97, LibelleEvt.eEvtLibelle_Coupleur_UB_N_3_97]:
        return EventTypeDatabase.Coupleur_UB_3_97
    elif libelle_evt in [LibelleEvt.eEvtLibelle_Coupleur_UB_L_5_95, LibelleEvt.eEvtLibelle_Coupleur_UB_N_5_95]:
        return EventTypeDatabase.Coupleur_UB_5_95
    elif libelle_evt in [LibelleEvt.eEvtLibelle_Coupleur_UB_L_7_93, LibelleEvt.eEvtLibelle_Coupleur_UB_N_7_93]:
        return EventTypeDatabase.Coupleur_UB_7_93
    elif libelle_evt in [LibelleEvt.eEvtLibelle_Coupleur_UB_L_10_90, LibelleEvt.eEvtLibelle_Coupleur_UB_N_10_90]:
        return EventTypeDatabase.Coupleur_UB_10_90
    elif libelle_evt in [LibelleEvt.eEvtLibelle_Coupleur_UB_L_15_85, LibelleEvt.eEvtLibelle_Coupleur_UB_N_15_85]:
        return EventTypeDatabase.Coupleur_UB_15_85
    elif libelle_evt in [LibelleEvt.eEvtLibelle_Coupleur_UB_L_20_80, LibelleEvt.eEvtLibelle_Coupleur_UB_N_20_80]:
        return EventTypeDatabase.Coupleur_UB_20_80
    elif libelle_evt in [LibelleEvt.eEvtLibelle_Coupleur_UB_L_25_75, LibelleEvt.eEvtLibelle_Coupleur_UB_N_25_75]:
        return EventTypeDatabase.Coupleur_UB_25_75
    elif libelle_evt in [LibelleEvt.eEvtLibelle_Coupleur_UB_L_30_70, LibelleEvt.eEvtLibelle_Coupleur_UB_N_30_70]:
        return EventTypeDatabase.Coupleur_UB_30_70
    elif libelle_evt in [LibelleEvt.eEvtLibelle_Coupleur_UB_L_35_65, LibelleEvt.eEvtLibelle_Coupleur_UB_N_35_65]:
        return EventTypeDatabase.Coupleur_UB_35_65
    elif libelle_evt in [LibelleEvt.eEvtLibelle_Coupleur_UB_L_40_60, LibelleEvt.eEvtLibelle_Coupleur_UB_N_40_60]:
        return EventTypeDatabase.Coupleur_UB_40_60
    elif libelle_evt in [LibelleEvt.eEvtLibelle_Coupleur_UB_L_45_55, LibelleEvt.eEvtLibelle_Coupleur_UB_N_45_55]:
        return EventTypeDatabase.Coupleur_UB_45_55
    elif libelle_evt in [LibelleEvt.eEvtLibelle_Coupleur_UB_L_50_50, LibelleEvt.eEvtLibelle_Coupleur_UB_N_50_50]:
        return EventTypeDatabase.Coupleur_UB_50_50
    elif libelle_evt == LibelleEvt.eEvtLibelle_Cascaded_UB_Coupleur:
        return EventTypeDatabase.Cascaded_UB_Coupleur
    elif libelle_evt in [LibelleEvt.eEvtLibelle_Cascaded_Std_Coupleur_L, LibelleEvt.eEvtLibelle_Cascaded_Std_Coupleur]:
        return EventTypeDatabase.Cascaded_Std_Coupleur
    elif libelle_evt == LibelleEvt.eEvtLibelle_NonMesure:
        return EventTypeDatabase.NonMesure
    else:
        print(f"I don't know how to match to db events {libelle_evt}, please debug me!")
        return EventTypeDatabase(0)


class EventProfFormat(BaseModel, frozen=True):
    db_evt_type: EventTypeDatabase
    index_debut_evt: Optional[int]
    index_fin_evt: Optional[int]
    loss_db: Optional[float]
    reflectance_db: Optional[float]
    bilan_db: Optional[float]
    pos_meters: float
    type_mesure: TypeMesure
    methode_mesure: MethodeMesure
    nature_evt_type_if_sor: Optional[NatureEventType] = None

    def important_info(self, event_type: Union[type[NatureEventType], type[EventTypeDatabase]]):
        if event_type == NatureEventType:
            event_type = self.nature_evt_type_if_sor.name
        elif event_type == EventTypeDatabase:
            event_type = self.db_evt_type.name
        else:
            raise RuntimeError(f"event type {event_type} received and we do not know how to handle")
        return {
            "event_type": event_type,
            "pos_meters": self.pos_meters,
            "index_deb": self.index_debut_evt,
            "loss": self.loss_db,
            "refl": self.reflectance_db,
        }


@enforce_strict_types
def event_to_event_db_event_type(event: Event, resolution_m: float) -> EventProfFormat:
    return EventProfFormat(
        db_evt_type=maplibelleEvtsxmlSORToEventdatabase(event.libelle_evt_type),
        index_debut_evt=event.index_debut_evt,
        index_fin_evt=event.index_fin_evt,
        loss_db=event.loss_db,
        reflectance_db=event.reflectance_db,
        bilan_db=event.bilan_db,
        pos_meters=event.index_debut_evt * resolution_m,
        type_mesure=event.type_mesure,
        methode_mesure=event.methode_mesure,
        nature_evt_type_if_sor=event.nature_evt_type,
    )


@enforce_strict_types
def multipulse_event_to_event_db_event_type(multipulse_event: MultipulseEvent) -> EventProfFormat:
    return EventProfFormat(
        db_evt_type=maplibelleEvtsxmlSORToEventdatabase(mapTableIconToLibelleEvt(multipulse_event.table_icon)),
        index_debut_evt=None,
        index_fin_evt=None,
        loss_db=multipulse_event.loss_db,
        reflectance_db=multipulse_event.reflectance_db,
        bilan_db=multipulse_event.bilan_db,
        pos_meters=multipulse_event.pos_meters,
        type_mesure=TypeMesure.eEvtType_NonApplicable,
        methode_mesure=MethodeMesure.eEvtMethode_NonApplicable,
        nature_evt_type_if_sor=None,  # File is msor
    )
