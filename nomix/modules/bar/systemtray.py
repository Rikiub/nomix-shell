from ignis.services.system_tray import SystemTrayItem, SystemTrayService
from ignis.widgets import Widget

systemtray = SystemTrayService.get_default()


class TrayItem(Widget.Button):
    def __init__(self, item: SystemTrayItem, **kwargs):
        def popup():
            if item.menu:
                item.menu.popup()

        super().__init__(
            css_classes=["tray-item"],
            tooltip_text=item.bind("tooltip"),
            on_click=lambda _: popup(),
            on_right_click=lambda _: popup(),
            setup=lambda _: item.connect("removed", lambda _: self.unparent()),
            child=Widget.Box(
                child=[
                    Widget.Icon(image=item.bind("icon"), pixel_size=24),
                    item.menu,
                ]
            ),
            **kwargs,
        )


class SystemTray(Widget.Box):
    def __init__(self):
        super().__init__(
            css_classes=["systemtray"],
            setup=lambda _: systemtray.connect(
                "added",
                lambda _, item: self.append(TrayItem(item)),
            ),
        )
