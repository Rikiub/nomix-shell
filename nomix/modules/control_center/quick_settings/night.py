import asyncio
from ignis.utils.exec_sh import exec_sh_async

from nomix.utils.user_options import cache_options, user_options

from nomix.widgets.qsbutton import QSButton


class NightLightQS(QSButton):
    def __init__(self):
        super().__init__(
            label="Night Light",
            icon_name="night-light-symbolic",
            on_activate=lambda _: self.toggle(),
            on_deactivate=lambda _: self.toggle(),
            active=cache_options.bind("night_light"),
        )

        self._on_activate() if cache_options.night_light else self._on_deactivate()

    def toggle(self):
        self._on_deactivate() if self.active else self._on_activate()

    def _on_activate(self):
        asyncio.create_task(
            self._run_command(user_options.night_light.activate_command)
        )
        cache_options.night_light = True

    def _on_deactivate(self):
        asyncio.create_task(
            self._run_command(
                user_options.night_light.deactivate_command
                or user_options.night_light.activate_command
            )
        )
        cache_options.night_light = False

    async def _run_command(self, command: str):
        try:
            await exec_sh_async(command)
        except Exception:
            pass
