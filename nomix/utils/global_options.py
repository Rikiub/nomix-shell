from ignis.options_manager import OptionsGroup, OptionsManager

from nomix.utils.constants import CACHE_DIR, IGNIS_DIR


class CacheOptions(OptionsManager):
    last_ethernet = None
    theme_is_dark = False
    night_light = False
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
        scheme = "monochrome"
        run_user_config = True

    class Debug(OptionsGroup):
        bluetooth_forced = False
        battery_hidden = False

    bar = Bar()
    launcher = Launcher()
    control_center = ControlCenter()
    night_light = NightLight()
    matugen = Matugen()

    debug = Debug()


config_file = IGNIS_DIR / "options.json"
cache_file = CACHE_DIR / "options.json"

for config in (config_file, cache_file):
    if not config.exists():
        config.parent.mkdir(exist_ok=True)
        config.write_text("{}")

user_options = UserOptions(str(config_file))
cache_options = CacheOptions(str(cache_file))
cache_options.theme_is_dark = False
