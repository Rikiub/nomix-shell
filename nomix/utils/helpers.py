from nomix.utils.constants import CONFIG_DIR

from ignis.app import IgnisApp
from ignis.utils import Utils

app = IgnisApp.get_default()


def monitor_gtk4_css():
    """Auto reload ignis on ~/.config/gtk-4.0/gtk.css changes"""

    Utils.FileMonitor(
        str(CONFIG_DIR / "gtk-4.0" / "gtk.css"),
        callback=lambda *_: app.reload(),
    )
