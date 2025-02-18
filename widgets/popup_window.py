from typing import Callable

from ignis.base_widget import BaseWidget
from ignis.variable import Variable
from ignis.widgets import Widget

from utils.types import ALIGN, TRANSITION_TYPE

OPENED_POPUP = Variable("")


class PopupWindow(Widget.RevealerWindow):
    def __init__(
        self,
        namespace: str,
        valign: ALIGN = "start",
        halign: ALIGN = "center",
        width_request: int = -1,
        height_request: int = -1,
        transition_type: TRANSITION_TYPE = "crossfade",
        transition_duration: int = 130,
        on_close: Callable | None = None,
        css_classes: list[str] = [],
        child: list[BaseWidget] = [],
        **kwargs,
    ):
        self._on_close = on_close

        panel = Widget.Box(
            css_classes=["popup-window"] + css_classes,
            width_request=width_request,
            height_request=height_request,
            valign=valign,
            halign=halign,
            vertical=True,
            child=child,
        )

        overlay = Widget.Overlay(
            child=Widget.EventBox(
                css_classes=["window-backdrop"],
                on_click=lambda _: OPENED_POPUP.set_value(""),
            ),
            overlays=[panel],
        )

        revealer = Widget.Revealer(
            transition_type=transition_type,
            transition_duration=transition_duration,
            child=overlay,
        )

        super().__init__(
            style="background-color: transparent;",
            anchor=["top", "bottom", "left", "right"],
            kb_mode="on_demand",
            namespace=namespace,
            popup=True,
            visible=OPENED_POPUP.bind("value", lambda value: value == self.namespace),
            child=revealer,
            revealer=revealer,
            **kwargs,
        )

        self.connect("notify::visible", lambda *_: self._toggle())

    def _toggle(self):
        if self.visible and self.namespace != OPENED_POPUP.value:
            OPENED_POPUP.value = self.namespace
        elif self._on_close:
            self._on_close()