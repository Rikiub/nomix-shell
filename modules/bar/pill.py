from ignis.app import IgnisApp
from ignis.options import options
from ignis.services.audio import AudioService
from ignis.services.bluetooth import BluetoothDevice, BluetoothService
from ignis.services.network import Ethernet, NetworkService, Wifi
from ignis.services.upower import UPowerService
from ignis.widgets import Widget

from modules.types import WindowName

__all__ = ["StatusPill"]

app = IgnisApp.get_default()

network = NetworkService.get_default()
bluetooth = BluetoothService.get_default()
audio = AudioService.get_default()
battery = UPowerService.get_default()


class IndicatorIcon(Widget.Icon):
    def __init__(self, **kwargs):
        super().__init__(
            style="margin-right: 0.5rem;", css_classes=["indicator-icon"], **kwargs
        )


class NetworkIndicatorIcon(IndicatorIcon):
    def __init__(
        self, device_type: Ethernet | Wifi, other_device_type: Wifi | Ethernet
    ):
        self._device_type = device_type
        self._other_device_type = other_device_type

        super().__init__(icon_name=device_type.bind("icon-name"))

        for binding in (
            device_type.bind("devices", self._check_visibility),
            other_device_type.bind("is_connected", self._check_visibility),
            device_type.bind("is_connected", self._check_visibility),
        ):
            self.visible = binding  # type: ignore

    def _check_visibility(self, *args) -> bool:
        return len(self._device_type.devices) > 0 and (
            not self._other_device_type.is_connected or self._device_type.is_connected
        )


class WifiIcon(NetworkIndicatorIcon):
    def __init__(self):
        super().__init__(device_type=network.wifi, other_device_type=network.ethernet)


class EthernetIcon(NetworkIndicatorIcon):
    def __init__(self):
        super().__init__(device_type=network.ethernet, other_device_type=network.wifi)


class BluetoothIcon(IndicatorIcon):
    def __init__(self):
        super().__init__(
            image=bluetooth.bind("connected_devices", self._get_image),
            visible=bluetooth.bind("connected_devices", lambda v: bool(v)),
        )
        bluetooth.notify("connected_devices")

    def _get_image(self, devices: list[BluetoothDevice]):
        if devices:
            self.set_image(devices[0].icon_name)


class VpnIcon(IndicatorIcon):
    def __init__(self):
        super().__init__(
            image=network.vpn.bind("icon_name"),
            visible=network.vpn.bind("is_connected"),
        )


class VolumeIcon(IndicatorIcon):
    def __init__(self):
        super().__init__(image=audio.speaker.bind("icon-name"))


class DNDIcon(IndicatorIcon):
    def __init__(self):
        super().__init__(
            image="notification-disabled-symbolic",
            visible=options.notifications.bind("dnd"),
        )

class BatteryIcon(IndicatorIcon):
    def __init__(self):
        super().__init__(
            image=battery.bind("batteries", lambda v: v and v[0].icon_name),
            visible=battery.bind("batteries", lambda v: bool(v)),
        )


class StatusPill(Widget.Button):
    def __init__(self):
        super().__init__(
            child=Widget.Box(
                child=[
                    WifiIcon(),
                    EthernetIcon(),
                    VpnIcon(),
                    BluetoothIcon(),
                    VolumeIcon(),
                    DNDIcon(),
                    BatteryIcon(),
                ]
            ),
            css_classes=["status-pill"],
            on_click=lambda _: app.toggle_window(WindowName.control),
        )
