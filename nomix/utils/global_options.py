from ignis.options_manager import OptionsGroup, OptionsManager

from nomix.utils.constants import CACHE_DIR, IGNIS_DIR


class CacheOptions(OptionsManager):
    theme_is_dark = False
    night_light = False
    wallpaper = ""
    matugen_scheme = ""


class UserOptions(OptionsManager):
    prefer_dark_shell = False

    class ClockFormat(OptionsGroup):
        full_date = False
        week_day = False

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
        run_user_config = True

    bar = Bar()
    clock = ClockFormat()
    launcher = Launcher()
    control_apps = ControlApps()
    night_light = NightLight()
    matugen = Matugen()


config_file = IGNIS_DIR / "options.json"
cache_file = CACHE_DIR / "options.json"

for config in (config_file, cache_file):
    if not config.exists():
        cache_file.parent.mkdir(exist_ok=True)
        cache_file.write_text("{}")

user_options = UserOptions(str(config_file))
cache_options = CacheOptions(str(cache_file))
cache_options.theme_is_dark = False
