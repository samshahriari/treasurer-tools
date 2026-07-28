from dataclasses import dataclass

from generated.hutype import Hutype

__NAMESPACE__ = (
    "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1"
)


@dataclass
class Hu(Hutype):
    class Meta:
        name = "HU"
        namespace = "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1"
