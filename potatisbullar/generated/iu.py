from dataclasses import dataclass

from generated.iutype import Iutype

__NAMESPACE__ = (
    "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1"
)


@dataclass
class Iu(Iutype):
    class Meta:
        name = "IU"
        namespace = "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1"
