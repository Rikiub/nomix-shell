from enum import Enum
from pathlib import Path

from gi.repository import GLib  # type: ignore

USER_CONFIG_DIR = Path(GLib.get_user_config_dir())
USER_CACHE_DIR = Path(GLib.get_user_cache_dir())

IGNIS_DIR = USER_CONFIG_DIR / "ignis"
STYLES_DIR = IGNIS_DIR / "styles"
CACHE_DIR = IGNIS_DIR / ".cache"


class ModuleWindow(str, Enum):
    notification_center = "notification-center"
    control_center = "control-center"
    launcher = "launcher"
    osd = "osd"
