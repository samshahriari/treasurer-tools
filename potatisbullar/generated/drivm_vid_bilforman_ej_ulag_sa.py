from dataclasses import dataclass, field
from typing import Optional

__NAMESPACE__ = (
    "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1"
)


@dataclass
class DrivmVidBilformanEjUlagSa:
    class Meta:
        name = "DrivmVidBilformanEjUlagSA"
        namespace = "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1"

    value: Optional[int] = field(
        default=None,
        metadata={
            "required": True,
            "min_inclusive": 0,
            "max_inclusive": 9999999,
        },
    )
    faltkod: str = field(
        init=False,
        default="134",
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
