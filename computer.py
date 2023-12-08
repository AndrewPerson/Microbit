from pynput.keyboard import Key, Controller
import serial
from data import Message, ButtonMessage, CompassMessage
from mapping import Mapping


mappings = {
    "1": Mapping({ "A": Key.up, "B": Key.down }, Key.left, Key.right),
    "2": Mapping({ "A": "w", "B": "s" }, "a", "d"),
}

keyboard = Controller()

with serial.Serial('/dev/cu.usbmodem11402', baudrate=115200) as ser:
    ser.flush()
    while True:
        if ser.in_waiting > 0:
            length = int.from_bytes(ser.read(2), "big")
            message = ser.read(length)[3:]

            data = Message.deserialize(message)

            if isinstance(data, ButtonMessage):
                if data.button == "A":
                    if data.pressed:
                        keyboard.press(mappings[data.id].buttons["A"])
                    else:
                        keyboard.release(mappings[data.id].buttons["A"])
                elif data.button == "B":
                    if data.pressed:
                        keyboard.press(mappings[data.id].buttons["B"])
                    else:
                        keyboard.release(mappings[data.id].buttons["B"])
            elif isinstance(data, CompassMessage):
                if data.heading - 180 > 45:
                    keyboard.press(mappings[data.id].right_rotation)
                    keyboard.release(mappings[data.id].left_rotation)
                elif data.heading - 180 < -45:
                    keyboard.press(mappings[data.id].left_rotation)
                    keyboard.release(mappings[data.id].right_rotation)
                else:
                    keyboard.release(mappings[data.id].left_rotation)
                    keyboard.release(mappings[data.id].right_rotation)