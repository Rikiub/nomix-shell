from ignis.utils.exec_sh import exec_sh_async

from modules.user_options import cache_options
from .qsbutton import QSButton


class NightLightQS(QSButton):
    def __init__(self):
        def do_toggle():
            cache_options.night_light = not self.active

        def on_activate(toggle):
            exec_sh_async("wlsunset")

            if toggle:
                do_toggle()

        def on_deactivate(toggle):
            exec_sh_async("pkill wlsunset")

            if toggle:
                do_toggle()

        super().__init__(
            label="Night Light",
            icon_name="night-light-symbolic",
            on_activate=lambda _: on_activate(True),
            on_deactivate=lambda _: on_deactivate(True),
            active=cache_options.bind("night_light"),
        )

        if self.active:
            on_activate(False)
        else:
            on_deactivate(False)