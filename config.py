from ignis.app import IgnisApp
from ignis.utils import Utils

from nomix.modules.bar import Bar
from nomix.modules.control_center import ControlCenter
from nomix.modules.launcher import Launcher
from nomix.modules.notification_center import NotificationCenter
from nomix.modules.notification_popup import NotificationPopup
from nomix.modules.osd import OSD
from nomix.services.color_scheme.service import ColorSchemeService
from nomix.services.matugen import MatugenService
from nomix.utils.constants import STYLES_DIR
from nomix.utils.helpers import monitor_gtk4_css, setup_cache

# SETUP
# cache directory
setup_cache()

# services
MatugenService.get_default()
ColorSchemeService.get_default()

app = IgnisApp.get_default()
app.apply_css(str(STYLES_DIR / "index.scss"))

# auto reload in GTK4 theme changes
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
