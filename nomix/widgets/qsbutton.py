from typing import Callable

from ignis.gobject import Binding, IgnisProperty
from ignis.widgets import Widget

from nomix.widgets.menu import Menu


class QSButton(Widget.Box):
    def __init__(
        self,
        title: str | Binding | None = None,
        subtitle: str | Binding | None = None,
        icon_name: str | Binding | None = None,
        on_activate: Callable | None = None,
        on_deactivate: Callable | None = None,
        menu: Menu | None = None,
        **kwargs,
    ):
        self.on_activate = on_activate
        self.on_deactivate = on_deactivate
        self._active = False
        self._menu = menu

        self._subtitle = Widget.Label(
            label=subtitle,
            halign="start",
            ellipsize="end",
            max_width_chars=15,
            css_classes=["qs-button-subtitle"],
        )
        self._subtitle.connect(
            "notify::label",
            lambda *_: self._subtitle.set_visible(bool(self._subtitle.label)),
        )
        self._subtitle.notify("label")

        def on_click_arrow():
            if self._arrow.rotated:
                self._button_arrow.add_css_class("hover")
            else:
                self._button_arrow.remove_css_class("hover")

        self._arrow = Widget.Arrow(
            pixel_size=20, rotated=menu and menu.bind("reveal_child")
        )
        self._arrow.connect("notify::rotated", lambda *_: on_click_arrow())

        self._button_arrow = Widget.Button(
            on_click=lambda _: menu and menu.toggle(),
            css_classes=["qs-button-menu"],
            child=self._arrow,
        )

        super().__init__(
            child=[
                Widget.Button(
                    on_click=self._callback,
                    css_classes=["qs-button-text"],
                    hexpand=True,
                    child=Widget.Box(
                        child=[
                            Widget.Icon(image=icon_name, style="margin: 0 7px;")
                            if icon_name
                            else None,
                            Widget.Box(
                                vertical=True,
                                valign="center",
                                halign="start",
                                css_classes=["qs-button-title"],
                                child=[
                                    Widget.Label(
                                        label=title, halign="start", ellipsize="end"
                                    )
                                    if title
                                    else None,
                                    self._subtitle,
                                ],
                            ),
                        ],
                    ),
                ),
                Widget.Separator() if menu else None,
                self._button_arrow if menu else None,
            ],
            css_classes=["qs-box"],
            **kwargs,
        )

        if menu:
            self.add_css_class("has-menu")

    def _callback(self, *_) -> None:
        if self.active:
            if self.on_deactivate:
                self.on_deactivate(self)
        else:
            if self.on_activate:
                self.on_activate(self)

    @IgnisProperty
    def active(self) -> bool:  # type: ignore
        return self._active

    @active.setter
    def active(self, value: bool) -> None:
        self._active = value

        if value:
            self.add_css_class("active")
        else:
            self.remove_css_class("active")

    @IgnisProperty
    def menu(self) -> Menu | None:
        return self._menu
