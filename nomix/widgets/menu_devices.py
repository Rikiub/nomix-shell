from typing import Callable

from ignis.base_widget import BaseWidget
from ignis.gobject import Binding
from ignis.utils.exec_sh import exec_sh_async
from ignis.widgets import Widget

from nomix.widgets.menu import Menu


class DeviceItem(Widget.EventBox):
    def __init__(
        self,
        on_click: Callable | None = None,
        icon_name: str | Binding = "",
        extra_icon_name: str | Binding | None = None,
        label: str | Binding = "Device",
        active: bool | Binding = False,
        extra_widget: BaseWidget | None = None,
    ):
        start = Widget.Box(
            css_classes=["device-icons"],
            child=[
                Widget.Icon(
                    image=icon_name,
                    css_classes=["icon"],
                ),
                Widget.Icon(
                    image=extra_icon_name or "",
                    visible=bool(extra_icon_name),
                    pixel_size=10,
                    css_classes=["icon"],
                ),
            ],
        )

        center = Widget.Label(
            label=label,
            max_width_chars=35,
            ellipsize="end",
            css_classes=["label"],
        )

        check = Widget.Icon(
            image="object-select-symbolic",
            visible=active,
            tooltip_text="Connected",
            css_classes=["no-actionable"],
            halign="end",
            hexpand=True,
        )

        end = Widget.Box(
            css_classes=["indicators"],
            child=[
                extra_widget or Widget.Box(),
            ],
        )

        super().__init__(
            css_classes=["device-item"],
            child=[
                Widget.Button(
                    hexpand=True,
                    on_click=on_click,
                    child=Widget.Box(child=[start, center, check]),
                ),
                end,
            ],
        )


class DeviceMenu(Menu):
    def __init__(
        self,
        name: str,
        height_request: int = 150,
        header: BaseWidget | None = None,
        devices: list[DeviceItem] | Binding = [],
        settings_visible: bool = True,
        settings_label: str = "Settings",
        settings_command: str = "",
        css_classes: list["str"] = [],
        **kwargs,
    ):
        super().__init__(
            name=name,
            css_classes=["device-menu"] + css_classes,
            child=[
                Widget.Box(
                    vertical=True,
                    css_classes=["header"],
                    child=[header if header else Widget.Label(visible=False)],
                ),
                Widget.Scroll(
                    height_request=height_request,
                    vexpand=True,
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
                            css_classes=["device-item", "settings"],
                            on_click=lambda _: exec_sh_async(settings_command),
                            child=Widget.Box(
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
            **kwargs,
        )
