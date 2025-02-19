from ignis.options_manager import OptionsGroup, OptionsManager

from nomix.utils.constants import CACHE_DIR, IGNIS_DIR


class CacheOptions(OptionsManager):
    night_light = False


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

    class Bar(OptionsGroup):
        battery_percent = False

    class NightLight(OptionsGroup):
        activate_command = "wlsunset"
        deactivate_command = "pkill wlsunset"

    bar = Bar()
    clock = ClockFormat()
    launcher = Launcher()
    control_apps = ControlApps()
    night_light = NightLight()


config_file = IGNIS_DIR / "options.json"
cache_file = CACHE_DIR / "ignis" / "nomix_options.json"

if not cache_file.exists():
    cache_file.touch(exist_ok=True)
    cache_file.write_text("{}")

user_options = UserOptions(str(config_file))
cache_options = CacheOptions(str(cache_file))
