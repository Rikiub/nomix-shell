import asyncio

from ignis.services.mpris import MprisPlayer, MprisService
from ignis.utils import Utils
from ignis.widgets import Widget

from nomix.utils.helpers import AppInfo

mpris = MprisService.get_default()


class Player(Widget.Revealer):
    def __init__(self, player: MprisPlayer):
        self._player = player
        self._player.connect("closed", lambda *_: self._destroy())

        app_name = ""
        app_icon = ""

        if desktop := AppInfo.from_app_name(player.desktop_entry or ""):
            app_name = desktop.name
            app_icon = desktop.symbolic_icon

        def play_pause():
            asyncio.create_task(self._player.play_pause_async())

        header = Widget.EventBox(
            css_classes=["notification-header"],
            on_click=lambda _: play_pause(),
            child=[
                Widget.Icon(image=app_icon, css_classes=["app-icon"]),
                Widget.Label(label=app_name, css_classes=["app-name"]),
            ],
        )

        picture_size = 50
        picture = Widget.EventBox(
            on_click=lambda _: play_pause(),
            child=[
                Widget.Picture(
                    image=self._player.bind(
                        "art_url", lambda v: v or "emblem-music-symbolic"
                    ),
                    width=picture_size,
                    height=picture_size,
                    content_fit="contain",
                    css_classes=["art"],
                )
            ],
        )

        text_limit = 50
        metadata = Widget.EventBox(
            vertical=True,
            hexpand=True,
            on_click=lambda _: play_pause(),
            css_classes=["metadata"],
            child=[
                Widget.Label(
                    label=self._player.bind("title"),
                    tooltip_text=self._player.bind("title"),
                    justify="left",
                    ellipsize="end",
                    max_width_chars=text_limit,
                    css_classes=["label-title"],
                    halign="start",
                ),
                Widget.Label(
                    label=self._player.bind("artist"),
                    tooltip_text=self._player.bind("artist"),
                    justify="left",
                    ellipsize="end",
                    max_width_chars=text_limit,
                    css_classes=["label-artist"],
                    halign="start",
                ),
            ],
        )

        controls = Widget.Box(
            valign="start",
            halign="end",
            hexpand=True,
            css_classes=["controls"],
            child=[
                Widget.Button(
                    css_classes=["action-button"],
                    on_click=lambda _: asyncio.create_task(
                        self._player.previous_async()
                    ),
                    child=Widget.Icon(image="media-skip-backward-symbolic"),
                ),
                Widget.Button(
                    css_classes=["action-button"],
                    on_click=lambda _: play_pause(),
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
                    css_classes=["action-button"],
                    on_click=lambda _: asyncio.create_task(self._player.next_async()),
                    visible=self._player.bind("can_go_next"),
                    child=Widget.Icon(image="media-skip-forward-symbolic"),
                ),
            ],
        )

        def str_minutes(seconds: int) -> str:
            if seconds == -1:
                return ""

            minutes = seconds // 60
            remaining_seconds = seconds % 60

            return f"{minutes}:{remaining_seconds:02}"

        progress = Widget.EventBox(
            css_classes=["progress-bar"],
            on_click=lambda _: play_pause(),
            visible=player.bind("position", lambda v: v != -1),
            child=[
                Widget.Label(
                    label=self._player.bind("position", lambda v: str_minutes(v))
                ),
                Widget.Scale(
                    max=self._player.bind("length"),
                    value=self._player.bind("position"),
                    on_change=lambda x: asyncio.create_task(
                        self._player.set_position_async(x.value)
                    ),
                    hexpand=True,
                ),
                Widget.Label(
                    label=self._player.bind("length", lambda v: str_minutes(v)),
                    visible=self._player.bind("length", lambda v: v != -1),
                ),
            ],
        )

        super().__init__(
            transition_type="slide_down",
            reveal_child=self._player.bind("position", lambda v: v != -1),
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
        Utils.Timeout(self.transition_duration, self.unparent)


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
