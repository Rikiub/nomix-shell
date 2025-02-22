from ignis.services.hyprland import HyprlandService
from ignis.services.niri import NiriService
from ignis.utils.exec_sh import exec_sh
from ignis.widgets import Widget

hyprland = HyprlandService.get_default()
niri = NiriService.get_default()


class PowerMenu(Widget.Button):
    def __init__(self, **kwargs):
        menu = Widget.PopoverMenu(
            items=[
                Widget.MenuItem(
                    label="Lock",
                    on_activate=lambda x: exec_sh("swaylock"),
                ),
                Widget.Separator(),
                Widget.MenuItem(
                    label="Suspend",
                    on_activate=lambda x: exec_sh("systemctl suspend"),
                ),
                # Widget.MenuItem(
                #    label="Hibernate",
                #    on_activate=lambda x: exec_sh("systemctl hibernate"),
                # ),
                Widget.Separator(),
                Widget.MenuItem(
                    label="Reboot",
                    on_activate=lambda x: exec_sh("systemctl reboot"),
                ),
                Widget.MenuItem(
                    label="Shutdown",
                    on_activate=lambda x: exec_sh("systemctl poweroff"),
                ),
                Widget.Separator(),
                Widget.MenuItem(
                    label="Logout",
                    enabled=hyprland.is_available or niri.is_available,  # type: ignore
                    on_activate=lambda x: self.logout(),
                ),
            ]
        )

        super().__init__(
            child=Widget.Box(
                child=[
                    Widget.Icon(image="system-shutdown-symbolic", pixel_size=20),
                    menu,
                ]
            ),
            css_classes=["powermenu-button"],
            on_click=lambda x: menu.popup(),
            **kwargs,
        )

    def logout(self) -> None:
        if hyprland.is_available:
            exec_sh("hyprctl dispatch exit 0")
        elif niri.is_available:
            exec_sh("niri msg action quit --skip-confirmation")
