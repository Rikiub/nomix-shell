from ignis.options_manager import OptionsGroup, OptionsManager
from gi.repository import GLib  # type: ignore


class UserOptions(OptionsManager):
    class ControlCenter(OptionsGroup):
        network_app = "nm-connection-editor"
        sound_app = "pavucontrol"
        bluetooth_app = "overskride"

        night_light = False

    control_center = ControlCenter()


config_file = f"{GLib.get_user_config_dir()}/ignis/user_options.json"
user_options = UserOptions(config_file)
