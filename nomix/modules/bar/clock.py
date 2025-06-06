import datetime

from ignis import utils, widgets

from nomix.utils.constants import ModuleWindow
from nomix.utils.options import USER_OPTIONS
from nomix.widgets.action_button import ActionButton


class Clock(ActionButton):
    def __init__(self):
        self.format: str = self._update_format()

        USER_OPTIONS.bar.connect(
            "subgroup_changed",
            lambda _, group, option: self._update_format()
            if group == "clock_format"
            else None,
        )

        super().__init__(
            css_classes=["clock"],
            tooltip_text="Launcher",
            toggle_window=ModuleWindow.LAUNCHER,
            child=widgets.Label(
                css_classes=["clock-text"],
                label=utils.Poll(
                    1000,
                    lambda _: datetime.datetime.now().strftime(self.format),
                ).bind("output"),
            ),
        )

    def _update_format(self) -> str:
        opt = USER_OPTIONS.bar.clock_format

        # Time
        time_format = "%H:%M" if opt.military_time else "%I:%M"
        time_format += ":%S" if opt.seconds else ""

        if not opt.military_time:
            time_format = time_format + " %P"

        # Date
        week = ""
        if opt.week_day:
            if opt.full_date:
                week = "%A"
            else:
                week = "%a"

            week = week + " "

        date_format = f"{week}{'%B' if opt.full_date else '%b'} %d"

        self.format = f"{date_format}   {time_format}"
        return self.format
