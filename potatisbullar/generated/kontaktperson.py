from dataclasses import dataclass, field
from typing import Optional

__NAMESPACE__ = (
    "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1"
)


@dataclass
class Kontaktperson:
    class Meta:
        namespace = "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1"

    namn: Optional[str] = field(
        default=None,
        metadata={
            "name": "Namn",
            "type": "Element",
            "required": True,
            "min_length": 1,
            "max_length": 50,
            "pattern": r"[^<>]*[^<>\s][^<>]*",
        },
    )
    telefon: Optional[str] = field(
        default=None,
        metadata={
            "name": "Telefon",
            "type": "Element",
            "required": True,
            "min_length": 1,
            "max_length": 20,
            "pattern": r"[^<>]*[^<>\s][^<>]*",
        },
    )
    epostadress: Optional[str] = field(
        default=None,
        metadata={
            "name": "Epostadress",
            "type": "Element",
            "required": True,
            "min_length": 5,
            "max_length": 254,
            "pattern": r"[a-zA-Z0-9_]+([-+.'][a-zA-Z0-9_]+)*@[a-zA-Z0-9_]+([-.][a-zA-Z0-9_]+)*\.[a-zA-Z0-9_]+([-.][a-zA-Z0-9_]+)*",
        },
    )
    sakomrade: Optional[str] = field(
        default=None,
        metadata={
            "name": "Sakomrade",
            "type": "Element",
            "min_length": 1,
            "max_length": 50,
            "pattern": r"[^<>]*[^<>\s][^<>]*",
        },
    )
