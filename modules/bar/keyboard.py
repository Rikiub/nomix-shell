from ignis.services.hyprland import HyprlandService
from ignis.services.niri import NiriService
from ignis.widgets import Widget

hyprland = HyprlandService.get_default()
niri = NiriService.get_default()


class KeyboardLayout(Widget.Button):
    def __init__(self):
        if hyprland.is_available:
            service = hyprland
        elif niri.is_available:
            service = niri
        else:
            return Widget.EventBox()

        super().__init__(
            css_classes=["kb-layout"],
            tooltip_text="Keyboard layout",
            on_click=lambda self: service.switch_kb_layout(),
            child=Widget.Box(
                child=[
                    Widget.Icon(image="input-keyboard", style="margin-right: 5px;"),
                    Widget.Label(
                        label=service.bind("kb_layout"),
                    ),
                ]
            ),
        )
