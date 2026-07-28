from dataclasses import dataclass, field

__NAMESPACE__ = (
    "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1"
)


@dataclass
class KonventionMed:
    class Meta:
        namespace = "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1"

    value: str = field(
        default="",
        metadata={
            "required": True,
            "min_length": 2,
            "max_length": 2,
            "pattern": r"[1-9][A-Z]",
        },
    )
    faltkod: str = field(
        init=False,
        default="305",
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
