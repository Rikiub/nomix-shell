from ignis.gobject import Binding, IgnisProperty
from ignis.widgets import Widget


class HeaderLabel(Widget.Box):
    def __init__(
        self,
        icon_name: str = "",
        label: str = "",
        active: bool | Binding = False,
        **kwargs,
    ):
        self._icon = Widget.Icon(
            image=icon_name, pixel_size=17, css_classes=["header-icon"]
        )

        super().__init__(
            css_classes=["header"],
            child=[
                self._icon,
                Widget.Label(label=label, halign="start", css_classes=["header-label"]),
            ],
            **kwargs,
        )

        self._active = False

        if isinstance(active, Binding):
            self.bind_property2(
                "active", active.target, active.target_properties, active.transform
            )
        else:
            self.active = active

    @IgnisProperty
    def active(self) -> bool:  # type: ignore
        return self._active

    @active.setter
    def active(self, value: bool):
        self._active = value
        self._toggle_active()

    def _toggle_active(self):
        css_class = "active"

        if self.active:
            self._icon.add_css_class(css_class)
        elif not self.active:
            self._icon.remove_css_class(css_class)
