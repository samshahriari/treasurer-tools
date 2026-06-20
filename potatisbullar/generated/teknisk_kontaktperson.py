from dataclasses import dataclass, field
from typing import Optional

__NAMESPACE__ = (
    "http://xmls.skatteverket.se/se/skatteverket/da/komponent/schema/1.1"
)


@dataclass
class TekniskKontaktperson:
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
    utdelningsadress1: Optional[str] = field(
        default=None,
        metadata={
            "name": "Utdelningsadress1",
            "type": "Element",
            "min_length": 1,
            "max_length": 50,
            "pattern": r"[^<>]*[^<>\s][^<>]*",
        },
    )
    utdelningsadress2: Optional[str] = field(
        default=None,
        metadata={
            "name": "Utdelningsadress2",
            "type": "Element",
            "min_length": 1,
            "max_length": 50,
            "pattern": r"[^<>]*[^<>\s][^<>]*",
        },
    )
    postnummer: Optional[str] = field(
        default=None,
        metadata={
            "name": "Postnummer",
            "type": "Element",
            "min_length": 1,
            "max_length": 9,
            "pattern": r"[A-Za-z0-9 -]+",
        },
    )
    postort: Optional[str] = field(
        default=None,
        metadata={
            "name": "Postort",
            "type": "Element",
            "min_length": 1,
            "max_length": 50,
            "pattern": r"[^<>]*[^<>\s][^<>]*",
        },
    )
