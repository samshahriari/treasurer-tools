from dataclasses import dataclass, field

__NAMESPACE__ = (
    "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1"
)


@dataclass
class RedovisningsPeriod:
    class Meta:
        namespace = "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1"

    value: str = field(
        default="",
        metadata={
            "required": True,
            "min_length": 6,
            "max_length": 6,
            "pattern": r"20(18(0[7-9]|1[012])|19(0[1-9]|1[012])|[2-9][0-9](0[1-9]|1[012]))",
        },
    )
    faltkod: str = field(
        init=False,
        default="006",
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
