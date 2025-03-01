import asyncio

from ignis.services.network import EthernetDevice, NetworkService

from nomix.utils.global_options import cache_options
from nomix.widgets.header_label import HeaderLabel
from nomix.utils.global_options import user_options
from nomix.widgets.menu_devices import DeviceItem, DeviceMenu
from nomix.widgets.qsbutton import QSButton

network = NetworkService.get_default()


class EthernetItem(DeviceItem):
    def __init__(self, device: EthernetDevice):
        def active_and_save():
            cache_options.last_ethernet = device.name
            return device.is_connected

        super().__init__(
            label=device.name,
            icon_name=device.bind(
                "is_connected",
                lambda i: "network-wired-symbolic"
                if i
                else "network-wired-disconnected-symbolic",
            ),
            active=device.bind("is_connected", lambda _: active_and_save()),
            on_click=lambda _: asyncio.create_task(device.disconnect_from())
            if device.is_connected
            else asyncio.create_task(device.connect_to()),
        )


class EthernetMenu(DeviceMenu):
    def __init__(self):
        super().__init__(
            name="ethernet",
            header=HeaderLabel(
                icon_name="network-wired-symbolic",
                label="Wired",
                active=network.ethernet.bind("is_connected"),
            ),
            devices=network.ethernet.bind(
                "devices",
                lambda value: [EthernetItem(i) for i in value],
            ),
            settings_label="Network Settings",
            settings_command=user_options.control_apps.network,
        )


class EthernetQS(QSButton):
    def __init__(self):
        def get_last_wired() -> EthernetDevice | None:
            for n in network.ethernet.devices:
                if n.name == cache_options.last_ethernet:
                    return n

        def get_connected() -> EthernetDevice | None:
            for n in network.ethernet.devices:
                if n.is_connected:
                    return n

        def on_activate():
            if self._last_wired:
                asyncio.create_task(self._last_wired.connect_to())

        def on_deactivate():
            if wired := get_connected():
                self._last_wired = wired
                asyncio.create_task(wired.disconnect_from())

        def subtitle():
            if wired := get_connected():
                return wired.name
            else:
                return None

        self._last_wired = get_last_wired()

        super().__init__(
            title="Wired",
            subtitle=network.ethernet.bind("is_connected", lambda _: subtitle()),
            icon_name=network.ethernet.bind("icon_name"),
            active=network.ethernet.bind("is_connected"),
            on_activate=lambda _: on_activate(),
            on_deactivate=lambda _: on_deactivate(),
            menu=EthernetMenu(),
        )


def ethernet_control() -> list[QSButton]:
    if len(network.ethernet.devices) > 0:
        return [EthernetQS()]
    else:
        return []
