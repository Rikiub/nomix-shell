from gi.repository import GObject  # type: ignore
from ignis.base_widget import BaseWidget
from ignis.variable import Variable
from ignis.widgets import Widget

OPENED_MENU = Variable("")


class Menu(Widget.Revealer):
    def __init__(
        self,
        name: str,
        child: list[BaseWidget],
        css_classes: list[str] = [],
        **kwargs,
    ):
        self._name = name
        self._box = Widget.Box(
            vertical=True,
            css_classes=["accordion-menu"] + css_classes,
            child=child,
        )

        super().__init__(
            transition_type="slide_down",
            transition_duration=300,
            reveal_child=OPENED_MENU.bind("value", lambda value: value == self._name),
            child=self._box,
            **kwargs,
        )

    def toggle(self) -> None:
        if self.reveal_child:
            OPENED_MENU.value = ""
        else:
            OPENED_MENU.value = self._name

    @GObject.Property
    def box(self) -> Widget.Box:
        return self._box
