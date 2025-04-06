from pathlib import Path
from ignis.options_manager import OptionsGroup, OptionsManager

from nomix.utils.types import StrPath
from nomix.utils.constants import CACHE_DIR, IGNIS_DIR


class BaseManager(OptionsManager):
    def __init__(self, file: StrPath):
        file = Path(file)

        if not file.exists():
            file.parent.mkdir(exist_ok=True)
            file.write_text("{}")

        super().__init__(str(file))


class CacheOptions(BaseManager):
    def __init__(self):
        super().__init__(CACHE_DIR / "options.json")
        self.theme_is_dark = False

    color_scheme = "default"
    theme_is_dark = False
    night_light = False
    last_ethernet = None
    wallpaper = ""
    matugen_scheme = ""


class UserOptions(BaseManager):
    def __init__(self):
        super().__init__(IGNIS_DIR / "options.json")

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
            sound = "pavucontrol"
            network = "nm-connection-editor"
            bluetooth = "overskride"

        screenlocker = "swaylock"
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

    bar: Bar | None = Bar()
    launcher = Launcher()
    control_center = ControlCenter()
    night_light = NightLight()
    matugen = Matugen()

    debug = Debug()

USER_OPTIONS = UserOptions()
CACHE_OPTIONS = CacheOptions()