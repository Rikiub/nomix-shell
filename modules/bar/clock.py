import datetime
import locale
from typing import Literal

from ignis.utils import Utils
from ignis.widgets import Widget

from modules.user_options import user_options

class Clock(Widget.Label):
    def __init__(self):
        options = user_options.clock

        # Time
        time_format = f"%H:%M{':%S' if options.seconds else ''}"

        if not options.military_time:
            time_format = time_format + " %p"

        # Date
        week = ""
        if options.week_day:
            if options.full_date:
                week = "%A"
            else:
                week = "%a"

            week = week + " "

        date_format = f"{week}{'%B' if options.full_date else '%b'} %d"

        super().__init__(
            css_classes=["clock"],
            label=Utils.Poll(
                1000,
                lambda _: datetime.datetime.now().strftime(
                    f"{date_format}   {time_format}"
                ),
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