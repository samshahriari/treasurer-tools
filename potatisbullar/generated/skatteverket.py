from dataclasses import dataclass, field
from typing import Optional

from generated.avsandare import Avsandare
from generated.blankettgemensamt import Blankettgemensamt
from generated.blankett import Blankett
from generated.franvarouppgift import Franvarouppgift
from generated.omrade import Omrade

__NAMESPACE__ = (
    "http://xmls.skatteverket.se/se/skatteverket/da/instans/schema/1.1"
)


@dataclass
class Skatteverket:
    """
    Huvuduppgift, individuppgifter och frånvarouppgifter.
    """

    class Meta:
        namespace = (
            "http://xmls.skatteverket.se/se/skatteverket/da/instans/schema/1.1"
        )

    avsandare: Optional[Avsandare] = field(
        default=None,
        metadata={
            "name": "Avsandare",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
            "required": True,
        },
    )
    blankettgemensamt: Optional[Blankettgemensamt] = field(
        default=None,
        metadata={
            "name": "Blankettgemensamt",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
            "required": True,
        },
    )
    blankett: list[Blankett] = field(
        default_factory=list,
        metadata={
            "name": "Blankett",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
            "min_occurs": 1,
        },
    )
    franvarouppgift: list[Franvarouppgift] = field(
        default_factory=list,
        metadata={
            "name": "Franvarouppgift",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
            "min_occurs": 1,
            "sequence": 1,
        },
    )
    omrade: Optional[Omrade] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
