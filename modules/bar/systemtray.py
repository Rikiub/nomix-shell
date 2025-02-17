from ignis.dbus_menu import DBusMenu
from ignis.services.system_tray import SystemTrayItem, SystemTrayService
from ignis.widgets import Widget


class SystemTray(Widget.Box):
    def __init__(self):
        super().__init__(
            setup=lambda self: SystemTrayService.get_default().connect(
                "added", lambda x, item: self.append(self.tray_item(item))
            ),
            css_classes=["tray"],
            spacing=10,
        )

    def tray_item(self, item: SystemTrayItem) -> Widget.Button:
        if item.menu:
            menu: DBusMenu | None = item.menu.copy()
        else:
            menu = None

        return Widget.Button(
            child=Widget.Box(
                child=[
                    Widget.Icon(image=item.bind("icon"), pixel_size=24),
                    menu,
                ]
            ),
            setup=lambda self: item.connect("removed", lambda x: self.unparent()),
            tooltip_text=item.bind("tooltip"),
            on_click=lambda x: menu.popup() if menu else None,
            on_right_click=lambda x: menu.popup() if menu else None,
            css_classes=["tray-item"],
        )
