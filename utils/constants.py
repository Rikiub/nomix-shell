from enum import Enum
from pathlib import Path

from gi.repository import GLib  # type: ignore

CONFIG_DIR = Path(GLib.get_user_config_dir())
CACHE_DIR = Path(GLib.get_user_cache_dir())
IGNIS_DIR = CONFIG_DIR / "ignis"


class WindowName(str, Enum):
    notification_center = "notification-center"
    control_center = "control-center"
    launcher = "launcher"
    osd = "osd"
