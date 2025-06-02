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
            css_classes=["accordion-menu"] + css_classes,
            vertical=True,
            child=child,
        )

        super().__init__(
            reveal_child=OPENED_MENU.bind("value", lambda value: value == self._name),
            transition_type="slide_down",
            transition_duration=300,
            child=self._box,
            **kwargs,
        )

    def toggle(self) -> None:
        if self.reveal_child:
            OPENED_MENU.value = ""
        else:
            OPENED_MENU.value = self._name
