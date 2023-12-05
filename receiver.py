from microbit import *
import radio

display.show(Image.HEART)

radio.on()
radio.config(channel=2)

uart.init(baudrate=115200)

while True:
    incoming = radio.receive()

    if incoming:
        # TODO: Make the byte length of the length itself variable. For now, just don't send big messages. RIP.
        uart.write(len(incoming).to_bytes(2, "big") + incoming)