from statemachine import StateMachine, State
import pyautogui
import serial
from data import Button, ButtonType


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
            pyautogui.keyUp("left")
        elif state.id == "right":
            pyautogui.keyUp("right")
        elif state.id == "up":
            pyautogui.keyUp("up")

    def on_enter_state(self, event, state):
        print(f"Entering '{state.id}' state from '{event}' event.")
        if state.id == "left":
            pyautogui.keyDown("left")
        elif state.id == "right":
            pyautogui.keyDown("right")
        elif state.id == "up":
            pyautogui.keyDown("up")


key_machine = KeyMachine()

with serial.Serial('/dev/ttyACM0', baudrate=115200) as ser:
    ser.flush()
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().rstrip()

            data = Button.deserialize(line)

            if data.type == ButtonType.A:
                if data.is_pressed:
                    key_machine.a_pressed()
                else:
                    key_machine.a_released()
            elif data.type == ButtonType.B:
                if data.is_pressed:
                    key_machine.b_pressed()
                else:
                    key_machine.b_released()
