from dataclasses import dataclass

from generated.uppgifts_type import UppgiftsType

__NAMESPACE__ = (
    "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1"
)


@dataclass
class Uppgift(UppgiftsType):
    class Meta:
        namespace = "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1"
