import asyncio
from typing import Callable

from ignis.base_widget import BaseWidget
from ignis.gobject import Binding, IgnisProperty
from ignis.utils.shell import exec_sh_async
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
        tooltip_text: str | Binding | None = None,
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
                    tooltip_text=tooltip_text,
                ),
                end,
            ],
        )


class DeviceMenu(Menu):
    def __init__(
        self,
        name: str,
        height_request: int = 200,
        header: BaseWidget | None = None,
        placeholder_text: str | Binding = "No devices found",
        devices: list[DeviceItem] | Binding = [],
        settings_visible: bool = True,
        settings_label: str = "Settings",
        settings_command: str = "",
        css_classes: list["str"] = [],
        **kwargs,
    ):
        self._placeholder_text = ""
        self._device_items: list[DeviceItem] = []

        self._devices_widget = Widget.Box(
            css_classes=["devices"], vertical=True, child=devices
        )

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
                    child=self._devices_widget,
                ),
                Widget.Box(
                    vertical=True,
                    visible=settings_visible,
                    child=[
                        Widget.Separator(),
                        Widget.Button(
                            css_classes=["device-item", "settings"],
                            on_click=lambda _: asyncio.create_task(
                                exec_sh_async(settings_command)
                            ),
                            child=Widget.Box(
                                css_classes=["device-icons"],
                                child=[
                                    Widget.Icon(
                                        image="preferences-system-symbolic",
                                        css_classes=["icon"],
                                    ),
                                    Widget.Label(
                                        label=settings_label,
                                        halign="start",
                                        css_classes=["icon"],
                                    ),
                                ],
                            ),
                        ),
                    ],
                ),
            ],
            **kwargs,
        )

        if isinstance(devices, Binding):
            self.bind_property2(
                "device_items",
                devices.target,
                devices.target_properties,
                devices.transform,
            )
        else:
            self._device_items = devices

        if isinstance(placeholder_text, Binding):
            self.bind_property2(
                "placeholder_text",
                placeholder_text.target,
                placeholder_text.target_properties,
                placeholder_text.transform,
            )
        else:
            self._placeholder_text = placeholder_text

    @IgnisProperty
    def placeholder_text(self) -> str:  # type: ignore
        return self._placeholder_text

    @placeholder_text.setter
    def placeholder_text(self, value: str):
        self._placeholder_text = value
        self._sync()

    @IgnisProperty
    def device_items(self) -> list[DeviceItem]:  # type: ignore
        return self._device_items

    @device_items.setter
    def device_items(self, value: list[DeviceItem]):
        self._device_items = value
        self._sync()

    def _get_placeholder_text(self) -> Widget.Label:
        return Widget.Label(
            label=self._placeholder_text,
            wrap="word",
            justify="center",
            valign="center",
            vexpand=True,
            css_classes=["placeholder-label"],
        )

    def _sync(self):
        if self.device_items:
            self._devices_widget.child = self.device_items
        else:
            self._devices_widget.child = [self._get_placeholder_text()]
