from ignis.options_manager import OptionsGroup, OptionsManager


class UserOptions(OptionsManager):
    class Control(OptionsGroup):
        network_app = "nm-connection-editor"
        sound_app = "pavucontrol"
        bluetooth_app = "overskride"

    control = Control()


user_options = UserOptions(None)
