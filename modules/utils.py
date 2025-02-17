from enum import Enum
from pathlib import Path
from typing import Literal

from gi.repository import GLib  # type: ignore
from ignis.utils import Utils
from ignis.app import IgnisApp

app = IgnisApp.get_default()

CONFIG_DIR = Path(GLib.get_user_config_dir())
CACHE_DIR = Path(GLib.get_user_cache_dir())
IGNIS_DIR = CONFIG_DIR / "ignis"

ALIGN = Literal["start", "center", "end"]
ANCHOR = Literal["top", "bottom", "left", "right"]


class WindowName(str, Enum):
    notification_center = "notification-center"
    control_center = "control-center"
    launcher = "launcher"
    osd = "osd"


def monitor_gtk4_css():
    """Auto reload ignis on ~/.config/gtk-4.0/gtk.css changes"""

    Utils.FileMonitor(
        str(CONFIG_DIR / "gtk-4.0" / "gtk.css"),
        callback=lambda *_: app.reload(),
    )
