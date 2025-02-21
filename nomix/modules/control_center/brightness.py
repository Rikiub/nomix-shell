from ignis.services.backlight import BacklightService
from ignis.widgets import Widget

backlight = BacklightService.get_default()


class BacklightSlider(Widget.Scale):
    def __init__(self, step: int = 5):
        super().__init__(
            min=0,
            max=backlight.max_brightness,
            step=step,
            value=backlight.bind("brightness"),
            on_change=lambda x: backlight.set_brightness(x.value),
            hexpand=True,
        )


class Brightness(Widget.Box):
    def __init__(self, step: int = 1, **kwargs):
        self.step = step

        super().__init__(
            css_classes=["volume-slider"],
            style="padding: 0 16px;",
            visible=backlight.bind("available"),
            child=[
                Widget.Box(
                    css_classes=["volume-icon"],
                    child=[
                        Widget.Icon(
                            image="display-brightness-symbolic",
                            pixel_size=20,
                        )
                    ],
                ),
                BacklightSlider(step),
            ],
            **kwargs,
        )
