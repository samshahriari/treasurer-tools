from dataclasses import dataclass, field
from typing import Optional

from generated.arendeinformation import Arendeinformation
from generated.blankettinnehall import Blankettinnehall

__NAMESPACE__ = (
    "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1"
)


@dataclass
class Blankett:
    class Meta:
        namespace = "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1"

    arendeinformation: Optional[Arendeinformation] = field(
        default=None,
        metadata={
            "name": "Arendeinformation",
            "type": "Element",
            "required": True,
        },
    )
    blankettinnehall: Optional[Blankettinnehall] = field(
        default=None,
        metadata={
            "name": "Blankettinnehall",
            "type": "Element",
            "required": True,
        },
    )
