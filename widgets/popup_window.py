from typing import Callable

from ignis.base_widget import BaseWidget
from ignis.widgets import Widget

from modules.types import ALIGN

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
            namespace=namespace,
            visible=False,
            popup=True,
            kb_mode="on_demand",
            anchor=["top", "bottom", "left", "right"],
            css_classes=["window-backdrop"],
            child=Widget.Overlay(
                child=Widget.Button(
                    vexpand=True,
                    hexpand=True,
                    can_focus=False,
                    on_click=lambda _: self.set_visible(False),
                    css_classes=["window-backdrop"],
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
            lambda *_: self._exit(),
        )

    def _exit(self):
        if not self.visible and self._on_close:
            self._on_close()
