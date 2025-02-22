from ignis.app import IgnisApp
from ignis.utils import Utils

from nomix.utils.constants import CACHE_DIR, USER_CONFIG_DIR

app = IgnisApp.get_default()


def monitor_gtk4_css():
    """Auto reload ignis on ~/.config/gtk-4.0/gtk.css changes"""

    Utils.FileMonitor(
        str(USER_CONFIG_DIR / "gtk-4.0" / "gtk.css"),
        callback=lambda *_: app.reload(),
    )

def setup_cache():
    files = [CACHE_DIR / "override.scss", CACHE_DIR / "_dark.scss"]

    for f in files:
        f.touch(exist_ok=True)