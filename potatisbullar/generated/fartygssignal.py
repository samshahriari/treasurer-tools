from dataclasses import dataclass, field

__NAMESPACE__ = (
    "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1"
)


@dataclass
class Fartygssignal:
    class Meta:
        namespace = "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1"

    value: str = field(
        default="",
        metadata={
            "required": True,
            "min_length": 4,
            "max_length": 5,
            "pattern": r"[A-Za-z0-9]+",
        },
    )
    faltkod: str = field(
        init=False,
        default="026",
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
