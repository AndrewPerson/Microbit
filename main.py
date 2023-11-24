from statemachine import StateMachine, State
from microbit import *

radio.on()
radio.config(channel=2)

class KeyMachine(StateMachine):
    no_key = State(initial=True)
    left = State()
    right = State()
    up = State()

    a_pressed = no_key.to(left) | right.to(up)
    b_pressed = no_key.to(right) | left.to(up)

    a_released = left.to(no_key) | up.to(right)
    b_released = right.to(no_key) | up.to(left)

    def on_exit_state(self, event, state):
        print(f"Exiting '{state.id}' state from '{event}' event.")
        if state.id == "left":
            radio.send(bytes([0x11]))
        elif state.id == "right":
            radio.send(bytes([0x21]))
        elif state.id == "up":
            radio.send(bytes([0x01]))

    def on_enter_state(self, event, state):
        print(f"Entering '{state.id}' state from '{event}' event.")
        if state.id == "left":
            radio.send(bytes([0x10]))
        elif state.id == "right":
            radio.send(bytes([0x20]))
        elif state.id == "up":
            radio.send(bytes([0x00]))

key_machine = KeyMachine()

while True:
    if button_a.is_pressed():
        key_machine.a_pressed()
    else:
        key_machine.a_released()

    if button_b.is_pressed():
        key_machine.b_pressed()
    else:
        key_machine.b_released()
