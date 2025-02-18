from gi.repository import Gio  # type: ignore
from ignis.utils.exec_sh import exec_sh_async

from .qsbutton import QSButton


class DarkModeQS(QSButton):
    def __init__(self):
        self.settings = Gio.Settings.new("org.gnome.desktop.interface")

        super().__init__(
            label="Dark Style",
            icon_name="display-brightness-symbolic",
            on_activate=lambda _: self.set_dark(),
            on_deactivate=lambda _: self.set_light(),
            active=self.is_dark(),
        )

        exec_sh_async("darkman run")
        self.settings.connect("changed::color-scheme", self.on_change)

    def on_change(self, setting: Gio.Settings, key: str):
        if setting.get_string(key) == "prefer-dark":
            self.set_dark()
        else:
            self.set_light()

    def set_light(self):
        self.settings.set_string("color-scheme", "prefer-light")
        exec_sh_async("darkman set light")

        self.set_active(False)

    def set_dark(self):
        self.settings.set_string("color-scheme", "prefer-dark")
        exec_sh_async("darkman set dark")

        self.set_active(True)

    def is_dark(self) -> bool:
        mode = self.settings.get_string("color-scheme")

        if mode == "prefer-dark":
            return True
        else:
            return False
