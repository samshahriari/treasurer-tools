from dataclasses import dataclass, field
from typing import Optional

from generated.ag_registrerad_id import AgRegistreradId
from generated.ej_fast_driftstalle_isv import EjFastDriftstalleIsv

__NAMESPACE__ = (
    "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1"
)


@dataclass
class ArbetsgivareHutype:
    class Meta:
        name = "ArbetsgivareHUTYPE"

    ag_registrerad_id: Optional[AgRegistreradId] = field(
        default=None,
        metadata={
            "name": "AgRegistreradId",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
            "required": True,
        },
    )
    ej_fast_driftstalle_isv: Optional[EjFastDriftstalleIsv] = field(
        default=None,
        metadata={
            "name": "EjFastDriftstalleISv",
            "type": "Element",
            "namespace": "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1",
        },
    )
