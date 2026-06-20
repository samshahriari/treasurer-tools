from dataclasses import dataclass, field
from typing import Optional

from generated.ag_registrerad_id import AgRegistreradId

__NAMESPACE__ = (
    "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1"
)


@dataclass
class ArbetsgivareIutype:
    class Meta:
        name = "ArbetsgivareIUTYPE"

    ag_registrerad_id: Optional[AgRegistreradId] = field(
        default=None,
        metadata={
            "name": "AgRegistreradId",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
            "required": True,
        },
    )
