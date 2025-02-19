from gi.repository import Gio  # type: ignore
from ignis.utils.exec_sh import exec_sh_async

from nomix.services.color_scheme import ColorSchemeService

from .qsbutton import QSButton

color_scheme = ColorSchemeService.get_default()


class DarkModeQS(QSButton):
    def __init__(self):
        self.settings = Gio.Settings.new("org.gnome.desktop.interface")

        super().__init__(
            label="Dark Style",
            icon_name="display-brightness-symbolic",
            on_activate=lambda _: self.set_dark(),
            on_deactivate=lambda _: self.set_light(),
            active=color_scheme.bind("is_dark"),
        )

        exec_sh_async("darkman run")

        color_scheme.connect(
            "notify::color_scheme",
            lambda *_: self.set_dark() if color_scheme.is_dark() else self.set_light(),
        )

    def set_light(self):
        exec_sh_async("darkman set light")

    def set_dark(self):
        exec_sh_async("darkman set dark")
