from typing import Callable

from ignis.base_widget import BaseWidget
from ignis.variable import Variable
from ignis.widgets import Widget

from modules.utils import ALIGN

OPENED_POPUP = Variable("")


class PopupWindow(Widget.Window):
    def __init__(
        self,
        namespace: str,
        valign: ALIGN = "start",
        halign: ALIGN = "center",
        on_close: Callable | None = None,
        css_classes: list[str] = [],
        child: list[BaseWidget] = [],
        **kwargs,
    ):
        self._on_close = on_close

        super().__init__(
            style="background-color: transparent;",
            anchor=["top", "bottom", "left", "right"],
            kb_mode="on_demand",
            namespace=namespace,
            popup=True,
            visible=OPENED_POPUP.bind("value", lambda value: value == namespace),
            child=Widget.Overlay(
                child=Widget.Button(
                    css_classes=["window-backdrop"],
                    vexpand=True,
                    hexpand=True,
                    can_focus=False,
                    on_click=lambda _: OPENED_POPUP.set_value(""),
                ),
                overlays=[
                    Widget.Box(
                        css_classes=["popup-window"] + css_classes,
                        valign=valign,
                        halign=halign,
                        vertical=True,
                        child=child,
                    )
                ],
            ),
            **kwargs,
        )

        self.connect(
            "notify::visible",
            lambda *_: self._toggle(),
        )

    def _toggle(self):
        if self.visible:
            OPENED_POPUP.value = self.namespace
        elif self._on_close:
            self._on_close()