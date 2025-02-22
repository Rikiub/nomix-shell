import asyncio

from ignis.services.bluetooth import BluetoothDevice, BluetoothService
from ignis.widgets import Widget

from nomix.utils.user_options import user_options
from nomix.widgets.menu_devices import DeviceItem, DeviceMenu
from nomix.widgets.qsbutton import QSButton
from nomix.widgets.toggle_box import ToggleBox

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
            header=ToggleBox(
                label="Bluetooth",
                active=bluetooth.bind("powered"),
                on_change=lambda _, state: bluetooth.set_powered(state),
                css_classes=["network-header-box"],
            ),
            devices=bluetooth.bind(
                "devices", lambda value: [BluetoothItem(i) for i in value]
            ),
            settings_label="Bluetooth Settings",
            settings_command=user_options.control_apps.bluetooth,
        )


class BluetoothQS(QSButton):
    def __init__(self):
        menu = BluetoothMenu()

        def get_label(devices: list[BluetoothDevice]) -> str:
            if len(devices) == 0:
                return "Bluetooth"
            elif len(devices) == 1:
                return devices[0].alias
            else:
                return f"{len(devices)} pairs"

        def toggle_menu(_):
            bluetooth.setup_mode = True
            menu.toggle()

        super().__init__(
            label=bluetooth.bind("connected_devices", get_label),
            icon_name="bluetooth-active-symbolic",
            on_activate=toggle_menu,
            on_deactivate=toggle_menu,
            active=bluetooth.bind("powered"),
            menu=menu,
        )
        bluetooth.notify("connected_devices")


def bluetooth_control() -> list[QSButton]:
    # return [] if bluetooth.state == "absent" else [BluetoothButton()]
    return [BluetoothQS()]
