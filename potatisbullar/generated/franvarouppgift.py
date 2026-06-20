from dataclasses import dataclass, field
from typing import Optional

from generated.ag_registrerad_id import AgRegistreradId
from generated.betalningsmottagar_id import BetalningsmottagarId
from generated.franvaro_borttag import FranvaroBorttag
from generated.franvaro_datum import FranvaroDatum
from generated.franvaro_procent_fp import FranvaroProcentFp
from generated.franvaro_procent_tfp import FranvaroProcentTfp
from generated.franvaro_specifikationsnummer import (
    FranvaroSpecifikationsnummer,
)
from generated.franvaro_timmar_fp import FranvaroTimmarFp
from generated.franvaro_timmar_tfp import FranvaroTimmarTfp
from generated.franvaro_typ import FranvaroTyp
from generated.redovisnings_period import RedovisningsPeriod

__NAMESPACE__ = (
    "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1"
)


@dataclass
class Franvarouppgift:
    class Meta:
        namespace = "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1"

    ag_registrerad_id: Optional[AgRegistreradId] = field(
        default=None,
        metadata={
            "name": "AgRegistreradId",
            "type": "Element",
            "required": True,
        },
    )
    betalningsmottagar_id: Optional[BetalningsmottagarId] = field(
        default=None,
        metadata={
            "name": "BetalningsmottagarId",
            "type": "Element",
            "required": True,
        },
    )
    franvaro_borttag: Optional[FranvaroBorttag] = field(
        default=None,
        metadata={
            "name": "FranvaroBorttag",
            "type": "Element",
        },
    )
    franvaro_datum: Optional[FranvaroDatum] = field(
        default=None,
        metadata={
            "name": "FranvaroDatum",
            "type": "Element",
            "required": True,
        },
    )
    franvaro_procent_fp: Optional[FranvaroProcentFp] = field(
        default=None,
        metadata={
            "name": "FranvaroProcentFP",
            "type": "Element",
        },
    )
    franvaro_procent_tfp: Optional[FranvaroProcentTfp] = field(
        default=None,
        metadata={
            "name": "FranvaroProcentTFP",
            "type": "Element",
        },
    )
    franvaro_specifikationsnummer: Optional[FranvaroSpecifikationsnummer] = (
        field(
            default=None,
            metadata={
                "name": "FranvaroSpecifikationsnummer",
                "type": "Element",
                "required": True,
            },
        )
    )
    franvaro_timmar_fp: Optional[FranvaroTimmarFp] = field(
        default=None,
        metadata={
            "name": "FranvaroTimmarFP",
            "type": "Element",
        },
    )
    franvaro_timmar_tfp: Optional[FranvaroTimmarTfp] = field(
        default=None,
        metadata={
            "name": "FranvaroTimmarTFP",
            "type": "Element",
        },
    )
    franvaro_typ: Optional[FranvaroTyp] = field(
        default=None,
        metadata={
            "name": "FranvaroTyp",
            "type": "Element",
            "required": True,
        },
    )
    redovisnings_period: Optional[RedovisningsPeriod] = field(
        default=None,
        metadata={
            "name": "RedovisningsPeriod",
            "type": "Element",
            "required": True,
        },
    )
