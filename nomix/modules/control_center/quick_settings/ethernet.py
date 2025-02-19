from ignis.services.network import EthernetDevice, NetworkService

from nomix.utils.user_options import user_options
from nomix.widgets.menu_devices import DeviceItem, DeviceMenu

from .qsbutton import QSButton

network = NetworkService.get_default()


class EthernetItem(DeviceItem):
    def __init__(self, device: EthernetDevice):
        super().__init__(
            icon_name=device.name,
            label=device.bind(
                "is_connected", lambda value: "Disconnect" if value else "Connect"
            ),
            active=device.bind("is_connected"),
            on_click=lambda x: device.disconnect_from()
            if device.is_connected
            else device.connect_to(),
        )


class EthernetMenu(DeviceMenu):
    def __init__(self):
        super().__init__(
            name="ethernet",
            devices=network.ethernet.bind(
                "devices",
                lambda value: [EthernetItem(i) for i in value],
            ),
            settings_label="Network Settings",
            settings_command=user_options.control_apps.network,
        )


class EthernetQS(QSButton):
    def __init__(self):
        menu = EthernetMenu()

        super().__init__(
            label="Wired",
            icon_name="network-wired-symbolic",
            on_activate=lambda x: menu.toggle(),
            on_deactivate=lambda x: menu.toggle(),
            menu=menu,
            active=network.ethernet.bind("is_connected"),
        )


def ethernet_control() -> list[QSButton]:
    if len(network.ethernet.devices) > 0:
        return [EthernetQS()]
    else:
        return []
