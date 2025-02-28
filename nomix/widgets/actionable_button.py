from typing import Callable
from ignis.app import IgnisApp
from ignis.base_widget import BaseWidget
from ignis.gobject import Binding
from ignis.widgets import Widget

from nomix.utils.constants import ModuleWindow

app = IgnisApp.get_default()


class ActionableButton(Widget.EventBox):
    def __init__(
        self,
        on_click: Callable | None = None,
        toggle_window: ModuleWindow | None = None,
        css_classes: list[str] = [],
        child: Binding | BaseWidget | None = None,
        **kwargs,
    ):
        self.__on_click = on_click
        self.__toggle_window = toggle_window

        self._button = Widget.Button(css_classes=css_classes, child=child)

        super().__init__(
            on_click=lambda v: self._callback(v), child=[self._button], **kwargs
        )

        if toggle_window:
            self._window = app.get_window(toggle_window)
            self._window.connect("notify::visible", lambda *_: self._toggle_active())

    def _callback(self, value):
        if self.__on_click:
            self.__on_click(value)

        if self.__toggle_window:
            app.toggle_window(self.__toggle_window)

    def _toggle_active(self):
        if self._window.is_visible():
            self._button.add_css_class("active")
        else:
            self._button.remove_css_class("active")
