from microbit import *

radio.on()
radio.config(channel=2)

uart.init(baudrate=115200)

while True:
    incoming = radio.receive()

    # if incoming == "a_pressed":
    #     display.show("A")
    # elif incoming == "b_pressed":
    #     display.show("B")
    # elif incoming == "a_released":
    #     display.show("a")
    # elif incoming == "b_released":
    #     display.show("b")
    # else:
    #     display.show(incoming)

    uart.write(incoming + b"\n")