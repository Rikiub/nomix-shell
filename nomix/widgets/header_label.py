from ignis.widgets import Widget


class HeaderLabel(Widget.Box):
    def __init__(
        self,
        icon_name: str = "",
        label: str = "",
        **kwargs,
    ):
        self._icon = Widget.Icon(
            css_classes=["header-icon"],
            image=icon_name,
            pixel_size=17,
        )

        super().__init__(
            css_classes=["header"],
            child=[
                self._icon,
                Widget.Label(
                    css_classes=["header-label"],
                    label=label,
                    halign="start",
                ),
            ],
            **kwargs,
        )
