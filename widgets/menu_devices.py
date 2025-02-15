from typing import Callable
from ignis.base_widget import BaseWidget
from ignis.gobject import Binding
from ignis.widgets import Widget
from ignis.utils.exec_sh import exec_sh_async

from widgets.menu import Menu


class DeviceItem(Widget.Button):
    def __init__(
        self,
        on_click: Callable | None = None,
        icon_name: str | Binding = "",
        label: str | Binding = "Device",
        active: bool | Binding = False,
    ):
        super().__init__(
            on_click=on_click,
            css_classes=["device-item"],
            child=Widget.Box(
                child=[
                    Widget.Icon(
                        image=icon_name,
                        style="margin-right: 8px;",
                        css_classes=["icon"],
                    ),
                    Widget.Label(
                        label=label,
                        halign="start",
                        css_classes=["label"],
                    ),
                    Widget.Icon(
                        image="object-select-symbolic",
                        halign="end",
                        hexpand=True,
                        visible=active,
                        css_classes=["check"],
                    ),
                ]
            ),
        )


class DeviceMenu(Menu):
    def __init__(
        self,
        name: str,
        header: BaseWidget | None = None,
        devices: list[DeviceItem] | Binding = [],
        settings_visible: bool = True,
        settings_label: str = "Settings",
        settings_command: str = "",
    ):
        super().__init__(
            name=name,
            css_classes=["device-menu"],
            child=[
                Widget.Box(
                    vertical=True,
                    css_classes=["header"],
                    child=[header if header else Widget.Label(visible=False)],
                ),
                Widget.Scroll(
                    height_request=130,
                    child=Widget.Box(
                        css_classes=["devices"],
                        vertical=True,
                        child=devices,
                    ),
                ),
                Widget.Box(
                    vertical=True,
                    visible=settings_visible,
                    child=[
                        Widget.Separator(),
                        Widget.Button(
                            on_click=lambda x: exec_sh_async(settings_command),
                            child=Widget.Box(
                                css_classes=["settings"],
                                child=[
                                    Widget.Icon(
                                        image="preferences-system-symbolic",
                                        style="margin-right: 6px;",
                                    ),
                                    Widget.Label(
                                        label=settings_label,
                                        halign="start",
                                    ),
                                ],
                            ),
                        ),
                    ],
                ),
            ],
        )
