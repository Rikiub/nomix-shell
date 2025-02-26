import asyncio

from ignis.app import IgnisApp
from ignis.utils import Utils
from ignis.utils.shell import exec_sh_async

from nomix.utils.constants import USER_CONFIG_DIR

app = IgnisApp.get_default()


def monitor_gtk4_css():
    """Auto reload ignis on ~/.config/gtk-4.0/gtk.css changes"""

    Utils.FileMonitor(
        str(USER_CONFIG_DIR / "gtk-4.0" / "gtk.css"),
        callback=lambda *_: app.reload(),
    )

def send_notification(title: str, message: str, icon_name: str = ""):
    asyncio.create_task(
        exec_sh_async(
            f"notify-send --app-name 'Ignis' --icon '{icon_name}' '{title}' '{message}'"
        )
    )