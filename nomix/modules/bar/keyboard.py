from ignis.services.hyprland import HyprlandService, HyprlandKeyboard
from ignis.services.niri import NiriService, NiriKeyboardLayouts
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
            css_classes=["kb-layout"],
            tooltip_text=keyboard.bind(name_property, tooltip)
            if keyboard
            else "Unknown Keyboard Layout",
            on_click=lambda _: keyboard and keyboard.switch_layout(next_property),
            child=Widget.Label(label=keyboard.bind(name_property, short))
            if keyboard
            else Widget.Label(label="?"),
        )
