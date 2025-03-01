import asyncio

from ignis.services.bluetooth import BluetoothDevice, BluetoothService
from ignis.widgets import Widget

from nomix.utils.global_options import user_options
from nomix.widgets.header_label import HeaderLabel
from nomix.widgets.menu_devices import DeviceItem, DeviceMenu
from nomix.widgets.qsbutton import QSButton

bluetooth = BluetoothService.get_default()


class BluetoothItem(DeviceItem):
    def __init__(self, device: BluetoothDevice):
        super().__init__(
            icon_name=device.bind("icon_name", lambda v: v + "-symbolic"),
            label=device.alias,
            active=device.bind("connected"),
            on_click=lambda _: asyncio.create_task(device.disconnect_from())
            if device.connected
            else asyncio.create_task(device.connect_to()),
            extra_widget=Widget.Icon(
                image="bluetooth-active-symbolic",
                tooltip_text="Paired",
                visible=device.bind("paired"),
                css_classes=["no-actionable"],
            ),
        )


class BluetoothMenu(DeviceMenu):
    def __init__(self):
        super().__init__(
            name="bluetooth",
            header=HeaderLabel(
                icon_name="bluetooth-active-symbolic",
                label="Bluetooth",
                active=bluetooth.bind("powered"),
            ),
            devices=bluetooth.bind(
                "devices", lambda value: [BluetoothItem(i) for i in value]
            ),
            settings_label="Bluetooth Settings",
            settings_command=user_options.control_apps.bluetooth,
        )


class BluetoothQS(QSButton):
    def __init__(self):
        def get_label(devices: list[BluetoothDevice]) -> str | None:
            if len(devices) == 0:
                return None
            elif len(devices) == 1:
                return devices[0].alias
            else:
                return f"{len(devices)} pairs"

        super().__init__(
            title="Bluetooth",
            subtitle=bluetooth.bind("connected_devices", get_label),
            icon_name="bluetooth-active-symbolic",
            on_activate=lambda _: bluetooth.set_powered(True),
            on_deactivate=lambda _: bluetooth.set_powered(False),
            active=bluetooth.bind("powered"),
            menu=BluetoothMenu(),
        )
        bluetooth.notify("connected_devices")


def bluetooth_control() -> list[QSButton]:
    # return [] if bluetooth.state == "absent" else [BluetoothButton()]
    return [BluetoothQS()]
