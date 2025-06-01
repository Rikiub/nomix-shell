from ignis.services.audio import AudioService
from ignis.services.mpris import MprisPlayer, MprisService
from ignis.widgets import Widget

audio = AudioService.get_default()
mpris = MprisService.get_default()


class Mpris(Widget.Label):
    def __init__(self):
        super().__init__(
            setup=lambda _: mpris.connect(
                "player-added", lambda _, player: self.append(self.mpris_title(player))
            ),
            child=[
                Widget.Label(
                    # label="No media players",
                    visible=mpris.bind("players", lambda value: value != 0),
                )
            ],
        )

    def mpris_title(self, player: MprisPlayer) -> Widget.Box:
        return Widget.Box(
            setup=lambda self: player.connect(
                "closed",
                lambda _: self.unparent(),
            ),
            child=[
                Widget.Icon(image="audio-x-generic-symbolic"),
                Widget.Label(
                    label=player.bind("title"),
                    max_width_chars=20,
                    ellipsize="end",
                ),
            ],
        )
