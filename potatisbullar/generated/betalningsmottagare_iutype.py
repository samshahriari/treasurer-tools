from dataclasses import dataclass, field
from typing import Optional

from generated.betalningsmottagare_idchoice import BetalningsmottagareIdchoice
from generated.efternamn import Efternamn
from generated.fodelseort import Fodelseort
from generated.fornamn import Fornamn
from generated.fri_adress import FriAdress
from generated.gatuadress import Gatuadress
from generated.gatuadress2 import Gatuadress2
from generated.landskod_fodelseort import LandskodFodelseort
from generated.landskod_medborgare import LandskodMedborgare
from generated.landskod_postort import LandskodPostort
from generated.landskod_tin import LandskodTin
from generated.org_namn import OrgNamn
from generated.postnummer import Postnummer
from generated.postort import Postort
from generated.tin import Tin

__NAMESPACE__ = (
    "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1"
)


@dataclass
class BetalningsmottagareIutype:
    class Meta:
        name = "BetalningsmottagareIUTYPE"

    betalningsmottagare_idchoice: Optional[BetalningsmottagareIdchoice] = (
        field(
            default=None,
            metadata={
                "name": "BetalningsmottagareIDChoice",
                "type": "Element",
                "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
                "required": True,
            },
        )
    )
    efternamn: Optional[Efternamn] = field(
        default=None,
        metadata={
            "name": "Efternamn",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    fodelseort: Optional[Fodelseort] = field(
        default=None,
        metadata={
            "name": "Fodelseort",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    fornamn: Optional[Fornamn] = field(
        default=None,
        metadata={
            "name": "Fornamn",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    fri_adress: Optional[FriAdress] = field(
        default=None,
        metadata={
            "name": "FriAdress",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    gatuadress: Optional[Gatuadress] = field(
        default=None,
        metadata={
            "name": "Gatuadress",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    gatuadress2: Optional[Gatuadress2] = field(
        default=None,
        metadata={
            "name": "Gatuadress2",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    landskod_fodelseort: Optional[LandskodFodelseort] = field(
        default=None,
        metadata={
            "name": "LandskodFodelseort",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    landskod_medborgare: Optional[LandskodMedborgare] = field(
        default=None,
        metadata={
            "name": "LandskodMedborgare",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    landskod_postort: Optional[LandskodPostort] = field(
        default=None,
        metadata={
            "name": "LandskodPostort",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    landskod_tin: Optional[LandskodTin] = field(
        default=None,
        metadata={
            "name": "LandskodTIN",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    org_namn: Optional[OrgNamn] = field(
        default=None,
        metadata={
            "name": "OrgNamn",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    postnummer: Optional[Postnummer] = field(
        default=None,
        metadata={
            "name": "Postnummer",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    postort: Optional[Postort] = field(
        default=None,
        metadata={
            "name": "Postort",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
    tin: Optional[Tin] = field(
        default=None,
        metadata={
            "name": "TIN",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
