from ignis.options_manager import OptionsGroup, OptionsManager

from modules.utils import IGNIS_DIR  # type: ignore


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

    class Launcher(OptionsGroup):
        grid = False
        grid_columns = 4

    class NightLight(OptionsGroup):
        enabled = False
        activate_command = "wlsunset"
        deactivate_command = "pkill wlsunset"

    clock = ClockFormat()
    launcher = Launcher()
    control_apps = ControlApps()
    night_light = NightLight()


config_file = IGNIS_DIR / "options.json"
user_options = UserOptions(str(config_file))
