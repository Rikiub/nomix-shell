from ignis.options_manager import OptionsGroup, OptionsManager

from nomix.utils.constants import CACHE_DIR, IGNIS_DIR


class CacheOptions(OptionsManager):
    color_scheme = "default"
    theme_is_dark = False
    night_light = False
    last_ethernet = None
    wallpaper = ""
    matugen_scheme = ""


class UserOptions(OptionsManager):
    prefer_dark_shell = False

    class Bar(OptionsGroup):
        class StatusPill(OptionsGroup):
            battery_percent = False

        class ClockFormat(OptionsGroup):
            full_date = False
            week_day = False

            military_time = True
            seconds = False

        clock_format = ClockFormat()
        status_pill = StatusPill()

    class ControlCenter(OptionsGroup):
        class SettingsApps(OptionsGroup):
            network = "nm-connection-editor"
            sound = "pavucontrol"
            bluetooth = "overskride"

        settings_apps = SettingsApps()

    class Launcher(OptionsGroup):
        grid = False
        grid_columns = 4

    class NightLight(OptionsGroup):
        enabled = True
        activate_command = "wlsunset"
        deactivate_command = "pkill wlsunset"

    class Matugen(OptionsGroup):
        enabled = False
        scheme = "tonal-spot"
        run_user_config = True

    class Debug(OptionsGroup):
        battery_hidden = False

    bar = Bar()
    launcher = Launcher()
    control_center = ControlCenter()
    night_light = NightLight()
    matugen = Matugen()

    debug = Debug()


json_schema = """{
    "$schema": "./schema.json"
}"""

config_file = IGNIS_DIR / "options.json"
if not config_file.exists():
    config_file.parent.mkdir(exist_ok=True)
    config_file.write_text(json_schema)

cache_file = CACHE_DIR / "options.json"
if not cache_file.exists():
    cache_file.parent.mkdir(exist_ok=True)
    cache_file.write_text("{}")

USER_OPTIONS = UserOptions(str(config_file))
CACHE_OPTIONS = CacheOptions(str(cache_file))
CACHE_OPTIONS.theme_is_dark = False
