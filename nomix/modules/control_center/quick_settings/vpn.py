from ignis.services.network import NetworkService, VpnConnection
from ignis.widgets import Widget

from nomix.utils.user_options import user_options
from nomix.widgets.menu_devices import DeviceItem, DeviceMenu

from .qsbutton import QSButton

network = NetworkService.get_default()


class VpnItem(DeviceItem):
    def __init__(self, conn: VpnConnection):
        super().__init__(
            on_click=lambda x: conn.toggle_connection(),
            icon_name=conn.name,
            active=conn.bind("is_connected"),
        )


class VpnMenu(DeviceMenu):
    def __init__(self):
        super().__init__(
            name="vpn",
            header=Widget.Box(
                child=[
                    Widget.Icon(icon_name="network-vpn-symbolic", pixel_size=28),
                    Widget.Label(label="VPN connections"),
                ],
            ),
            devices=network.vpn.bind(
                "connections",
                transform=lambda value: [VpnItem(i) for i in value],
            ),
            settings_label="Network Settings",
            settings_command=user_options.control_apps.network,
        )


class VpnQS(QSButton):
    def __init__(self):
        menu = VpnMenu()

        def get_label(id: str) -> str:
            if id:
                return id
            else:
                return "VPN"

        def get_icon(icon_name: str) -> str:
            if network.vpn.is_connected:
                return icon_name
            else:
                return "network-vpn-symbolic"

        super().__init__(
            label=network.vpn.bind("active_vpn_id", get_label),
            icon_name=network.vpn.bind("icon-name", get_icon),
            on_activate=lambda x: menu.toggle(),
            on_deactivate=lambda x: menu.toggle(),
            active=network.vpn.bind("is-connected"),
            menu=menu,
        )


def vpn_control() -> list[QSButton]:
    if len(network.vpn.connections) > 0:
        return [VpnQS()]
    else:
        return []
