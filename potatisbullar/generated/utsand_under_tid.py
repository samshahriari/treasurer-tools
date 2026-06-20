from dataclasses import dataclass, field

__NAMESPACE__ = (
    "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1"
)


@dataclass
class UtsandUnderTid:
    class Meta:
        namespace = "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1"

    value: str = field(
        default="",
        metadata={
            "required": True,
            "min_length": 1,
            "max_length": 1,
            "pattern": r"[ABC]",
        },
    )
    faltkod: str = field(
        init=False,
        default="091",
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
