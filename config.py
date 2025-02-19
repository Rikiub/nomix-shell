from ignis.app import IgnisApp
from ignis.utils import Utils

from modules.bar import Bar
from modules.control_center import ControlCenter
from modules.launcher import Launcher
from modules.notification_center import NotificationCenter
from modules.notification_popup import NotificationPopup
from modules.osd import OSD
from utils.constants import STYLES_DIR
from utils.helpers import monitor_gtk4_css

# SETUP
app = IgnisApp.get_default()
app.apply_css(str(STYLES_DIR / "index.scss"))

# Auto reload in GTK4 theme changes
monitor_gtk4_css()

# WINDOWS
Launcher()
ControlCenter(halign="end", valign="start")
NotificationCenter(halign="end")
OSD()

# Show in all monitors
for m in range(Utils.get_n_monitors()):
    Bar(m)
    NotificationPopup(m, anchor=["top", "right"])
