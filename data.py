try:
    from typing import Type
except ImportError:
    pass

import struct

class Message:
    types: dict[str, Type["Message"]] = {}

    def __init__(self, id: str, inherited_obj: "Message"):
        self.id = id
        self.type = type(inherited_obj)
        self.inherited_obj = inherited_obj

    @staticmethod
    def register_type(type: Type["Message"]):
        Message.types[type.__name__] = type

    @staticmethod
    def deserialize(data: bytes) -> "Message":
        id_len = data[0]
        id = data[1 : id_len + 1].decode("utf-8")

        type_len = data[id_len + 1]
        type = data[id_len + 2 : id_len + 2 + type_len].decode("utf-8")

        return Message.types[type]._deserialize_internal(id, data[id_len + 2 + type_len :])

    @staticmethod
    def _deserialize_internal(id: str, data: bytes) -> "Message":
        raise NotImplementedError

    def serialize(self) -> bytes:
        return bytes(
            [len(self.id)]
            + list(self.id.encode("utf-8"))
            + [len(self.type.__name__)]
            + list(self.type.__name__.encode("utf-8"))
            + list(self._serialize_internal())
        )
    
    def _serialize_internal(self) -> bytes:
        raise NotImplementedError


class ButtonMessage(Message):
    def __init__(self, id: str, button: str, pressed: bool):
        super().__init__(id, self)
        self.button = button
        self.pressed = pressed

    @staticmethod
    def _deserialize_internal(id: str, data: bytes) -> "ButtonMessage":
        button_len = data[0]
        button = data[1 : button_len + 1].decode("utf-8")

        pressed = bool(data[button_len + 1])

        return ButtonMessage(id, button, pressed)

    def _serialize_internal(self) -> bytes:
        return bytes(
            [len(self.button)]
            + list(self.button.encode("utf-8"))
            + [self.pressed]
        )


class CompassMessage(Message):
    def __init__(self, id: str, x: float, y: float, z: float):
        super().__init__(id, self)
        self.x = x
        self.y = y
        self.z = z

    @staticmethod
    def _deserialize_internal(id: str, data: bytes) -> "CompassMessage":
        x, y, z = struct.unpack("fff", data)

        return CompassMessage(id, x, y, z)
    
    def _serialize_internal(self) -> bytes:
        return struct.pack("fff", self.x, self.y, self.z)

Message.register_type(ButtonMessage)
Message.register_type(CompassMessage)
