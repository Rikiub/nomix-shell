from __future__ import annotations

from typing import Callable
from ignis.app import IgnisApp
from ignis.base_widget import BaseWidget
from ignis.widgets import Widget

app = IgnisApp.get_default()


class PopupWindow(Widget.Window):
    def __init__(
        self,
        namespace: str,
        overlays: list[BaseWidget] = [],
        on_close: Callable | None = None,
        **kwargs,
    ):
        self._on_close = on_close

        super().__init__(
            namespace=namespace,
            visible=False,
            popup=True,
            kb_mode="on_demand",
            anchor=["top", "bottom", "left", "right"],
            css_classes=["unset"],
            child=Widget.Overlay(
                child=Widget.Button(
                    vexpand=True,
                    hexpand=True,
                    can_focus=False,
                    on_click=lambda _: self.set_visible(False),
                    css_classes=["unset"],
                ),
                overlays=overlays,
            ),
            **kwargs,
        )

        self.connect(
            "notify::visible",
            lambda *_: not self.visible and self._on_close and self._on_close(),
        )
