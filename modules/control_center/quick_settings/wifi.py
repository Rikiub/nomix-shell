from ignis.services.network import NetworkService, WifiAccessPoint, WifiDevice
from ignis.widgets import Widget

from modules.control_center.quick_settings.qsbutton import QSButton
from modules.user_options import user_options
from widgets.menu_devices import DeviceItem, DeviceMenu
from widgets.toggle_box import ToggleBox

network = NetworkService.get_default()


class WifiItem(DeviceItem):
    def __init__(self, access_point: WifiAccessPoint):
        super().__init__(
            label=access_point.ssid,
            icon_name=access_point.bind("strength", lambda _: access_point.icon_name),
            extra_icon_name="lock-symbolic"
            if access_point.security
            else "unlock-symbolic",
            active=access_point.bind("is_connected"),
            on_click=lambda _: self.toggle(access_point),
            extra_widget=Widget.Button(
                tooltip_text="Click to Forget",
                on_click=lambda _: access_point.forget(),
                child=Widget.Icon(image="dialog-password-symbolic"),
                visible=access_point.bind("psk", lambda v: bool(v)),
            ),
        )

    def toggle(self, access_point: WifiAccessPoint):
        if access_point.is_connected:
            access_point.disconnect_from()
        else:
            access_point.connect_to_graphical()


class WifiMenu(DeviceMenu):
    def __init__(self, device: WifiDevice):
        super().__init__(
            name="wifi",
            header=ToggleBox(
                label="Wi-Fi",
                active=network.wifi.enabled,
                on_change=lambda x, state: network.wifi.set_enabled(state),
            ),
            devices=device.bind(
                "access_points",
                transform=lambda value: [WifiItem(i) for i in value],
            ),
            settings_label="Network Settings",
            settings_command=user_options.control_apps.network,
        )


class WifiQS(QSButton):
    def __init__(self, device: WifiDevice):
        menu = WifiMenu(device)

        def toggle_list(x) -> None:
            device.scan()
            menu.toggle()

        super().__init__(
            label=device.ap.bind("ssid", lambda v: v or "Wi-Fi"),
            icon_name=device.ap.bind("icon-name", lambda v: v),
            on_activate=toggle_list,
            on_deactivate=toggle_list,
            active=network.wifi.bind("enabled"),
            menu=menu,
        )


def wifi_control() -> list[QSButton]:
    return [WifiQS(dev) for dev in network.wifi.devices]
