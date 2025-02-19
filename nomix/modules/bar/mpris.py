from ignis.services.audio import AudioService
from ignis.services.mpris import MprisPlayer, MprisService
from ignis.widgets import Widget

audio = AudioService.get_default()
mpris = MprisService.get_default()


class Mpris(Widget.Box):
    def __init__(self):
        super().__init__(
            spacing=10,
            setup=lambda self: mpris.connect(
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
            spacing=10,
            setup=lambda self: player.connect(
                "closed",
                lambda _: self.unparent(),  # remove widget when player is closed
            ),
            child=[
                Widget.Icon(image="audio-x-generic-symbolic"),
                Widget.Label(
                    ellipsize="end",
                    max_width_chars=20,
                    label=player.bind("title"),
                ),
            ],
        )
