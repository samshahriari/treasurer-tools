"""AGI XML generation package."""

from .models import Employee
from .config import AGIConfig
from .generator import generate_agi_xml

__all__ = ["Employee", "AGIConfig", "generate_agi_xml"]
