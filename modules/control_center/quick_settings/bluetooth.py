from ignis.services.bluetooth import BluetoothDevice, BluetoothService

from modules.user_options import user_options
from widgets.menu_devices import DeviceItem, DeviceMenu
from widgets.toggle_box import ToggleBox

from .qsbutton import QSButton

bluetooth = BluetoothService.get_default()


class BluetoothItem(DeviceItem):
    def __init__(self, device: BluetoothDevice):
        super().__init__(
            icon_name=device.bind("icon_name"),
            label=device.alias,
            active=device.bind("connected"),
            on_click=lambda x: device.disconnect_from()
            if device.connected
            else device.connect_to(),
        )


class BluetoothMenu(DeviceMenu):
    def __init__(self):
        super().__init__(
            name="bluetooth",
            header=ToggleBox(
                label="Bluetooth",
                active=bluetooth.bind("powered"),
                on_change=lambda x, state: bluetooth.set_powered(state),
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

        def toggle_menu(x) -> None:
            bluetooth.set_setup_mode(True)
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
