import asyncio
from typing import Callable

from ignis import widgets
from ignis.base_widget import BaseWidget
from ignis.gobject import Binding, IgnisProperty
from ignis.utils.shell import exec_sh_async

from nomix.widgets.menu import Menu


class DeviceItem(widgets.EventBox):
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
        start = widgets.Box(
            css_classes=["device-icons"],
            child=[
                widgets.Icon(
                    image=icon_name,
                    css_classes=["icon"],
                ),
                widgets.Icon(
                    image=extra_icon_name or "",
                    visible=bool(extra_icon_name),
                    pixel_size=10,
                    css_classes=["icon"],
                ),
            ],
        )

        center = widgets.Label(
            label=label,
            max_width_chars=35,
            ellipsize="end",
            css_classes=["label"],
        )

        check = widgets.Icon(
            image="object-select-symbolic",
            visible=active,
            tooltip_text="Connected",
            css_classes=["no-actionable"],
            halign="end",
            hexpand=True,
        )

        end = widgets.Box(
            css_classes=["indicators"],
            child=[
                extra_widget or widgets.Box(),
            ],
        )

        super().__init__(
            css_classes=["device-item"],
            child=[
                widgets.Button(
                    hexpand=True,
                    on_click=on_click,
                    child=widgets.Box(child=[start, center, check]),
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

        self._devices_widget = widgets.Box(
            css_classes=["devices"], vertical=True, child=devices
        )

        super().__init__(
            name=name,
            css_classes=["device-menu"] + css_classes,
            child=[
                widgets.Box(
                    vertical=True,
                    css_classes=["header"],
                    child=[header if header else widgets.Label(visible=False)],
                ),
                widgets.Scroll(
                    height_request=height_request,
                    vexpand=True,
                    child=self._devices_widget,
                ),
                widgets.Box(
                    vertical=True,
                    visible=settings_visible,
                    child=[
                        widgets.Separator(),
                        widgets.Button(
                            css_classes=["device-item", "settings"],
                            on_click=lambda _: asyncio.create_task(
                                exec_sh_async(settings_command)
                            ),
                            child=widgets.Box(
                                css_classes=["device-icons"],
                                child=[
                                    widgets.Icon(
                                        image="preferences-system-symbolic",
                                        css_classes=["icon"],
                                    ),
                                    widgets.Label(
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

    def _get_placeholder_text(self) -> widgets.Label:
        return widgets.Label(
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
