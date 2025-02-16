import datetime

from ignis.utils import Utils
from ignis.widgets import Widget


class Clock(Widget.Button):
    def __init__(self):
        self.date = False

        super().__init__(
            css_classes=["clock"],
            on_click=lambda _: self.toggle_date(),
            setup=lambda _: self.toggle_date(),
        )

    def toggle_date(self):
        if self.date:
            self.child = Widget.Label(
                label=Utils.Poll(
                    1000, lambda self: datetime.datetime.now().strftime("%A, %B %d, %Y")
                ).bind("output")
            )
        else:
            self.child = Widget.Label(
                label=Utils.Poll(
                    1000, lambda self: datetime.datetime.now().strftime("%H:%M")
                ).bind("output")
            )

        self.date = not self.date
