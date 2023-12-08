from pynput.keyboard import Key


class Mapping:
    buttons: dict[str, Key]
    left_rotation: Key
    right_rotation: Key

    def __init__(self, buttons: dict[str, Key], left_rotation: Key, right_rotation: Key):
        self.buttons = buttons
        self.left_rotation = left_rotation
        self.right_rotation = right_rotation