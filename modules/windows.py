from enum import Enum


class WindowName(str, Enum):
    control = "control"
    launcher = "launcher"
    osd = "osd"
