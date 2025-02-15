from enum import Enum
from typing import Literal


class WindowName(str, Enum):
    control = "control"
    launcher = "launcher"
    osd = "osd"


ALIGN = Literal["start", "center", "end"]
