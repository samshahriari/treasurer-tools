from dataclasses import dataclass

from generated.arbetsgivare_iutype import ArbetsgivareIutype

__NAMESPACE__ = (
    "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1"
)


@dataclass
class ArbetsgivareIugroup(ArbetsgivareIutype):
    class Meta:
        name = "ArbetsgivareIUGROUP"
        namespace = "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1"
