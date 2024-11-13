from enum import Enum


class Mouse:
    class Button(Enum):
        LEFT = 0
        RIGHT = 1
        MIDDLE = 2

    class Event(Enum):
        PRESS = 0
        RELEASE = 1
        DOUBLE_CLICK = 2
        MOVE = 3
