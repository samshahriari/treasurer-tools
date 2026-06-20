from dataclasses import dataclass, field
from typing import Optional

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

    avsandare: Optional[str] = field(
        default=None,
        metadata={
            "name": "Avsandare",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
            "required": True,
        },
    )
    blankettgemensamt: Optional[str] = field(
        default=None,
        metadata={
            "name": "Blankettgemensamt",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
            "required": True,
        },
    )
    blankett: list[str] = field(
        default_factory=list,
        metadata={
            "name": "Blankett",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
            "min_occurs": 1,
        },
    )
    franvarouppgift: list[str] = field(
        default_factory=list,
        metadata={
            "name": "Franvarouppgift",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
            "min_occurs": 1,
            "sequence": 1,
        },
    )
    omrade: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
