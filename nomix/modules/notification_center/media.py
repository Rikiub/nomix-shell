from ignis.services.mpris import MprisPlayer, MprisService
from ignis.utils import Utils
from ignis.widgets import Widget

mpris = MprisService.get_default()


def _parse_app_name(entry: str) -> str:
    # Format flatpak apps name
    parts = entry.split(".")

    if len(parts) >= 2:
        entry = parts[-1]

    # Else return direct entry
    return entry.capitalize()


class Player(Widget.Revealer):
    def __init__(self, player: MprisPlayer):
        self._player = player
        self._player.connect("closed", lambda _: self._destroy())

        header = Widget.EventBox(
            css_classes=["notification-header"],
            on_click=lambda _: self._player.play_pause(),
            child=[
                Widget.Label(
                    css_classes=["notification-app-name"],
                    label=self._player.bind("desktop_entry", _parse_app_name),
                )
            ],
        )

        picture_size = 50
        picture = Widget.EventBox(
            on_click=lambda _: self._player.play_pause(),
            child=[
                Widget.Picture(
                    image=self._player.bind("art_url"),
                    width=picture_size,
                    height=picture_size,
                    content_fit="contain",
                    css_classes=["player-image"],
                )
            ],
        )

        text_limit = 50
        metadata = Widget.EventBox(
            vertical=True,
            hexpand=True,
            on_click=lambda _: self._player.play_pause(),
            css_classes=["player-metadata"],
            child=[
                Widget.Label(
                    label=self._player.bind("title"),
                    tooltip_text=self._player.bind("title"),
                    justify="left",
                    ellipsize="end",
                    max_width_chars=text_limit,
                    css_classes=["player-title"],
                    halign="start",
                ),
                Widget.Label(
                    label=self._player.bind("artist"),
                    tooltip_text=self._player.bind("artist"),
                    justify="left",
                    ellipsize="end",
                    max_width_chars=text_limit,
                    css_classes=["player-artist"],
                    halign="start",
                ),
            ],
        )

        controls = Widget.Box(
            valign="start",
            halign="end",
            hexpand=True,
            css_classes=["player-controls"],
            child=[
                Widget.Button(
                    css_classes=["notification-action"],
                    on_click=lambda _: self._player.previous(),
                    child=Widget.Icon(image="media-skip-backward-symbolic"),
                ),
                Widget.Button(
                    css_classes=["notification-action"],
                    on_click=lambda _: self._player.play_pause(),
                    visible=self._player.bind("can_play"),
                    child=Widget.Icon(
                        image=self._player.bind(
                            "playback_status",
                            lambda value: "media-playback-pause-symbolic"
                            if value == "Playing"
                            else "media-playback-start-symbolic",
                        )
                    ),
                ),
                Widget.Button(
                    css_classes=["notification-action"],
                    on_click=lambda _: self._player.next(),
                    visible=self._player.bind("can_go_next"),
                    child=Widget.Icon(image="media-skip-forward-symbolic"),
                ),
            ],
        )

        def minutes(seconds: int) -> str:
            minutes = seconds // 60
            remaining_seconds = seconds % 60
            return f"{minutes}:{remaining_seconds:02}"

        progress = Widget.EventBox(
            css_classes=["player-progress"],
            on_click=lambda _: self._player.play_pause(),
            visible=player.bind("position", lambda value: value != -1),
            child=[
                Widget.Label(label=self._player.bind("position", lambda v: minutes(v))),
                Widget.Scale(
                    max=self._player.bind("length"),
                    value=self._player.bind("position"),
                    on_change=lambda x: self._player.set_position(x.value),
                    hexpand=True,
                ),
                Widget.Label(label=self._player.bind("length", lambda v: minutes(v))),
            ],
        )

        super().__init__(
            transition_type="slide_down",
            reveal_child=False,
            child=Widget.Box(
                css_classes=["notification", "player"],
                vertical=True,
                child=[
                    header,
                    Widget.Box(child=[picture, metadata, controls]),
                    progress,
                ],
            ),
        )

    def _destroy(self):
        self.reveal_child = False
        Utils.Timeout(self.transition_duration, super().unparent)


class MediaPlayer(Widget.Box):
    def __init__(self, **kwargs):
        super().__init__(
            vertical=True,
            setup=lambda _: mpris.connect(
                "player_added", lambda _, player: self._add_player(player)
            ),
            **kwargs,
        )

    def _add_player(self, player: MprisPlayer):
        media = Player(player)
        self.append(media)
        media.reveal_child = True
