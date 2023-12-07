from pynput.keyboard import Key, Controller
import serial
from data import Message, ButtonMessage, CompassMessage
import os


keyboard = Controller()

with serial.Serial('/dev/ttyACM0', baudrate=115200) as ser:
    ser.flush()
    while True:
        if ser.in_waiting > 0:
            length = int.from_bytes(ser.read(2), "big")
            message = ser.read(length)[3:]

            data = Message.deserialize(message)

            if isinstance(data, ButtonMessage):
                if data.button == "A":
                    if data.pressed:
                        keyboard.press(Key.up)
                    else:
                        keyboard.release(Key.up)
                elif data.button == "B":
                    if data.pressed:
                        keyboard.press(Key.down)
                    else:
                        keyboard.release(Key.down)
            elif isinstance(data, CompassMessage):
                os.system("clear")
                print(data.x, data.y, data.z)