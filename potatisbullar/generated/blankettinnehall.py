from dataclasses import dataclass, field
from typing import Optional

from generated.hu import Hu
from generated.iu import Iu

__NAMESPACE__ = (
    "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1"
)


@dataclass
class Blankettinnehall:
    class Meta:
        namespace = "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1"

    hu: Optional[Hu] = field(
        default=None,
        metadata={
            "name": "HU",
            "type": "Element",
        },
    )
    iu: Optional[Iu] = field(
        default=None,
        metadata={
            "name": "IU",
            "type": "Element",
        },
    )
