from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional

__NAMESPACE__ = (
    "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1"
)


@dataclass
class FranvaroProcentTfp:
    class Meta:
        name = "FranvaroProcentTFP"
        namespace = "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1"

    value: Optional[Decimal] = field(
        default=None,
        metadata={
            "required": True,
            "min_inclusive": Decimal("0.01"),
            "max_inclusive": Decimal("100.00"),
            "fraction_digits": 2,
        },
    )
    faltkod: str = field(
        init=False,
        default="824",
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
