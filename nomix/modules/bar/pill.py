from typing import Literal

from ignis.app import IgnisApp
from ignis.gobject import Binding
from ignis.options import options
from ignis.services.audio import AudioService
from ignis.services.bluetooth import BluetoothDevice, BluetoothService
from ignis.services.network import Ethernet, NetworkService, Wifi
from ignis.services.upower import UPowerDevice, UPowerService
from ignis.widgets import Widget

from nomix.utils.constants import ModuleWindow
from nomix.utils.options import USER_OPTIONS
from nomix.widgets.actionable_button import ActionableButton

app = IgnisApp.get_default()

network = NetworkService.get_default()
bluetooth = BluetoothService.get_default()
audio = AudioService.get_default()
upower = UPowerService.get_default()


class IndicatorIcon(Widget.Box):
    def __init__(
        self,
        icon_name: str | Binding = "",
        label: str | Binding = "",
        **kwargs,
    ):
        self.label = Widget.Label(label=label)

        super().__init__(
            style="margin-right: 0.5rem;",
            css_classes=["indicator-icon"],
            child=[Widget.Icon(image=icon_name), self.label],
            **kwargs,
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
            self.visible = binding

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
            icon_name=bluetooth.bind("connected_devices", self._get_image),
            visible=bluetooth.bind("connected_devices", lambda v: bool(v)),
        )
        bluetooth.notify("connected_devices")

    def _get_image(self, devices: list[BluetoothDevice]):
        if devices:
            return devices[0].icon_name + "-symbolic"


class VpnIcon(IndicatorIcon):
    def __init__(self):
        super().__init__(
            icon_name=network.vpn.bind("icon_name"),
            visible=network.vpn.bind("is_connected"),
        )


class VolumeIcon(IndicatorIcon):
    def __init__(self):
        super().__init__(icon_name=audio.speaker.bind("icon-name"))


class DNDIcon(IndicatorIcon):
    def __init__(self):
        super().__init__(
            icon_name="notification-disabled-symbolic",
            visible=options.notifications.bind("dnd"),
        )


class BatteryItem(IndicatorIcon):
    def __init__(self, device: UPowerDevice):
        super().__init__(
            icon_name=device.bind("icon_name", lambda v: v + "-symbolic"),
            setup=lambda self: device.connect("removed", lambda _: self.unparent()),
        )

        # Options hot-reload
        def sync():
            if USER_OPTIONS.debug.battery_hidden:
                self.visible = False
            else:
                self.visible = True

            self.label.label = (
                device.bind("percent", lambda v: f"{round(v)}%")
                if USER_OPTIONS.bar.status_pill.battery_percent
                else ""
            )

        sync()

        USER_OPTIONS.bar.status_pill.connect_option(
            "battery_percent", lambda *_: sync()
        )
        USER_OPTIONS.debug.connect_option("battery_hidden", lambda *_: sync())


class BatteriesIcons(Widget.Box):
    def __init__(self):
        super().__init__(
            setup=lambda self: upower.connect(
                "battery-added", lambda _, device: self.append(BatteryItem(device))
            ),
            visible=upower.bind("batteries", lambda v: bool(v)),
        )


class StatusPill(ActionableButton):
    def __init__(self):
        self.volume_steps = 5

        super().__init__(
            css_classes=["status-pill"],
            tooltip_text="Control Center",
            on_scroll_up=lambda _: self._scroll("up"),
            on_scroll_down=lambda _: self._scroll("down"),
            toggle_window=ModuleWindow.CONTROL_CENTER,
            child=Widget.Box(
                child=[
                    WifiIcon(),
                    EthernetIcon(),
                    VpnIcon(),
                    BluetoothIcon(),
                    VolumeIcon(),
                    # DNDIcon(),
                    BatteriesIcons(),
                ]
            ),
        )

    def _scroll(self, direction: Literal["up", "down"]):
        if not audio.speaker.is_muted:
            volume = audio.speaker.volume

            if direction == "up":
                volume -= self.volume_steps

                if volume < 0:
                    volume = 0
            elif direction == "down":
                volume += self.volume_steps

                if volume > 100:
                    volume = 100

            audio.speaker.set_volume(volume)

            app.open_window(ModuleWindow.OSD)
