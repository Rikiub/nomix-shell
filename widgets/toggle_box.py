from typing import Callable

from ignis.gobject import Binding
from ignis.widgets import Widget


class ToggleBox(Widget.Box):
    def __init__(
        self,
        label: str | Binding,
        active: bool | Binding,
        on_change: Callable,
        css_classes: list[str] = [],
        **kwargs,
    ):
        super().__init__(
            child=[
                Widget.Label(label=label),
                Widget.Switch(
                    halign="end",
                    hexpand=True,
                    active=active,
                    on_change=on_change,
                ),
            ],
            css_classes=["toggle-box"] + css_classes,
            **kwargs,
        )
