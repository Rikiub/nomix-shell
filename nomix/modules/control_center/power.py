from typing import Callable

from ignis.services.hyprland import HyprlandService
from ignis.services.niri import NiriService
from ignis.utils.exec_sh import exec_sh_async
from ignis.widgets import Widget

from nomix.widgets.menu_devices import DeviceItem, DeviceMenu

hyprland = HyprlandService.get_default()
niri = NiriService.get_default()


class PowerItem(DeviceItem):
    def __init__(self, on_click: Callable, label: str = "", icon_name: str = ""):
        super().__init__(label=label, icon_name=icon_name, on_click=on_click)


class PowerMenu(DeviceMenu):
    def __init__(self):
        menu = [
            PowerItem(
                label="Suspend",
                icon_name="system-suspend-symbolic",
                on_click=lambda _: exec_sh_async("systemctl suspend"),
            ),
            Widget.Separator(),
            PowerItem(
                label="Reboot",
                icon_name="system-reboot-symbolic",
                on_click=lambda _: exec_sh_async("systemctl reboot"),
            ),
            PowerItem(
                label="Shutdown",
                icon_name="system-shutdown-symbolic",
                on_click=lambda _: exec_sh_async("systemctl poweroff"),
            ),
            Widget.Separator(),
            PowerItem(
                label="Logout",
                icon_name="system-log-out-symbolic",
                on_click=lambda _: self._logout(),
            ),
        ]

        super().__init__(
            name="power",
            css_classes=["power-menu"],
            height_request=210,
            settings_visible=False,
            devices=menu,
            header=Widget.Box(
                child=[
                    Widget.Icon(
                        image="system-shutdown-symbolic",
                        pixel_size=24,
                        style="margin-right: 5px;",
                    ),
                    Widget.Label(
                        label="Power Menu",
                        halign="start",
                    ),
                ],
            ),
        )

    def _logout(self) -> None:
        if hyprland.is_available:
            exec_sh_async("hyprctl dispatch exit 0")
        elif niri.is_available:
            exec_sh_async("niri msg action quit --skip-confirmation")


class PowerButton(Widget.Button):
    def __init__(self, **kwargs):
        self.menu = PowerMenu()

        super().__init__(
            child=Widget.Box(
                child=[
                    Widget.Icon(image="system-shutdown-symbolic"),
                    Widget.Arrow(
                        pixel_size=20,
                        rotated=self.menu.bind("reveal_child"),
                    ),
                ],
            ),
            on_click=lambda _: self.menu.toggle(),
            **kwargs,
        )
