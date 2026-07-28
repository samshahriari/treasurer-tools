from dataclasses import dataclass, field
from typing import Optional

from generated.annat_driftstod import AnnatDriftstod
from generated.arbetsgivare_hugroup import ArbetsgivareHugroup
from generated.avdrag_fo_u import AvdragFoU
from generated.avdrag_rederi_regress import AvdragRederiRegress
from generated.avdrag_regionalt_stod import AvdragRegionaltStod
from generated.redovisnings_period import RedovisningsPeriod
from generated.skatteavdr_pens_fors import SkatteavdrPensFors
from generated.skatteavdr_ranta_utd import SkatteavdrRantaUtd
from generated.slf_vinstandel_fk486 import SlfVinstandelFk486
from generated.summa_arb_avg_slf import SummaArbAvgSlf
from generated.summa_skatteavdr import SummaSkatteavdr
from generated.total_sjuklonekostnad import TotalSjuklonekostnad
from generated.ulag_fo_u import UlagFoU
from generated.ulag_rederi_regress import UlagRederiRegress
from generated.ulag_regionalt_stod import UlagRegionaltStod
from generated.ulag_skatteavdr_pens_fors import UlagSkatteavdrPensFors
from generated.ulag_skatteavdr_ranta_utd import UlagSkatteavdrRantaUtd
from generated.ulag_slf_vinstandel import UlagSlfVinstandel
from generated.uppgifts_type import UppgiftsType

__NAMESPACE__ = (
    "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1"
)


@dataclass
class Hutype(UppgiftsType):
    class Meta:
        name = "HUTYPE"

    arbetsgivare_hugroup: Optional[ArbetsgivareHugroup] = field(
        default=None,
        metadata={
            "name": "ArbetsgivareHUGROUP",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
            "required": True,
        },
    )
    annat_driftstod: Optional[AnnatDriftstod] = field(
        default=None,
        metadata={
            "name": "AnnatDriftstod",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    avdrag_fo_u: Optional[AvdragFoU] = field(
        default=None,
        metadata={
            "name": "AvdragFoU",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    avdrag_rederi_regress: Optional[AvdragRederiRegress] = field(
        default=None,
        metadata={
            "name": "AvdragRederiRegress",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    avdrag_regionalt_stod: Optional[AvdragRegionaltStod] = field(
        default=None,
        metadata={
            "name": "AvdragRegionaltStod",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    redovisnings_period: Optional[RedovisningsPeriod] = field(
        default=None,
        metadata={
            "name": "RedovisningsPeriod",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
            "required": True,
        },
    )
    skatteavdr_pens_fors: Optional[SkatteavdrPensFors] = field(
        default=None,
        metadata={
            "name": "SkatteavdrPensFors",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    skatteavdr_ranta_utd: Optional[SkatteavdrRantaUtd] = field(
        default=None,
        metadata={
            "name": "SkatteavdrRantaUtd",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    slf_vinstandel_fk486: Optional[SlfVinstandelFk486] = field(
        default=None,
        metadata={
            "name": "SlfVinstandelFK486",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    summa_arb_avg_slf: Optional[SummaArbAvgSlf] = field(
        default=None,
        metadata={
            "name": "SummaArbAvgSlf",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    summa_skatteavdr: Optional[SummaSkatteavdr] = field(
        default=None,
        metadata={
            "name": "SummaSkatteavdr",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    total_sjuklonekostnad: Optional[TotalSjuklonekostnad] = field(
        default=None,
        metadata={
            "name": "TotalSjuklonekostnad",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    ulag_fo_u: Optional[UlagFoU] = field(
        default=None,
        metadata={
            "name": "UlagFoU",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    ulag_rederi_regress: Optional[UlagRederiRegress] = field(
        default=None,
        metadata={
            "name": "UlagRederiRegress",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    ulag_regionalt_stod: Optional[UlagRegionaltStod] = field(
        default=None,
        metadata={
            "name": "UlagRegionaltStod",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    ulag_skatteavdr_pens_fors: Optional[UlagSkatteavdrPensFors] = field(
        default=None,
        metadata={
            "name": "UlagSkatteavdrPensFors",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    ulag_skatteavdr_ranta_utd: Optional[UlagSkatteavdrRantaUtd] = field(
        default=None,
        metadata={
            "name": "UlagSkatteavdrRantaUtd",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    ulag_slf_vinstandel: Optional[UlagSlfVinstandel] = field(
        default=None,
        metadata={
            "name": "UlagSlfVinstandel",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
