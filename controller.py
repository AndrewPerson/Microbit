from microbit import *
import radio
from data import ButtonMessage, CompassMessage

# display.scroll("Select the id")
# display.scroll("A increments")
# display.scroll("B decrements")
# display.scroll("A + B selects")

id = 0
while not (button_a.is_pressed() and button_b.is_pressed()):
    display.show(str(id))

    if button_a.was_pressed():
        id += 1

    if button_b.was_pressed():
        id -= 1

display.show(Image.SKULL)

radio.on()
radio.config(channel=2)

sleep(1000)

a_pressed = False
b_pressed = False

while True:
    if button_a.is_pressed():
        if not a_pressed:
            radio.send(ButtonMessage(str(id), "A", True).serialize())
            a_pressed = True
    else:
        if a_pressed:
            radio.send(ButtonMessage(str(id), "A", False).serialize())
            a_pressed = False

    if button_b.is_pressed():
        if not b_pressed:
            radio.send(ButtonMessage(str(id), "B", True).serialize())
            b_pressed = True
    else:
        if b_pressed:
            radio.send(ButtonMessage(str(id), "B", False).serialize())
            b_pressed = False

    radio.send(CompassMessage(str(id), compass.get_x(), compass.get_y(), compass.get_z()).serialize())
