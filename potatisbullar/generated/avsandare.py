from dataclasses import dataclass, field
from typing import Optional

from xsdata.models.datatype import XmlDateTime

from generated.teknisk_kontaktperson import TekniskKontaktperson

__NAMESPACE__ = (
    "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1"
)


@dataclass
class Avsandare:
    class Meta:
        namespace = "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1"

    programnamn: Optional[str] = field(
        default=None,
        metadata={
            "name": "Programnamn",
            "type": "Element",
            "required": True,
            "min_length": 1,
            "max_length": 50,
            "pattern": r"[^<>]*[^<>\s][^<>]*",
        },
    )
    organisationsnummer: Optional[str] = field(
        default=None,
        metadata={
            "name": "Organisationsnummer",
            "type": "Element",
            "required": True,
            "min_length": 12,
            "max_length": 12,
            "pattern": r"(((19|20)[0-9][0-9])((((01|03|05|07|08|10|12)(6[1-9]|7[0-9]|8[0-9]|9[0-1]))|((04|06|09|11)(6[1-9]|7[0-9]|8[0-9]|90))|((02)(6[1-9]|7[0-9]|8[0-8])))|00[6-9][0-9]|[0-9][0-9]60)|(((19|20)(04|08|12|16|20|24|28|32|36|40|44|48|52|56|60|64|68|72|76|80|84|88|92|96)(0289))|(20000289)))(00[1-9]|0[1-9][0-9]|[1-9][0-9][0-9])[0-9]|16(1[0-9]|2[0-9]|3[0-9]|5[0-9]|6[0-4]|66|68|7[0-9]|8[0-9]|9[0-9])[2-9]\d{7}|((((19|20)[0-9][0-9])(((01|03|05|07|08|10|12)(0[1-9]|1[0-9]|2[0-9]|3[0-1]))|((04|06|09|11)(0[1-9]|1[0-9]|2[0-9]|30))|((02)(0[1-9]|1[0-9]|2[0-8]))))|(((19|20)(04|08|12|16|20|24|28|32|36|40|44|48|52|56|60|64|68|72|76|80|84|88|92|96)(0229))|(20000229)))(00[1-9]|0[1-9][0-9]|[1-9][0-9][0-9])[0-9]",
        },
    )
    teknisk_kontaktperson: Optional[TekniskKontaktperson] = field(
        default=None,
        metadata={
            "name": "TekniskKontaktperson",
            "type": "Element",
            "required": True,
        },
    )
    skapad: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "Skapad",
            "type": "Element",
            "required": True,
        },
    )
