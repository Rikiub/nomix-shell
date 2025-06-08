from typing import Callable

from gi.repository import Gtk  # type: ignore
from ignis import widgets
from ignis.app import IgnisApp
from ignis.base_widget import BaseWidget
from ignis.variable import Variable

from nomix.utils.types import ALIGN, TRANSITION_TYPE

app = IgnisApp.get_default()
OPENED_POPUP = Variable("")


def is_popup_opened() -> bool:
    return bool([i for i in app.windows if i.popup and i.visible])


class PopupWindow(widgets.RevealerWindow):
    def __init__(
        self,
        namespace: str,
        valign: ALIGN = "start",
        halign: ALIGN = "center",
        vertical: bool = True,
        width_request: int = -1,
        height_request: int = -1,
        transition_type: TRANSITION_TYPE = "crossfade",
        transition_duration: int = 130,
        on_close: Callable | None = None,
        css_classes: list[str] = [],
        child: list[Gtk.Widget | BaseWidget] = [],
        **kwargs,
    ):
        self._on_close = on_close

        self.panel = widgets.Box(
            css_classes=["popup-window", *css_classes],
            width_request=width_request,
            height_request=height_request,
            valign=valign,
            halign=halign,
            vertical=vertical,
            child=child,
            **kwargs,
        )

        overlay = widgets.Overlay(
            child=widgets.EventBox(
                css_classes=["window-backdrop"],
                on_click=lambda _: OPENED_POPUP.set_value(""),
            ),
            overlays=[self.panel],
        )

        revealer = widgets.Revealer(
            transition_type=transition_type,
            transition_duration=transition_duration,
            child=overlay,
        )

        super().__init__(
            css_classes=["transparent"],
            anchor=["top", "bottom", "left", "right"],
            kb_mode="on_demand",
            namespace=namespace,
            popup=True,
            child=revealer,
            revealer=revealer,
            visible=OPENED_POPUP.bind("value", lambda value: value == self.namespace),
        )

        self.connect("notify::visible", lambda *_: self._toggle())

    def _toggle(self):
        if self.visible and self.namespace != OPENED_POPUP.value:
            OPENED_POPUP.value = self.namespace
        elif not self.visible and self._on_close:
            self._on_close()
