from typing import Callable

from ignis import widgets
from ignis.gobject import Binding


class ToggleBox(widgets.Box):
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
                widgets.Label(label=label),
                widgets.Switch(
                    halign="end",
                    hexpand=True,
                    active=active,
                    on_change=on_change,
                ),
            ],
            css_classes=["toggle-box"] + css_classes,
            **kwargs,
        )
