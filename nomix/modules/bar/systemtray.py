from ignis import widgets
from ignis.services.system_tray import SystemTrayItem, SystemTrayService

systemtray = SystemTrayService.get_default()


class TrayItem(widgets.Button):
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
            child=widgets.Box(
                child=[
                    widgets.Icon(image=item.bind("icon"), pixel_size=24),
                    item.menu,
                ]
            ),
            **kwargs,
        )


class SystemTray(widgets.Box):
    def __init__(self):
        super().__init__(
            css_classes=["systemtray"],
            setup=lambda _: systemtray.connect(
                "added",
                lambda _, item: self.append(TrayItem(item)),
            ),
        )
