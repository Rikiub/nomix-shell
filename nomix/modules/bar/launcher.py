from ignis.app import IgnisApp
from ignis.widgets import Widget
from nomix.utils.constants import ModuleWindow

app = IgnisApp.get_default()


class LauncherButton(Widget.Button):
    def __init__(self, **kwargs):
        super().__init__(
            on_click=lambda _: app.toggle_window(ModuleWindow.LAUNCHER),
            tooltip_text="App Launcher",
            child=Widget.Icon(image="start-here-symbolic", pixel_size=20),
            css_classes=["launcher-button"],
            **kwargs,
        )

        self._launcher = app.get_window(ModuleWindow.LAUNCHER)
        self._launcher.connect("notify::visible", lambda *_: self._toggle_active())

    def _toggle_active(self):
        if self._launcher.is_visible():
            self.add_css_class("active")
        else:
            self.remove_css_class("active")
