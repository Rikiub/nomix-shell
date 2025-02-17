from gi.repository import GLib  # type: ignore
from ignis.app import IgnisApp
from ignis.utils import Utils

from modules.bar import Bar
from modules.control_center import ControlCenter
from modules.launcher import Launcher
from modules.notification_center import NotificationCenter
from modules.notification_popup import NotificationPopup
from modules.osd import OSD

# SETUP
app = IgnisApp.get_default()
app.apply_css(f"{Utils.get_current_dir()}/style.scss")

# Auto reload in GTK theme changes
Utils.FileMonitor(
    f"{GLib.get_user_config_dir()}/gtk-4.0/gtk.css",
    callback=lambda path, event, _: app.reload(),
)

# WINDOWS
Launcher()
ControlCenter(valign="start", halign="end")
NotificationCenter()
OSD()

# Show in all monitors
for m in range(Utils.get_n_monitors()):
    Bar(m)
    NotificationPopup(m, anchor=["top", "right"])
