from dataclasses import dataclass, field

__NAMESPACE__ = (
    "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1"
)


@dataclass
class VaxaStod:
    class Meta:
        namespace = "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1"

    value: str = field(
        default="",
        metadata={
            "required": True,
            "pattern": r"1|true",
        },
    )
    faltkod: str = field(
        init=False,
        default="063",
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
