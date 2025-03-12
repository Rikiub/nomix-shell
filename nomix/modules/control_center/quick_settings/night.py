import asyncio

from ignis.utils.shell import exec_sh_async

from nomix.utils.options import CACHE_OPTIONS, USER_OPTIONS
from nomix.widgets.qsbutton import QSButton


class NightLightQS(QSButton):
    def __init__(self):
        super().__init__(
            title="Night Light",
            icon_name="night-light-symbolic",
            on_activate=lambda _: self.toggle(),
            on_deactivate=lambda _: self.toggle(),
            active=CACHE_OPTIONS.bind("night_light"),
        )

        self._on_activate() if CACHE_OPTIONS.night_light else self._on_deactivate()

    def toggle(self):
        self._on_deactivate() if self.active else self._on_activate()

    def _on_activate(self):
        asyncio.create_task(
            self._run_command(USER_OPTIONS.night_light.activate_command)
        )
        CACHE_OPTIONS.night_light = True

    def _on_deactivate(self):
        asyncio.create_task(
            self._run_command(
                USER_OPTIONS.night_light.deactivate_command
                or USER_OPTIONS.night_light.activate_command
            )
        )
        CACHE_OPTIONS.night_light = False

    async def _run_command(self, command: str):
        try:
            await exec_sh_async(command)
        except Exception:
            pass


def night_light_control():
    if USER_OPTIONS.night_light.enabled:
        return [NightLightQS()]

    return []
