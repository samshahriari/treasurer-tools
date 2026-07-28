from dataclasses import dataclass, field
from typing import Optional

from xsdata.models.datatype import XmlDate

__NAMESPACE__ = (
    "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1"
)


@dataclass
class FranvaroDatum:
    class Meta:
        namespace = "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1"

    value: Optional[XmlDate] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    faltkod: str = field(
        init=False,
        default="821",
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
