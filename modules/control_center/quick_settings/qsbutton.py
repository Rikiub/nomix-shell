from typing import Callable

from gi.repository import GObject  # type: ignore
from ignis.gobject import Binding
from ignis.widgets import Widget

from widgets.menu import Menu


class QSButton(Widget.Button):
    def __init__(
        self,
        label: str | Binding,
        icon_name: str | Binding,
        on_activate: Callable | None = None,
        on_deactivate: Callable | None = None,
        menu: Menu | None = None,
        **kwargs,
    ):
        self.on_activate = on_activate
        self.on_deactivate = on_deactivate
        self._active = False
        self._menu = menu

        super().__init__(
            child=Widget.Box(
                child=[
                    Widget.Icon(image=icon_name),
                    Widget.Label(
                        label=label,
                        ellipsize="end",
                        max_width_chars=15,
                        css_classes=["qs-button-label"],
                    ),
                    Widget.Arrow(
                        halign="end",
                        hexpand=True,
                        pixel_size=20,
                        rotated=menu.bind("reveal_child"),
                    )
                    if menu
                    else None,
                ],
            ),
            css_classes=["qs-button"],
            on_click=self._callback,
            hexpand=True,
            **kwargs,
        )

    def _callback(self, *args) -> None:
        if self.active:
            if self.on_deactivate:
                self.on_deactivate(self)
        else:
            if self.on_activate:
                self.on_activate(self)

    @GObject.Property
    def active(self) -> bool:  # type: ignore
        return self._active

    @active.setter
    def active(self, value: bool) -> None:
        self._active = value
        if value:
            self.add_css_class("active")
        else:
            self.remove_css_class("active")

    @GObject.Property
    def menu(self) -> Menu | None:
        return self._menu
