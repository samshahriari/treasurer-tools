from dataclasses import dataclass, field
from typing import Optional

from generated.ambassadanst_isv_mavtal import AmbassadanstIsvMavtal
from generated.andel_styrelsearvode import AndelStyrelsearvode
from generated.andra_kostnadsers import AndraKostnadsers
from generated.antal_dagar_sjoinkomst import AntalDagarSjoinkomst
from generated.arbetsgivare_iugroup import ArbetsgivareIugroup
from generated.arbetsplatsens_gatuadress import ArbetsplatsensGatuadress
from generated.arbetsplatsens_ort import ArbetsplatsensOrt
from generated.arbetsstallenummer import Arbetsstallenummer
from generated.avdr_prel_skatt import AvdrPrelSkatt
from generated.avdr_skatt_asink import AvdrSkattAsink
from generated.avdr_skatt_sink import AvdrSkattSink
from generated.avdrag_utgift_arbetet import AvdragUtgiftArbetet
from generated.avrakning_avgiftsfri_ers import AvrakningAvgiftsfriErs
from generated.bet_for_drivm_vid_bilforman_ulag_ag import (
    BetForDrivmVidBilformanUlagAg,
)
from generated.betalningsmottagare_iugroup import BetalningsmottagareIugroup
from generated.bilersattning import Bilersattning
from generated.borttag import Borttag
from generated.bostadsforman_ej_smahus_ej_ulag_sa import (
    BostadsformanEjSmahusEjUlagSa,
)
from generated.bostadsforman_ej_smahus_ulag_ag import (
    BostadsformanEjSmahusUlagAg,
)
from generated.bostadsforman_ej_smahus_ulag_ea import (
    BostadsformanEjSmahusUlagEa,
)
from generated.bostadsforman_smahus_ej_ulag_sa import (
    BostadsformanSmahusEjUlagSa,
)
from generated.bostadsforman_smahus_ulag_ag import BostadsformanSmahusUlagAg
from generated.bostadsforman_smahus_ulag_ea import BostadsformanSmahusUlagEa
from generated.drivm_vid_bilforman_ej_ulag_sa import DrivmVidBilformanEjUlagSa
from generated.drivm_vid_bilforman_ulag_ag import DrivmVidBilformanUlagAg
from generated.drivm_vid_bilforman_ulag_ea import DrivmVidBilformanUlagEa
from generated.ej_fast_driftstalle_individ import EjFastDriftstalleIndivid
from generated.ejskatteavdrag_ejbeskattning_sv import (
    EjskatteavdragEjbeskattningSv,
)
from generated.ers_ej_soc_avg_ej_jobbavd import ErsEjSocAvgEjJobbavd
from generated.ers_forman_bostad_mm_sink import ErsFormanBostadMmSink
from generated.ersattnings_belopp1 import ErsattningsBelopp1
from generated.ersattnings_belopp2 import ErsattningsBelopp2
from generated.ersattnings_belopp3 import ErsattningsBelopp3
from generated.ersattnings_belopp4 import ErsattningsBelopp4
from generated.ersattnings_kod1 import ErsattningsKod1
from generated.ersattnings_kod2 import ErsattningsKod2
from generated.ersattnings_kod3 import ErsattningsKod3
from generated.ersattnings_kod4 import ErsattningsKod4
from generated.fartygets_namn import FartygetsNamn
from generated.fartygssignal import Fartygssignal
from generated.forman_har_justerats import FormanHarJusterats
from generated.forman_som_pension_ej_ulag_sa import FormanSomPensionEjUlagSa
from generated.forskarskattenamnden import Forskarskattenamnden
from generated.forsta_anstalld import ForstaAnstalld
from generated.hyresersattning import Hyresersattning
from generated.kontant_ersattning_ej_ulag_sa import KontantErsattningEjUlagSa
from generated.kontant_ersattning_ulag_ag import KontantErsattningUlagAg
from generated.kontant_ersattning_ulag_ea import KontantErsattningUlagEa
from generated.konvention_med import KonventionMed
from generated.landskod_arbetsland import LandskodArbetsland
from generated.lokalanstalld import Lokalanstalld
from generated.narfart_fjarrfart import NarfartFjarrfart
from generated.personaloption import Personaloption
from generated.redovisnings_period import RedovisningsPeriod
from generated.skattebefr_enl_avtal import SkattebefrEnlAvtal
from generated.skattepl_bilforman_ej_ulag_sa import SkatteplBilformanEjUlagSa
from generated.skattepl_bilforman_ulag_ag import SkatteplBilformanUlagAg
from generated.skattepl_bilforman_ulag_ea import SkatteplBilformanUlagEa
from generated.skattepl_ovriga_formaner_ej_ulag_sa import (
    SkatteplOvrigaFormanerEjUlagSa,
)
from generated.skattepl_ovriga_formaner_ulag_ag import (
    SkatteplOvrigaFormanerUlagAg,
)
from generated.skattepl_ovriga_formaner_ulag_ea import (
    SkatteplOvrigaFormanerUlagEa,
)
from generated.specifikationsnummer import Specifikationsnummer
from generated.tjanstepension import Tjanstepension
from generated.traktamente import Traktamente
from generated.underlag_rotarbete import UnderlagRotarbete
from generated.underlag_rutarbete import UnderlagRutarbete
from generated.uppgifts_type import UppgiftsType
from generated.utsand_under_tid import UtsandUnderTid
from generated.vaxa_stod import VaxaStod
from generated.verksamhetens_art import VerksamhetensArt
from generated.vissa_avdrag import VissaAvdrag

