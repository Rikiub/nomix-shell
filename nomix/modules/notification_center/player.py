import asyncio

from ignis import utils, widgets
from ignis.services.mpris import MprisPlayer, MprisService

from nomix.utils.helpers import AppInfo

mpris = MprisService.get_default()


class Player(widgets.Revealer):
    PICTURE_SIZE = 60
    TEXT_LIMIT = 50

    def __init__(self, player: MprisPlayer):
        self._player = player
        self._player.connect("closed", lambda *_: self._destroy())

        def play_pause():
            asyncio.create_task(self._player.play_pause_async())

        app_name = ""
        app_icon = ""

        if desktop := AppInfo.from_app_name(player.desktop_entry or ""):
            app_name = desktop.name
            app_icon = desktop.symbolic_icon

        header = widgets.EventBox(
            css_classes=["notification-header"],
            on_click=lambda _: play_pause(),
            child=[
                widgets.Icon(image=app_icon, css_classes=["app-icon"]),
                widgets.Label(label=app_name, css_classes=["app-name"]),
            ],
        )

        picture = widgets.EventBox(
            on_click=lambda _: play_pause(),
            child=[
                widgets.Picture(
                    css_classes=["art"],
                    image=self._player.bind(
                        "art_url", lambda v: v or "emblem-music-symbolic"
                    ),
                    content_fit="contain",
                    width=self.PICTURE_SIZE,
                    height=self.PICTURE_SIZE,
                )
            ],
        )

        metadata = widgets.EventBox(
            css_classes=["metadata"],
            vertical=True,
            hexpand=True,
            on_click=lambda _: play_pause(),
            child=[
                widgets.Label(
                    css_classes=["title"],
                    label=self._player.bind("title"),
                    tooltip_text=self._player.bind("title"),
                    justify="left",
                    ellipsize="end",
                    halign="start",
                    max_width_chars=self.TEXT_LIMIT,
                ),
                widgets.Label(
                    css_classes=["artist"],
                    label=self._player.bind("artist"),
                    tooltip_text=self._player.bind("artist"),
                    justify="left",
                    ellipsize="end",
                    halign="start",
                    max_width_chars=self.TEXT_LIMIT,
                ),
            ],
        )

        controls = widgets.Box(
            css_classes=["controls"],
            valign="start",
            halign="end",
            child=[
                widgets.Button(
                    css_classes=["previous"],
                    on_click=lambda _: asyncio.create_task(
                        self._player.previous_async()
                    ),
                    child=widgets.Icon(image="media-skip-backward-symbolic"),
                ),
                widgets.Button(
                    css_classes=["play-pause"],
                    on_click=lambda _: play_pause(),
                    visible=self._player.bind("can_play"),
                    child=widgets.Icon(
                        image=self._player.bind(
                            "playback_status",
                            lambda value: "media-playback-pause-symbolic"
                            if value == "Playing"
                            else "media-playback-start-symbolic",
                        )
                    ),
                ),
                widgets.Button(
                    css_classes=["next"],
                    on_click=lambda _: asyncio.create_task(self._player.next_async()),
                    visible=self._player.bind("can_go_next"),
                    child=widgets.Icon(image="media-skip-forward-symbolic"),
                ),
            ],
        )

        def str_minutes(seconds: int) -> str:
            if seconds == -1:
                return ""

            minutes = seconds // 60
            remaining_seconds = seconds % 60

            return f"{minutes}:{remaining_seconds:02}"

        progress = widgets.EventBox(
            css_classes=["progress-bar"],
            on_click=lambda _: play_pause(),
            visible=player.bind("position", lambda v: v != -1),
            child=[
                widgets.Label(
                    label=self._player.bind("position", lambda v: str_minutes(v))
                ),
                widgets.Scale(
                    max=self._player.bind("length"),
                    value=self._player.bind("position"),
                    on_change=lambda x: asyncio.create_task(
                        self._player.set_position_async(x.value)
                    ),
                    hexpand=True,
                ),
                widgets.Label(
                    label=self._player.bind("length", lambda v: str_minutes(v)),
                    visible=self._player.bind("length", lambda v: v != -1),
                ),
            ],
        )

        super().__init__(
            transition_type="slide_down",
            reveal_child=self._player.bind("position", lambda v: v != -1),
            child=widgets.Box(
                css_classes=["notification", "player"],
                vertical=True,
                child=[
                    header,
                    widgets.Box(child=[picture, metadata, controls]),
                    progress,
                ],
            ),
        )

    def _destroy(self):
        self.reveal_child = False
        utils.Timeout(self.transition_duration, self.unparent)


class MediaPlayer(widgets.Box):
    def __init__(self, **kwargs):
        super().__init__(
            vertical=True,
            setup=lambda _: mpris.connect(
                "player_added",
                lambda _, player: self.append(Player(player)),
            ),
            **kwargs,
        )
