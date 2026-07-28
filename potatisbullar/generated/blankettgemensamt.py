from dataclasses import dataclass, field

from generated.arbetsgivare import Arbetsgivare

__NAMESPACE__ = (
    "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1"
)


@dataclass
class Blankettgemensamt:
    class Meta:
        namespace = "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1"

    arbetsgivare: list[Arbetsgivare] = field(
        default_factory=list,
        metadata={
            "name": "Arbetsgivare",
            "type": "Element",
        },
    )