__NAMESPACE__ = (
    "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1"
)


@dataclass
class Iutype(UppgiftsType):
    class Meta:
        name = "IUTYPE"

    arbetsgivare_iugroup: Optional[ArbetsgivareIugroup] = field(
        default=None,
        metadata={
            "name": "ArbetsgivareIUGROUP",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
            "required": True,
        },
    )
    betalningsmottagare_iugroup: Optional[BetalningsmottagareIugroup] = field(
        default=None,
        metadata={
            "name": "BetalningsmottagareIUGROUP",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
            "required": True,
        },
    )
    ambassadanst_isv_mavtal: Optional[AmbassadanstIsvMavtal] = field(
        default=None,
        metadata={
            "name": "AmbassadanstISvMAvtal",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    andel_styrelsearvode: Optional[AndelStyrelsearvode] = field(
        default=None,
        metadata={
            "name": "AndelStyrelsearvode",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    andra_kostnadsers: Optional[AndraKostnadsers] = field(
        default=None,
        metadata={
            "name": "AndraKostnadsers",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    antal_dagar_sjoinkomst: Optional[AntalDagarSjoinkomst] = field(
        default=None,
        metadata={
            "name": "AntalDagarSjoinkomst",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    arbetsplatsens_gatuadress: Optional[ArbetsplatsensGatuadress] = field(
        default=None,
        metadata={
            "name": "ArbetsplatsensGatuadress",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    arbetsplatsens_ort: Optional[ArbetsplatsensOrt] = field(
        default=None,
        metadata={
            "name": "ArbetsplatsensOrt",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    arbetsstallenummer: Optional[Arbetsstallenummer] = field(
        default=None,
        metadata={
            "name": "Arbetsstallenummer",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    avdr_prel_skatt: Optional[AvdrPrelSkatt] = field(
        default=None,
        metadata={
            "name": "AvdrPrelSkatt",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    avdr_skatt_asink: Optional[AvdrSkattAsink] = field(
        default=None,
        metadata={
            "name": "AvdrSkattASINK",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    avdr_skatt_sink: Optional[AvdrSkattSink] = field(
        default=None,
        metadata={
            "name": "AvdrSkattSINK",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    avdrag_utgift_arbetet: Optional[AvdragUtgiftArbetet] = field(
        default=None,
        metadata={
            "name": "AvdragUtgiftArbetet",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    avrakning_avgiftsfri_ers: Optional[AvrakningAvgiftsfriErs] = field(
        default=None,
        metadata={
            "name": "AvrakningAvgiftsfriErs",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    bet_for_drivm_vid_bilforman_ulag_ag: Optional[
        BetForDrivmVidBilformanUlagAg
    ] = field(
        default=None,
        metadata={
            "name": "BetForDrivmVidBilformanUlagAG",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    bilersattning: Optional[Bilersattning] = field(
        default=None,
        metadata={
            "name": "Bilersattning",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    borttag: Optional[Borttag] = field(
        default=None,
        metadata={
            "name": "Borttag",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    bostadsforman_ej_smahus_ej_ulag_sa: Optional[
        BostadsformanEjSmahusEjUlagSa
    ] = field(
        default=None,
        metadata={
            "name": "BostadsformanEjSmahusEjUlagSA",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    bostadsforman_ej_smahus_ulag_ag: Optional[BostadsformanEjSmahusUlagAg] = (
        field(
            default=None,
            metadata={
                "name": "BostadsformanEjSmahusUlagAG",
                "type": "Element",
                "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
            },
        )
    )
    bostadsforman_ej_smahus_ulag_ea: Optional[BostadsformanEjSmahusUlagEa] = (
        field(
            default=None,
            metadata={
                "name": "BostadsformanEjSmahusUlagEA",
                "type": "Element",
                "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
            },
        )
    )
    bostadsforman_smahus_ej_ulag_sa: Optional[BostadsformanSmahusEjUlagSa] = (
        field(
            default=None,
            metadata={
                "name": "BostadsformanSmahusEjUlagSA",
                "type": "Element",
                "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
            },
        )
    )
    bostadsforman_smahus_ulag_ag: Optional[BostadsformanSmahusUlagAg] = field(
        default=None,
        metadata={
            "name": "BostadsformanSmahusUlagAG",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    bostadsforman_smahus_ulag_ea: Optional[BostadsformanSmahusUlagEa] = field(
        default=None,
        metadata={
            "name": "BostadsformanSmahusUlagEA",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    drivm_vid_bilforman_ej_ulag_sa: Optional[DrivmVidBilformanEjUlagSa] = (
        field(
            default=None,
            metadata={
                "name": "DrivmVidBilformanEjUlagSA",
                "type": "Element",
                "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
            },
        )
    )
    drivm_vid_bilforman_ulag_ag: Optional[DrivmVidBilformanUlagAg] = field(
        default=None,
        metadata={
            "name": "DrivmVidBilformanUlagAG",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    drivm_vid_bilforman_ulag_ea: Optional[DrivmVidBilformanUlagEa] = field(
        default=None,
        metadata={
            "name": "DrivmVidBilformanUlagEA",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    ej_fast_driftstalle_individ: Optional[EjFastDriftstalleIndivid] = field(
        default=None,
        metadata={
            "name": "EjFastDriftstalleIndivid",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    ejskatteavdrag_ejbeskattning_sv: Optional[
        EjskatteavdragEjbeskattningSv
    ] = field(
        default=None,
        metadata={
            "name": "EjskatteavdragEjbeskattningSv",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    ers_ej_soc_avg_ej_jobbavd: Optional[ErsEjSocAvgEjJobbavd] = field(
        default=None,
        metadata={
            "name": "ErsEjSocAvgEjJobbavd",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    ers_forman_bostad_mm_sink: Optional[ErsFormanBostadMmSink] = field(
        default=None,
        metadata={
            "name": "ErsFormanBostadMmSINK",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    ersattnings_belopp1: Optional[ErsattningsBelopp1] = field(
        default=None,
        metadata={
            "name": "ErsattningsBelopp1",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    ersattnings_belopp2: Optional[ErsattningsBelopp2] = field(
        default=None,
        metadata={
            "name": "ErsattningsBelopp2",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    ersattnings_belopp3: Optional[ErsattningsBelopp3] = field(
        default=None,
        metadata={
            "name": "ErsattningsBelopp3",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    ersattnings_belopp4: Optional[ErsattningsBelopp4] = field(
        default=None,
        metadata={
            "name": "ErsattningsBelopp4",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    ersattnings_kod1: Optional[ErsattningsKod1] = field(
        default=None,
        metadata={
            "name": "ErsattningsKod1",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    ersattnings_kod2: Optional[ErsattningsKod2] = field(
        default=None,
        metadata={
            "name": "ErsattningsKod2",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    ersattnings_kod3: Optional[ErsattningsKod3] = field(
        default=None,
        metadata={
            "name": "ErsattningsKod3",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    ersattnings_kod4: Optional[ErsattningsKod4] = field(
        default=None,
        metadata={
            "name": "ErsattningsKod4",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    fartygets_namn: Optional[FartygetsNamn] = field(
        default=None,
        metadata={
            "name": "FartygetsNamn",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    fartygssignal: Optional[Fartygssignal] = field(
        default=None,
        metadata={
            "name": "Fartygssignal",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    forman_har_justerats: Optional[FormanHarJusterats] = field(
        default=None,
        metadata={
            "name": "FormanHarJusterats",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    forman_som_pension_ej_ulag_sa: Optional[FormanSomPensionEjUlagSa] = field(
        default=None,
        metadata={
            "name": "FormanSomPensionEjUlagSA",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    forskarskattenamnden: Optional[Forskarskattenamnden] = field(
        default=None,
        metadata={
            "name": "Forskarskattenamnden",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    forsta_anstalld: Optional[ForstaAnstalld] = field(
        default=None,
        metadata={
            "name": "ForstaAnstalld",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    hyresersattning: Optional[Hyresersattning] = field(
        default=None,
        metadata={
            "name": "Hyresersattning",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    kontant_ersattning_ej_ulag_sa: Optional[KontantErsattningEjUlagSa] = field(
        default=None,
        metadata={
            "name": "KontantErsattningEjUlagSA",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    kontant_ersattning_ulag_ag: Optional[KontantErsattningUlagAg] = field(
        default=None,
        metadata={
            "name": "KontantErsattningUlagAG",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    kontant_ersattning_ulag_ea: Optional[KontantErsattningUlagEa] = field(
        default=None,
        metadata={
            "name": "KontantErsattningUlagEA",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    konvention_med: Optional[KonventionMed] = field(
        default=None,
        metadata={
            "name": "KonventionMed",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    landskod_arbetsland: Optional[LandskodArbetsland] = field(
        default=None,
        metadata={
            "name": "LandskodArbetsland",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    lokalanstalld: Optional[Lokalanstalld] = field(
        default=None,
        metadata={
            "name": "Lokalanstalld",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    narfart_fjarrfart: Optional[NarfartFjarrfart] = field(
        default=None,
        metadata={
            "name": "NarfartFjarrfart",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    personaloption: Optional[Personaloption] = field(
        default=None,
        metadata={
            "name": "Personaloption",
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
    skattebefr_enl_avtal: Optional[SkattebefrEnlAvtal] = field(
        default=None,
        metadata={
            "name": "SkattebefrEnlAvtal",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    skattepl_bilforman_ej_ulag_sa: Optional[SkatteplBilformanEjUlagSa] = field(
        default=None,
        metadata={
            "name": "SkatteplBilformanEjUlagSA",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    skattepl_bilforman_ulag_ag: Optional[SkatteplBilformanUlagAg] = field(
        default=None,
        metadata={
            "name": "SkatteplBilformanUlagAG",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    skattepl_bilforman_ulag_ea: Optional[SkatteplBilformanUlagEa] = field(
        default=None,
        metadata={
            "name": "SkatteplBilformanUlagEA",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    skattepl_ovriga_formaner_ej_ulag_sa: Optional[
        SkatteplOvrigaFormanerEjUlagSa
    ] = field(
        default=None,
        metadata={
            "name": "SkatteplOvrigaFormanerEjUlagSA",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    skattepl_ovriga_formaner_ulag_ag: Optional[
        SkatteplOvrigaFormanerUlagAg
    ] = field(
        default=None,
        metadata={
            "name": "SkatteplOvrigaFormanerUlagAG",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    skattepl_ovriga_formaner_ulag_ea: Optional[
        SkatteplOvrigaFormanerUlagEa
    ] = field(
        default=None,
        metadata={
            "name": "SkatteplOvrigaFormanerUlagEA",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    specifikationsnummer: Optional[Specifikationsnummer] = field(
        default=None,
        metadata={
            "name": "Specifikationsnummer",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
            "required": True,
        },
    )
    tjanstepension: Optional[Tjanstepension] = field(
        default=None,
        metadata={
            "name": "Tjanstepension",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    traktamente: Optional[Traktamente] = field(
        default=None,
        metadata={
            "name": "Traktamente",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    underlag_rotarbete: Optional[UnderlagRotarbete] = field(
        default=None,
        metadata={
            "name": "UnderlagRotarbete",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    underlag_rutarbete: Optional[UnderlagRutarbete] = field(
        default=None,
        metadata={
            "name": "UnderlagRutarbete",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    utsand_under_tid: Optional[UtsandUnderTid] = field(
        default=None,
        metadata={
            "name": "UtsandUnderTid",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    vaxa_stod: Optional[VaxaStod] = field(
        default=None,
        metadata={
            "name": "VaxaStod",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    verksamhetens_art: Optional[VerksamhetensArt] = field(
        default=None,
        metadata={
            "name": "VerksamhetensArt",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    vissa_avdrag: Optional[VissaAvdrag] = field(
        default=None,
        metadata={
            "name": "VissaAvdrag",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
