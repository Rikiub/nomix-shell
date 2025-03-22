from enum import Enum
from pathlib import Path

from gi.repository import GLib  # type: ignore

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


class ModuleWindow(str, Enum):
    NOTIFICATION_CENTER = "notification-center"
    CONTROL_CENTER = "control-center"
    LAUNCHER = "launcher"
    OSD = "osd"
