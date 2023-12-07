from pynput.keyboard import Key, Controller
import serial
from data import Message, ButtonMessage, CompassMessage
import os


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
                        keyboard.press(Key.up)
                    else:
                        keyboard.release(Key.up)
                elif data.button == "B":
                    if data.pressed:
                        keyboard.press(Key.down)
                    else:
                        keyboard.release(Key.down)
            elif isinstance(data, CompassMessage):
                if data.heading - 180 > 30:
                    keyboard.press(Key.right)
                    keyboard.release(Key.left)
                elif data.heading - 180 < -30:
                    keyboard.press(Key.left)
                    keyboard.release(Key.right)
                else:
                    keyboard.release(Key.left)
                    keyboard.release(Key.right)