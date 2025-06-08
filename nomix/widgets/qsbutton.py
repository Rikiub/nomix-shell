from typing import Callable

from ignis import widgets
from ignis.gobject import Binding, IgnisProperty

from nomix.widgets.menu import Menu


class QSButton(widgets.Box):
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

        self._subtitle = widgets.Label(
            label=subtitle,
            halign="start",
            ellipsize="end",
            max_width_chars=13,
            css_classes=["subtitle"],
        )
        self._subtitle.connect(
            "notify::label",
            lambda *_: self._subtitle.set_visible(bool(self._subtitle.label)),
        )
        self._subtitle.notify("label")

        super().__init__(
            css_classes=["qs-button"],
            child=[
                widgets.Button(
                    css_classes=["sections"],
                    hexpand=True,
                    on_click=self._callback,
                    child=widgets.Box(
                        child=[
                            widgets.Icon(image=icon_name, css_classes=["icon"])
                            if icon_name
                            else None,
                            widgets.Box(
                                vertical=True,
                                valign="center",
                                halign="start",
                                css_classes=["title"],
                                child=[
                                    widgets.Label(
                                        label=title,
                                        halign="start",
                                        ellipsize="end",
                                    )
                                    if title
                                    else None,
                                    self._subtitle,
                                ],
                            ),
                        ],
                    ),
                ),
                widgets.Separator() if menu else None,
                widgets.Button(
                    css_classes=["menu"],
                    on_click=lambda _: menu and menu.toggle(),
                    child=widgets.Arrow(
                        pixel_size=20, rotated=menu and menu.bind("reveal_child")
                    ),
                )
                if menu
                else None,
            ],
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
