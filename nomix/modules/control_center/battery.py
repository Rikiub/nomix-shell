from ignis import widgets
from ignis.services.upower import UPowerDevice, UPowerService

from nomix.utils.options import USER_OPTIONS

upower = UPowerService.get_default()


class BatteryItem(widgets.Box):
    def __init__(self, device: UPowerDevice):
        super().__init__(
            css_classes=["battery-item"],
            setup=lambda self: device.connect("removed", lambda _: self.unparent()),
            child=[
                widgets.Icon(image=device.bind("icon-name")),
                widgets.Label(
                    label=device.bind("percent", lambda v: str(round(v)) + "%")
                ),
            ],
        )


class BatteryStatus(widgets.Box):
    def __init__(self, **kwargs):
        super().__init__(
            css_classes=["battery-status"],
            setup=lambda self: upower.connect(
                "battery-added", lambda _, device: self.append(BatteryItem(device))
            ),
            **kwargs,
        )

        def toggle_visible():
            if USER_OPTIONS.debug.battery_hidden:
                self.visible = False
            else:
                self.visible = upower.bind("batteries", lambda v: bool(v))

        toggle_visible()
        USER_OPTIONS.debug.connect_option("battery_hidden", lambda *_: toggle_visible())
