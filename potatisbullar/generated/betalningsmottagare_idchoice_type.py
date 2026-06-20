from dataclasses import dataclass, field
from typing import Optional

from generated.annat_id import AnnatId
from generated.betalningsmottagar_id import BetalningsmottagarId
from generated.fodelsetid import Fodelsetid

__NAMESPACE__ = (
    "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1"
)


@dataclass
class BetalningsmottagareIdchoiceType:
    class Meta:
        name = "BetalningsmottagareIDChoiceType"

    betalningsmottagar_id: Optional[BetalningsmottagarId] = field(
        default=None,
        metadata={
            "name": "BetalningsmottagarId",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
            "required": True,
        },
    )
    fodelsetid: list[Fodelsetid] = field(
        default_factory=list,
        metadata={
            "name": "Fodelsetid",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
            "max_occurs": 2,
        },
    )
    annat_id: list[AnnatId] = field(
        default_factory=list,
        metadata={
            "name": "AnnatId",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
            "max_occurs": 3,
        },
    )
