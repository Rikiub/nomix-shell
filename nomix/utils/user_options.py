from ignis.options_manager import OptionsGroup, OptionsManager

from nomix.utils.constants import CACHE_DIR, IGNIS_DIR


class CacheOptions(OptionsManager):
    force_dark = False
    night_light = False
    wallpaper = ""
    matugen_scheme = ""


class UserOptions(OptionsManager):
    force_dark_theme = False

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

    class Matugen(OptionsGroup):
        enabled = False
        scheme = "monochrome"

    bar = Bar()
    clock = ClockFormat()
    launcher = Launcher()
    control_apps = ControlApps()
    night_light = NightLight()
    matugen = Matugen()


config_file = IGNIS_DIR / "options.json"
if not config_file.exists():
    config_file.write_text("{}")

cache_file = CACHE_DIR / "options.json"
if not cache_file.exists():
    cache_file.parent.mkdir(exist_ok=True)
    cache_file.write_text("{}")

user_options = UserOptions(str(config_file))
cache_options = CacheOptions(str(cache_file))
cache_options.force_dark = False
