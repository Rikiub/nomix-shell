from gi.repository import Gio  # type: ignore
from ignis.utils.exec_sh import exec_sh

from .qsbutton import QSButton


class DarkModeQS(QSButton):
    def __init__(self):
        super().__init__(
            label="Dark Style",
            icon_name="display-brightness-symbolic",
            on_activate=lambda x: self.set_dark(),
            on_deactivate=lambda x: self.set_light(),
            active=self.is_dark(),
        )

        self.settings = Gio.Settings.new("org.gnome.desktop.interface")
        self.settings.connect("changed::color-scheme", self.on_change)

    def on_change(self, setting: Gio.Settings, key: str):
        if setting.get_string(key) == "prefer-dark":
            self.set_dark()
        else:
            self.set_light()

    def set_light(self):
        self.settings.set_string("color-scheme", "prefer-light")
        exec_sh("darkman set light")

        self.set_active(False)

    def set_dark(self):
        self.settings.set_string("color-scheme", "prefer-dark")
        exec_sh("darkman set dark")

        self.set_active(True)

    def is_dark(self) -> bool:
        mode: str = exec_sh("darkman get").stdout
        mode = mode.strip()

        if mode == "dark":
            return True
        else:
            return False
