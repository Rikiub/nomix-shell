from gi.repository import GLib  # type: ignore
from ignis.app import IgnisApp
from ignis.utils import Utils

from modules.bar import Bar
from modules.control_center import ControlCenter
from modules.launcher import Launcher
from modules.notification_center import NotificationCenter
from modules.notification_popup import NotificationPopup
from modules.osd import OSD

app = IgnisApp.get_default()
app.apply_css(f"{Utils.get_current_dir()}/style.scss")

Utils.FileMonitor(
    f"{GLib.get_user_config_dir()}/gtk-4.0/gtk.css",
    callback=lambda path, event, _: app.reload(),
)

Launcher()
ControlCenter(valign="start", halign="end")
NotificationCenter()
OSD()

for i in range(Utils.get_n_monitors()):
    Bar(i)
    NotificationPopup(i, anchor=["top", "right"])
