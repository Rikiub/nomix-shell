from ignis.app import IgnisApp
from ignis.widgets import Widget

from nomix.utils.constants import ModuleWindow
from nomix.widgets.actionable_button import ActionableButton

app = IgnisApp.get_default()


class LauncherButton(ActionableButton):
    def __init__(self):
        super().__init__(
            css_classes=["launcher-button"],
            tooltip_text="App Launcher",
            toggle_window=ModuleWindow.LAUNCHER,
            child=Widget.Icon(icon_name="start-here-symbolic", pixel_size=20),
        )
