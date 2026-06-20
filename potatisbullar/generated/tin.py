from dataclasses import dataclass, field

__NAMESPACE__ = (
    "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1"
)


@dataclass
class Tin:
    class Meta:
        name = "TIN"
        namespace = "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1"

    value: str = field(
        default="",
        metadata={
            "required": True,
            "min_length": 1,
            "max_length": 20,
            "pattern": r"[^<>]*[^<>\s][^<>]*",
        },
    )
    faltkod: str = field(
        init=False,
        default="252",
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
