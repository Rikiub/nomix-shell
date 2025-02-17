from enum import Enum
from pathlib import Path
from typing import Literal

from gi.repository import GLib  # type: ignore


class WindowName(str, Enum):
    notification_center = "notification-center"
    control_center = "control-center"
    launcher = "launcher"
    osd = "osd"

IGNIS_PATH = Path(GLib.get_user_config_dir(), "ignis")
ALIGN = Literal["start", "center", "end"]
