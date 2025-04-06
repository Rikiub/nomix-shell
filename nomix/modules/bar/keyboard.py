from ignis.services.hyprland import HyprlandKeyboard, HyprlandService
from ignis.services.niri import NiriKeyboardLayouts, NiriService
from ignis.widgets import Widget

hyprland = HyprlandService.get_default()
niri = NiriService.get_default()


class KeyboardLayout(Widget.Button):
    def __init__(self):
        keyboard: HyprlandKeyboard | NiriKeyboardLayouts | None = None
        name_property = ""
        next_property = ""

        if hyprland.is_available:
            keyboard = hyprland.main_keyboard
            name_property = "active_keymap"
            next_property = "next"
        elif niri.is_available:
            keyboard = niri.keyboard_layouts
            name_property = "current_name"
            next_property = "Next"

        def tooltip(text: str) -> str:
            return "Keyboard Layout:\n" + text

        def short(v: str):
            return v[:2].lower()

        super().__init__(
            # CSS Classes
            css_classes=["keyboard-layout"],
            #
            # Visibility
            tooltip_text=keyboard.bind(name_property, tooltip) if keyboard else "?",
            visible=keyboard and keyboard.bind("names", lambda v: len(v) > 1),
            #
            # Function
            on_click=lambda _: keyboard and keyboard.switch_layout(next_property),
            #
            # Widget
            child=Widget.Label(label=keyboard.bind(name_property, short))
            if keyboard
            else Widget.Label(label="?"),
        )
