"""AGI XML generation package."""

from .models import Employee
from .agi.config import AGIConfig
from .agi.generator import generate_agi_xml

__all__ = ["Employee", "AGIConfig", "generate_agi_xml"]
