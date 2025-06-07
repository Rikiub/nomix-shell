from typing import Literal

from ignis.services.audio import AudioService
from ignis import widgets

audio = AudioService.get_default()


class SpeakerVolume(widgets.EventBox):
    def __init__(self, steps: int = 5):
        self.steps = steps

        super().__init__(
            on_scroll_up=lambda self: self.scroll("up"),
            on_scroll_down=lambda self: self.scroll("down"),
            on_click=lambda self: audio.speaker.set_is_muted(
                not audio.speaker.is_muted
            ),
            css_classes=["volume"],
            child=[
                widgets.Button(
                    child=widgets.Box(
                        child=[
                            widgets.Icon(image=audio.speaker.bind("icon_name")),
                            widgets.Label(
                                label=audio.speaker.bind(
                                    "volume", transform=lambda v: str(v)
                                )
                            ),
                        ],
                    )
                )
            ],
        )

    def scroll(self, direction: Literal["up", "down"]):
        volume = audio.speaker.volume

        if direction == "up":
            volume -= self.steps

            if volume < 0:
                volume = 0
        elif direction == "down":
            volume += self.steps

            if volume > 100:
                volume = 100

        audio.speaker.set_volume(volume)
