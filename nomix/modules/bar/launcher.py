from ignis import widgets
from ignis.app import IgnisApp

from nomix.utils.constants import ModuleWindow
from nomix.widgets.action_button import ActionButton

app = IgnisApp.get_default()


class Launcher(ActionButton):
    def __init__(self, css_classes: list[str] = []):
        super().__init__(
            css_classes=["launcher-button", *css_classes],
            tooltip_text="App Launcher",
            toggle_window=ModuleWindow.LAUNCHER,
            child=widgets.Icon(icon_name="view-grid-symbolic", pixel_size=24),
        )
