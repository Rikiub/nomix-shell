from ignis import utils
from ignis.app import IgnisApp
from ignis.css_manager import CssInfoPath, CssManager

from nomix.modules.bar import Bar
from nomix.modules.control_center import ControlCenter
from nomix.modules.launcher import Launcher
from nomix.modules.notification_center import NotificationCenter
from nomix.modules.notification_popup import NotificationPopup
from nomix.modules.osd import OSD
from nomix.services.color_scheme.service import ColorSchemeService
from nomix.utils.constants import CACHE_DIR, OVERRIDE_FILE, STYLES_DIR
from nomix.utils.helpers import monitor_gtk4_css
from nomix.utils.options import USER_OPTIONS

app = IgnisApp.get_initialized()

css_manager = CssManager.get_default()
css_manager.apply_css(
    CssInfoPath(
        name="index",
        path=str(STYLES_DIR / "index.scss"),
        compiler_function=utils.sass_compile,
    )
)
css_manager.apply_css(
    CssInfoPath(
        name="theme",
        path=str(CACHE_DIR / "override.scss"),
    )
)

# SETUP
# services
ColorSchemeService.get_default()

if USER_OPTIONS.matugen.enabled:
    from nomix.services.matugen import MatugenService

    MatugenService.get_default()
else:
    OVERRIDE_FILE.write_text("")

    # auto reload in GTK4 theme changes
    monitor_gtk4_css()

# Hot-reload options
USER_OPTIONS.matugen.connect_option("enabled", lambda *_: app.reload())

# WINDOWS
Launcher(halign="center")
ControlCenter(halign="end")
NotificationCenter(halign="end")
OSD()

# Show in all monitors
for m in range(utils.get_n_monitors()):
    Bar(m)
    NotificationPopup(m, anchor=["top", "right"])
