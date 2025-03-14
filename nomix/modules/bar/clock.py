import datetime
import locale
from typing import Literal

from ignis.utils import Utils
from ignis.widgets import Widget

from nomix.utils.options import USER_OPTIONS


class Clock(Widget.Label):
    def __init__(self):
        self.format = self._update_format()

        USER_OPTIONS.bar.connect_option(
            "clock_format", lambda *_: self._update_format()
        )

        super().__init__(
            css_classes=["clock"],
            label=Utils.Poll(
                1000,
                lambda _: datetime.datetime.now().strftime(self.format),
            ).bind("output"),
        )

    def system_time_format(self) -> Literal["24", "12"]:
        try:
            locale.setlocale(locale.LC_TIME, "")
            time_format = locale.nl_langinfo(locale.T_FMT)

            if "%p" in time_format:
                return "12"
            else:
                return "24"
        except locale.Error:
            return "24"

    def _update_format(self) -> str:
        options = USER_OPTIONS.bar.clock_format

        # Time
        time_format = "%H:%M" if options.military_time else "%I:%M"
        time_format + ":%S" if options.seconds else ""

        if not options.military_time:
            time_format = time_format + " %P"

        # Date
        week = ""
        if options.week_day:
            if options.full_date:
                week = "%A"
            else:
                week = "%a"

            week = week + " "

        date_format = f"{week}{'%B' if options.full_date else '%b'} %d"

        self.format = f"{date_format}   {time_format}"
        return self.format
