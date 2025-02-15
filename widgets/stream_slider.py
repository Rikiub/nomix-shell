from ignis.services.audio import Stream
from ignis.widgets import Widget


class StreamSlider(Widget.Scale):
    def __init__(self, stream: Stream, step):
        super().__init__(
            min=0,
            max=100,
            step=step,
            value=stream.bind_many(
                ["is_muted", "volume"],
                lambda is_muted, volume: 0 if is_muted else volume,
            ),
            on_change=lambda x: stream.set_volume(x.value),
            sensitive=stream.bind("is_muted", lambda value: not value),
            hexpand=True,
        )


class StreamVolume(Widget.Box):
    def __init__(self, stream: Stream, step: int = 5, **kwargs):
        self.step = step

        super().__init__(
            css_classes=["volume-slider"],
            hexpand=True,
            child=[
                Widget.Button(
                    on_click=lambda self: stream.set_is_muted(not stream.is_muted),
                    child=Widget.Box(
                        child=[
                            Widget.Icon(
                                image=stream.bind("icon_name"),
                                pixel_size=20,
                            ),
                        ],
                    ),
                ),
                StreamSlider(stream, step),
            ],
            **kwargs,
        )
