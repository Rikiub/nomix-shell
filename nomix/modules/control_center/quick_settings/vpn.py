import asyncio

from ignis.services.network import NetworkService, VpnConnection

from nomix.utils.global_options import user_options
from nomix.widgets.header_label import HeaderLabel
from nomix.widgets.menu_devices import DeviceItem, DeviceMenu
from nomix.widgets.qsbutton import QSButton

network = NetworkService.get_default()


class VpnItem(DeviceItem):
    def __init__(self, conn: VpnConnection):
        super().__init__(
            on_click=lambda x: asyncio.create_task(conn.toggle_connection()),
            icon_name=conn.name,
            active=conn.bind("is_connected"),
        )


class VpnMenu(DeviceMenu):
    def __init__(self):
        super().__init__(
            name="vpn",
            header=HeaderLabel(
                icon_name="network-vpn-symbolic",
                label="VPN Connections",
                active=network.vpn.bind("is-connected"),
            ),
            placeholder_text="No VPN connection found",
            devices=network.vpn.bind(
                "connections",
                transform=lambda value: [VpnItem(i) for i in value],
            ),
            settings_label="Network Settings",
            settings_command=user_options.control_apps.network,
        )


class VpnQS(QSButton):
    def __init__(self):
        def get_icon(icon_name: str) -> str:
            if network.vpn.is_connected:
                return icon_name
            else:
                return "network-vpn-symbolic"

        super().__init__(
            title="VPN",
            subtitle=network.vpn.bind("active_vpn_id"),
            icon_name=network.vpn.bind("icon-name", get_icon),
            active=network.vpn.bind("is-connected"),
            menu=VpnMenu(),
        )


def vpn_control() -> list[QSButton]:
    if len(network.vpn.connections) > 0:
        return [VpnQS()]
    else:
        return []
