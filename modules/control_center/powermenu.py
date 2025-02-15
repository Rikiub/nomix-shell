from typing import Callable

from ignis.services.hyprland import HyprlandService
from ignis.services.niri import NiriService
from ignis.utils.exec_sh import exec_sh_async
from ignis.widgets import Widget

from widgets.menu_devices import DeviceItem, DeviceMenu

hyprland = HyprlandService.get_default()
niri = NiriService.get_default()


class PowerItem(DeviceItem):
    def __init__(self, label: str, on_click: Callable):
        super().__init__(label=label, on_click=on_click)


class PowerMenu(DeviceMenu):
    def __init__(self, **kwargs):
        menu = [
            PowerItem(
                label="Suspend", on_click=lambda _: exec_sh_async("systemctl suspend")
            ),
            Widget.Separator(),
            PowerItem(
                label="Reboot", on_click=lambda _: exec_sh_async("systemctl reboot")
            ),
            PowerItem(
                label="Shutdown", on_click=lambda _: exec_sh_async("systemctl poweroff")
            ),
            Widget.Separator(),
            PowerItem(label="Logout", on_click=lambda _: self._logout()),
        ]

        super().__init__(name="power", settings_visible=False, devices=menu)

    def _logout(self) -> None:
        if hyprland.is_available:
            exec_sh_async("hyprctl dispatch exit 0")
        elif niri.is_available:
            exec_sh_async("niri msg action quit")


class PowerButton(Widget.Box):
    def __init__(self, **kwargs):
        menu = PowerMenu()

        arrow = Widget.Button(
            child=Widget.Arrow(pixel_size=20, rotated=menu.bind("reveal_child")),
            on_click=lambda x: menu.toggle(),
        )

        super().__init__(
            vertical=True,
            halign="end",
            child=[
                Widget.Box(
                    hexpand=True,
                    halign="end",
                    child=[arrow],
                ),
                menu,
            ],
        )
