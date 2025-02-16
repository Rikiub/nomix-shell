from ignis.options_manager import OptionsGroup, OptionsManager

from modules.types import IGNIS_PATH  # type: ignore


class UserOptions(OptionsManager):
    class ClockFormat(OptionsGroup):
        full_date = False
        week_day = True

        military_time = True
        seconds = False

    class ControlApps(OptionsGroup):
        network = "nm-connection-editor"
        sound = "pavucontrol"
        bluetooth = "overskride"

    class NightLight(OptionsGroup):
        enabled = False
        activate_command = "wlsunset"
        deactivate_command = "pkill wlsunset"

    clock = ClockFormat()
    control_apps = ControlApps()
    night_light = NightLight()


config_file = IGNIS_PATH / "user_options.json"
user_options = UserOptions(str(config_file))
