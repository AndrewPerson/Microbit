from microbit import *
from data import Button, ButtonType

radio.on()
radio.config(channel=2)

a_pressed = False
b_pressed = False

while True:
    if button_a.is_pressed():
        if not a_pressed:
            radio.send(Button(True, ButtonType.A).serialize())
            a_pressed = True
    else:
        if a_pressed:
            radio.send(Button(False, ButtonType.A).serialize())
            a_pressed = False

    if button_b.is_pressed():
        if not b_pressed:
            radio.send(Button(True, ButtonType.B).serialize())
            b_pressed = True
    else:
        if b_pressed:
            radio.send(Button(False, ButtonType.B).serialize())
            b_pressed = False