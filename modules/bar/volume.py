from typing import Literal

from ignis.services.audio import AudioService
from ignis.widgets import Widget

audio = AudioService.get_default()


class SpeakerVolume(Widget.EventBox):
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
                Widget.Button(
                    child=Widget.Box(
                        child=[
                            Widget.Icon(
                                image=audio.speaker.bind("icon_name"),
                                style="margin-right: 5px;",
                            ),
                            Widget.Label(
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
