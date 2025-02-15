from ignis.utils.exec_sh import exec_sh_async

from .qsbutton import QSButton


class NightLightQS(QSButton):
    def __init__(self):
        super().__init__(
            label="Night Light",
            icon_name="night-light-symbolic",
            on_activate=lambda x: exec_sh_async("pkill -SIGUSR1 wlsunset"),
            on_deactivate=lambda x: exec_sh_async("pkill -SIGUSR1 wlsunset"),
        )
