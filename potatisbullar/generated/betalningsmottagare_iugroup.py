from dataclasses import dataclass

from generated.betalningsmottagare_iutype import BetalningsmottagareIutype

__NAMESPACE__ = (
    "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1"
)


@dataclass
class BetalningsmottagareIugroup(BetalningsmottagareIutype):
    class Meta:
        name = "BetalningsmottagareIUGROUP"
        namespace = "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1"
