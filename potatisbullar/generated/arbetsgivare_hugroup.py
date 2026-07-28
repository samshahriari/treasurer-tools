from dataclasses import dataclass

from generated.arbetsgivare_hutype import ArbetsgivareHutype

__NAMESPACE__ = (
    "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1"
)


@dataclass
class ArbetsgivareHugroup(ArbetsgivareHutype):
    class Meta:
        name = "ArbetsgivareHUGROUP"
        namespace = "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1"
