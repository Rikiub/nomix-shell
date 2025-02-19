from typing import Literal

from gi.repository import Gio, GObject  # type: ignore
from ignis.base_service import BaseService

from .constants import STYLE_FILE, STYLE_TEMPLATE


class ColorSchemeService(BaseService):
    def __init__(self) -> None:
        super().__init__()

        self.settings = Gio.Settings.new("org.gnome.desktop.interface")

        self._color_scheme = self.color_scheme
        self._is_dark = self._check_is_dark()

        self._write_style()

        self.settings.connect("changed::color-scheme", self._on_change)

    @GObject.Property
    def color_scheme(self) -> Literal["default", "prefer-light", "prefer-dark"]:
        return self.settings.get_string("color-scheme")  # type: ignore

    @GObject.Property
    def is_dark(self) -> bool:
        return self._is_dark

    @GObject.Property
    def is_light(self) -> bool:
        return not self._is_dark

    def _write_style(self) -> None:
        STYLE_FILE.touch(exist_ok=True)
        STYLE_FILE.write_text(
            STYLE_TEMPLATE.format("true" if self.is_dark else "false")
        )

    def _set_light(self):
        self.settings.set_string("color-scheme", "prefer-light")
        self._is_dark = False

        self.notify("is_light")
        self.notify("is_dark")

        self._write_style()

    def _set_dark(self):
        self.settings.set_string("color-scheme", "prefer-dark")
        self._is_dark = True

        self.notify("is_light")
        self.notify("is_dark")

        self._write_style()

    def _check_is_dark(self) -> bool:
        if self.color_scheme == "prefer-dark":
            return True
        else:
            return False

    def _on_change(self, setting: Gio.Settings, key: str):
        scheme = setting.get_string(key)

        if scheme == "prefer-dark":
            self._set_dark()
        else:
            self._set_light()

        self._color_scheme = scheme
        self.notify("color_scheme")
