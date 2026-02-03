"""Pin data model for ESP32 pinout."""
from dataclasses import dataclass
from typing import List


@dataclass
class Pin:
    """Represents a single ESP32 pin with its properties."""
    name: str
    functions: List[str]
    pin_type: str
    note: str = ""
