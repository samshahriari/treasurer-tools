from dataclasses import dataclass, field

__NAMESPACE__ = (
    "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1"
)


@dataclass
class BostadsformanEjSmahusUlagEa:
    class Meta:
        name = "BostadsformanEjSmahusUlagEA"
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
        default="124",
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
