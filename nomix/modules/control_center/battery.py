from nomix.utils.global_options import user_options

from ignis.services.upower import UPowerDevice, UPowerService
from ignis.widgets import Widget

upower = UPowerService.get_default()


class BatteryItem(Widget.Box):
    def __init__(self, device: UPowerDevice):
        super().__init__(
            css_classes=["battery-item"],
            setup=lambda self: device.connect("removed", lambda _: self.unparent()),
            child=[
                Widget.Icon(image=device.bind("icon-name")),
                Widget.Label(
                    label=device.bind("percent", lambda v: str(round(v)) + "%"),
                    style="margin: 0 3px;",
                ),
            ],
        )


class BatteryStatus(Widget.Box):
    def __init__(self, **kwargs):
        super().__init__(
            css_classes=["battery-status"],
            setup=lambda self: upower.connect(
                "battery-added", lambda _, device: self.append(BatteryItem(device))
            ),
            visible=upower.bind(
                "batteries", lambda v: not user_options.debug.battery_hidden and bool(v)
            ),
            **kwargs,
        )
