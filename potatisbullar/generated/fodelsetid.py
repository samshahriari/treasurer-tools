from dataclasses import dataclass, field

__NAMESPACE__ = (
    "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1"
)


@dataclass
class Fodelsetid:
    class Meta:
        namespace = "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1"

    value: str = field(
        default="",
        metadata={
            "required": True,
            "min_length": 11,
            "max_length": 11,
            "pattern": r"((((19|20)[0-9][0-9])(((01|03|05|07|08|10|12)(0[1-9]|1[0-9]|2[0-9]|3[0-1]))|((04|06|09|11)(0[1-9]|1[0-9]|2[0-9]|30))|((02)(0[1-9]|1[0-9]|2[0-8]))))|(((19|20)(04|08|12|16|20|24|28|32|36|40|44|48|52|56|60|64|68|72|76|80|84|88|92|96)(0229))|(20000229)))[0-9]{3}",
        },
    )
    faltkod: str = field(
        init=False,
        default="222",
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
