from enum import Enum
from typing import Literal


class WindowName(str, Enum):
    notification_center = "notification-center"
    control_center = "control-center"
    launcher = "launcher"
    osd = "osd"


ALIGN = Literal["start", "center", "end"]
