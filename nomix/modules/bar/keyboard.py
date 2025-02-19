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
            service = None

        super().__init__(
            css_classes=["kb-layout"],
            tooltip_text="Keyboard layout",
            on_click=lambda _: service and service.switch_kb_layout(),
            child=Widget.Box(
                child=[
                    Widget.Icon(
                        image="input-keyboard-symbolic", style="margin-right: 5px;"
                    ),
                    Widget.Label(
                        label=service and service.bind("kb_layout"),
                    ),
                ]
            ),
        )
