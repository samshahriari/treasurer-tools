from dataclasses import dataclass

from generated.betalningsmottagare_idchoice_type import (
    BetalningsmottagareIdchoiceType,
)

__NAMESPACE__ = (
    "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1"
)


@dataclass
class BetalningsmottagareIdchoice(BetalningsmottagareIdchoiceType):
    class Meta:
        name = "BetalningsmottagareIDChoice"
        namespace = "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1"
