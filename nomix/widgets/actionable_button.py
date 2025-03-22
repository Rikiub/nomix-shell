from typing import Callable

from ignis.app import IgnisApp
from ignis.base_widget import BaseWidget
from ignis.gobject import Binding
from ignis.widgets import Widget

from nomix.utils.constants import ModuleWindow
from nomix.widgets.popup_window import is_popup_opened

app = IgnisApp.get_default()


class ActionableButton(Widget.EventBox):
    def __init__(
        self,
        on_click: Callable | None = None,
        on_hover: Callable | None = None,
        on_hover_lost: Callable | None = None,
        toggle_window: ModuleWindow | None = None,
        css_classes: list[str] = [],
        child: Binding | BaseWidget | None = None,
        **kwargs,
    ):
        self.__on_click = on_click
        self.__on_hover = on_hover
        self.__on_hover_lost = on_hover_lost
        self.__toggle_window = toggle_window

        self._button = Widget.Button(css_classes=css_classes, child=child)

        super().__init__(
            on_click=lambda v: self._proxy_on_click(v),
            on_hover=lambda v: self._proxy_on_hover(v),
            on_hover_lost=lambda v: self._proxy_on_hover_lost(v),
            child=[self._button],
            **kwargs,
        )

        if toggle_window:
            self._window = app.get_window(toggle_window)
            self._window.connect("notify::visible", lambda *_: self._toggle_active())

    def _proxy_on_click(self, value):
        if self.__on_click:
            self.__on_click(value)

        if self.__toggle_window:
            app.toggle_window(self.__toggle_window)

    def _proxy_on_hover(self, value):
        self._button.add_css_class("hover")

        if self.__on_hover:
            self.__on_hover(value)

        if self.__toggle_window and is_popup_opened():
            app.open_window(self.__toggle_window)

    def _proxy_on_hover_lost(self, value):
        self._button.remove_css_class("hover")

        if self.__on_hover_lost:
            self.__on_hover_lost(value)

    def _toggle_active(self):
        if self._window.is_visible():
            self._button.add_css_class("active")
        else:
            self._button.remove_css_class("active")
