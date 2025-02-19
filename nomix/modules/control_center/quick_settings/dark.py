from nomix.services.color_scheme import ColorSchemeService

from .qsbutton import QSButton

color_scheme = ColorSchemeService.get_default()


class DarkModeQS(QSButton):
    def __init__(self):
        super().__init__(
            label="Dark Style",
            icon_name="display-brightness-symbolic",
            on_activate=lambda _: color_scheme.toggle(),
            on_deactivate=lambda _: color_scheme.toggle(),
            active=color_scheme.bind("is_dark"),
        )
