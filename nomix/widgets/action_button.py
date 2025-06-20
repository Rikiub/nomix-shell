from typing import Callable

from ignis import widgets
from ignis.base_widget import BaseWidget
from ignis.gobject import Binding
from ignis.window_manager import WindowManager

from nomix.utils.constants import ModuleWindow
from nomix.widgets.popup_window import is_popup_opened

windows = WindowManager.get_default()


class ActionButton(widgets.EventBox):
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

        self._button = widgets.Button(
            on_click=lambda v: self._proxy_on_click(v),
            css_classes=["action-button", *css_classes],
            child=child,
        )

        super().__init__(
            on_click=lambda v: self._proxy_on_click(v),
            on_hover=lambda v: self._proxy_on_hover(v),
            on_hover_lost=lambda v: self._proxy_on_hover_lost(v),
            child=[self._button],
            **kwargs,
        )

        if toggle_window:
            windows.get_window(toggle_window).connect(
                "notify::visible",
                lambda *_: self._toggle_active(),
            )

    def _proxy_on_click(self, value):
        if self.__on_click:
            self.__on_click(value)

        if self.__toggle_window:
            windows.toggle_window(self.__toggle_window)

    def _proxy_on_hover(self, value):
        self._button.add_css_class("hover")

        if self.__on_hover:
            self.__on_hover(value)

        if self.__toggle_window and is_popup_opened():
            windows.open_window(self.__toggle_window)

    def _proxy_on_hover_lost(self, value):
        self._button.remove_css_class("hover")

        if self.__on_hover_lost:
            self.__on_hover_lost(value)

    def _toggle_active(self):
        if (
            self.__toggle_window
            and windows.get_window(self.__toggle_window).is_visible()
        ):
            self._button.add_css_class("active")
        else:
            self._button.remove_css_class("active")
