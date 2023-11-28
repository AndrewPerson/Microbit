from dataclasses import dataclass
from enum import Enum


class ButtonType(Enum):
    A = 1
    B = 2


@dataclass
class Button:
    is_pressed: bool
    type: ButtonType

    def serialize(self) -> bytes:
        return bytes([self.is_pressed, self.type.value])
    
    @staticmethod
    def deserialize(data: bytes) -> "Button":
        return Button(bool(data[0]), ButtonType(data[1]))