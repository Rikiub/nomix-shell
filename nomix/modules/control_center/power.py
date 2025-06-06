from typing import Callable

from ignis import widgets
from ignis.services.hyprland import HyprlandService
from ignis.services.niri import NiriService
from ignis.utils.shell import exec_sh

from nomix.widgets.header_label import HeaderLabel
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
                on_click=lambda _: exec_sh("systemctl suspend"),
            ),
            PowerItem(
                label="Reboot",
                icon_name="system-reboot-symbolic",
                on_click=lambda _: exec_sh("systemctl reboot"),
            ),
            PowerItem(
                label="Shutdown",
                icon_name="system-shutdown-symbolic",
                on_click=lambda _: exec_sh("systemctl poweroff"),
            ),
            widgets.Separator(),
            PowerItem(
                label="Logout",
                icon_name="system-log-out-symbolic",
                on_click=lambda _: self._logout(),
            ),
        ]

        super().__init__(
            name="power",
            css_classes=["power-menu"],
            height_request=170,
            settings_visible=False,
            devices=menu,
            header=HeaderLabel(
                icon_name="system-shutdown-symbolic", label="Power Menu"
            ),
        )

    def _logout(self) -> None:
        if hyprland.is_available:
            exec_sh("hyprctl dispatch exit 0")
        elif niri.is_available:
            exec_sh("niri msg action quit --skip-confirmation")


class PowerButton(widgets.Button):
    def __init__(self, **kwargs):
        self.menu = PowerMenu()

        super().__init__(
            css_classes=["power-menu-button"],
            child=widgets.Box(
                child=[
                    widgets.Icon(image="system-shutdown-symbolic"),
                    widgets.Arrow(
                        pixel_size=20,
                        rotated=self.menu.bind("reveal_child"),
                    ),
                ],
            ),
            on_click=lambda _: self.menu.toggle(),
            **kwargs,
        )
