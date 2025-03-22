from os import PathLike
from typing import Literal

ALIGN = Literal["start", "center", "end"]
ANCHOR = Literal["top", "bottom", "left", "right"]
TRANSITION_TYPE = Literal[
    "none",
    "crossfade",
    "slide_right",
    "slide_left",
    "slide_up",
    "slide_down",
    "swing_right",
    "swing_left",
    "swing_up",
    "swing_down",
]

StrPath = str | PathLike[str]
