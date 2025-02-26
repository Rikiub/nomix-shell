from gi.repository import Gio, GObject  # type: ignore
from ignis.base_service import BaseService

from nomix.utils.constants import DARK_FILE
from nomix.utils.global_options import cache_options

from .constants import (
    CHANGE_ICON,
    CHANGE_THEME,
    COLOR_SCHEME,
    GTK_ICON_DARK,
    GTK_ICON_LIGHT,
    GTK_THEME_DARK,
    GTK_THEME_LIGHT,
    STYLE_VARIABLE_NAME,
)


class ColorSchemeService(BaseService):
    def __init__(self) -> None:
        super().__init__()
        self._settings = Gio.Settings.new("org.gnome.desktop.interface")

        self._color_scheme: COLOR_SCHEME = self._settings.get_string("color-scheme")  # type: ignore
        self._is_dark: bool = False

        self._lock = False

        self._settings.connect(
            "changed::color-scheme",
            lambda config, key: not self._lock
            and self.set_color_scheme(config.get_string(key)),
        )
        cache_options.connect_option(
            "theme_is_dark", lambda *_: self._update_dark_variable()
        )

        self._sync()

    @GObject.Property
    def color_scheme(self) -> COLOR_SCHEME:  # type: ignore
        return self._color_scheme

    @color_scheme.setter
    def color_scheme(self, value: COLOR_SCHEME) -> None:
        self._color_scheme = value
        self._sync()

    @GObject.Property
    def is_dark(self) -> bool:  # type: ignore
        return self._is_dark

    @is_dark.setter
    def is_dark(self, value: bool) -> None:
        if value:
            self._color_scheme = "prefer-dark"
        else:
            self._color_scheme = "prefer-light"

        self._sync()

    def toggle(self) -> None:
        self.is_dark = not self.is_dark

    def _update_dark_variable(self) -> None:
        boolean = "false"
        if cache_options.theme_is_dark or self._is_dark:
            boolean = "true"

        content = f"${STYLE_VARIABLE_NAME}: {boolean};"
        DARK_FILE.write_text(content)

    def _sync(self):
        self._lock = True

        if self._color_scheme == "prefer-dark":
            if CHANGE_THEME:
                self._settings.set_string("gtk-theme", GTK_THEME_DARK)
            if CHANGE_ICON:
                self._settings.set_string("icon-theme", GTK_ICON_DARK)
            self._settings.set_string("color-scheme", "prefer-dark")

            self._is_dark = True
        elif self._color_scheme == "prefer-light":
            if CHANGE_THEME:
                self._settings.set_string("gtk-theme", GTK_THEME_LIGHT)
            if CHANGE_ICON:
                self._settings.set_string("icon-theme", GTK_ICON_LIGHT)
            self._settings.set_string("color-scheme", "prefer-light")

            self._is_dark = False
        else:
            return

        self.notify("color_scheme")
        self.notify("is_dark")

        self._update_dark_variable()

        self._lock = False