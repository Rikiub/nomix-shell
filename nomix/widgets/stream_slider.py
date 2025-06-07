from ignis.services.audio import Stream
from ignis import widgets


class StreamSlider(widgets.Scale):
    def __init__(self, stream: Stream, step: int):
        super().__init__(
            min=0,
            max=100,
            step=step,
            value=stream.bind_many(
                ["is_muted", "volume"],
                lambda is_muted, volume: 0 if is_muted else volume or 0,
            ),
            on_change=lambda x: stream.set_volume(x.value),
            sensitive=stream.bind("is_muted", lambda value: not value),
            hexpand=True,
        )


class StreamVolume(widgets.Box):
    def __init__(self, stream: Stream, step: int = 5, muteable: bool = True, **kwargs):
        self.step = step

        super().__init__(
            css_classes=["volume-slider"],
            hexpand=True,
            child=[
                widgets.Button(
                    on_click=lambda _: stream.set_is_muted(not stream.is_muted),
                    tooltip_text=stream.bind_many(
                        ["is_muted", "volume"],
                        lambda is_muted, volume: str(0) + "%" + "\nMuted"
                        if is_muted
                        else str(volume) + "%",
                    ),
                    css_classes=["volume-icon"],
                    child=widgets.Icon(image=stream.bind("icon_name"), pixel_size=24),
                    sensitive=muteable,
                ),
                StreamSlider(stream, step),
            ],
            **kwargs,
        )
