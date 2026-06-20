from dataclasses import dataclass, field
from typing import Optional

__NAMESPACE__ = (
    "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1"
)


@dataclass
class ErsattningsKod3:
    class Meta:
        namespace = "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1"

    value: Optional[int] = field(
        default=None,
        metadata={
            "required": True,
            "min_inclusive": 100,
            "max_inclusive": 999,
        },
    )
    faltkod: str = field(
        init=False,
        default="086",
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
