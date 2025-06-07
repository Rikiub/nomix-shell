import datetime
from typing import Callable, Generic, TypeVar

from ignis import utils, widgets
from ignis.gobject import IgnisProperty
from ignis.services.notifications import Notification

T = TypeVar("T")


class Placeholder(Generic[T], widgets.EventBox):
    def __init__(self, item: T | None = None, **kwargs):
        super().__init__(**kwargs)

        self.item = item

        if item:
            self.update(item)

    def update(self, item: T) -> None:
        self.item = item


class Header(Placeholder):
    def __init__(self):
        self.app_icon = widgets.Icon(css_classes=["app-icon"], pixel_size=15)
        self.app_name = widgets.Label(css_classes=["app-name"], halign="start")
        self.time = widgets.Label(css_classes=["time"])

        self.button_arrow = widgets.Button(
            child=widgets.Arrow(
                direction="down",
                degree=180,
                pixel_size=24,
            )
        )

        super().__init__(
            css_classes=["notification-header"],
            child=[
                widgets.EventBox(
                    hexpand=True,
                    on_click=lambda _: self.item and self.item.close(),
                    child=[self.app_icon, self.app_name, self.time],
                ),
                widgets.Box(
                    halign="end",
                    hexpand=True,
                    child=[
                        self.button_arrow,
                        widgets.Button(
                            child=widgets.Icon(
                                image="window-close-symbolic",
                                pixel_size=24,
                            ),
                            on_click=lambda _: self.item and self.item.close(),
                        ),
                    ],
                ),
            ],
        )

    def update(self, item: Notification):
        self.item = item

        self.app_icon.image = item.icon or "" + "-symbolic"
        self.app_icon.visible = bool(item.icon)

        self.app_name.label = item.app_name
        self.app_name.visible = bool(item.app_name)

        self.time.label = utils.Poll(
            1000,
            lambda _: self._format_time(item.time),
        ).bind("output")

    def _format_time(self, time: int) -> str:
        days, hours, minutes = self._extract_date(time)

        if days:
            return f"{days} days ago"
        elif hours:
            return f"{hours} hours ago"
        elif minutes:
            return f"{minutes} minutes ago"
        else:
            return "Just now"

    def _extract_date(self, timestamp: float) -> tuple[int, int, int]:
        current = datetime.datetime.now()
        past = datetime.datetime.fromtimestamp(timestamp)
        delta = current - past

        hours, remainder = divmod(delta.total_seconds(), 3600)

        hours = round(hours)
        minutes = round(remainder // 60)

        return delta.days, hours, minutes


class Content(Placeholder):
    def __init__(self):
        self.icon = widgets.Icon(
            css_classes=["icon"],
            pixel_size=50,
            halign="start",
            valign="start",
        )

        self.summary = widgets.Label(
            css_classes=["summary"],
            ellipsize="end",
            halign="start",
        )
        self.body = widgets.Label(
            css_classes=["body"],
            use_markup=True,
            ellipsize="end",
            halign="start",
            wrap="word",
            justify="left",
        )

        super().__init__(
            css_classes=["information"],
            on_click=lambda _: self.item and self.item.close(),
            child=[
                self.icon,
                widgets.Box(
                    vertical=True,
                    hexpand=True,
                    child=[self.summary, self.body],
                ),
            ],
        )

    def update(self, item: Notification):
        self.item = item

        self.icon.image = item.icon
        self.icon.visible = bool(item.icon)

        self.summary.label = item.summary
        self.summary.visible = bool(item.summary)

        self.body.label = item.body
        self.body.visible = bool(item.body)

    def toggle_body(self, value: bool | None = None):
        if value:
            self._expand_body(value)
            return

        if self.body.get_ellipsize() == "none":
            self._expand_body(False)
        else:
            self._expand_body(True)

    def _expand_body(self, value: bool):
        if value:
            self.body.set_ellipsize("none")  # type: ignore
        else:
            self.body.set_ellipsize("end")  # type: ignore


class Action(Placeholder):
    def __init__(self):
        super().__init__(css_classes=["actions"], homogeneous=True)

    def update(self, item: Notification):
        self.item = item

        self.child = [
            widgets.Button(
                on_click=lambda _, action=action: action.invoke(),
                child=widgets.Label(label=action.label),
            )
            for action in item.actions
        ]


class NotificationWidget(widgets.EventBox):
    def __init__(
        self,
        notification: Notification | None = None,
        on_close: Callable | None = None,
        expand_on_hover: bool = False,
        css_classes: list[str] = [],
    ):
        self._on_close = on_close

        self.header = Header()
        self.content = Content()
        self.action = Action()

        super().__init__(
            css_classes=["notification", *css_classes],
            vertical=True,
            hexpand=True,
            on_hover=lambda _: expand_on_hover and self.content.toggle_body(True),
            on_hover_lost=lambda _: expand_on_hover and self.toggle_body(False),
            child=[self.header, self.content, self.action],
        )

        if notification:
            self.update(notification)

    @IgnisProperty
    def on_close(self) -> Callable | None:  # type: ignore
        return self._on_close

    @on_close.setter
    def on_close(self, callback: Callable):
        self._on_close = callback

    def update(self, notify: Notification):
        for widget in self.child:
            widget.update(notify)

        self.header.button_arrow.on_click = lambda _: self.content.toggle_body()
        self.header.button_arrow.rotated = self.content.body.bind(
            "ellipsize",
            lambda v: True if v == "none" else False,
        )

        notify.connect(
            "closed",
            lambda *_: self.on_close and self.on_close(),
        )
