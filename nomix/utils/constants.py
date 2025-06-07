from enum import Enum
from pathlib import Path

from gi.repository import Gdk, GLib  # type: ignore

USER_CONFIG_DIR = Path(GLib.get_user_config_dir())
USER_CACHE_DIR = Path(GLib.get_user_cache_dir())

IGNIS_DIR = USER_CONFIG_DIR / "ignis"
STYLES_DIR = IGNIS_DIR / "styles"
CACHE_DIR = IGNIS_DIR / ".cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

OVERRIDE_FILE = CACHE_DIR / "override.scss"
OVERRIDE_FILE.touch(exist_ok=True)

DARK_FILE = CACHE_DIR / "dark.scss"
DARK_FILE.touch(exist_ok=True)

NAVIGATION_KEYS = [
    Gdk.KEY_Up,
    Gdk.KEY_Down,
    Gdk.KEY_Left,
    Gdk.KEY_Right,
    Gdk.KEY_Return,
    Gdk.KEY_KP_Enter,
    Gdk.KEY_Tab,
    Gdk.KEY_ISO_Left_Tab,
    Gdk.KEY_Home,
    Gdk.KEY_End,
    Gdk.KEY_Page_Up,
    Gdk.KEY_Page_Down,
]


class ModuleWindow(str, Enum):
    NOTIFICATION_CENTER = "notification-center"
    CONTROL_CENTER = "control-center"
    LAUNCHER = "launcher"
    OSD = "osd"
