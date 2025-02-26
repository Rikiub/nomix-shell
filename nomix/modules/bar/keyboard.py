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

        def tooltip(text: str) -> str:
            return "Keyboard Layout:\n" + text

        super().__init__(
            css_classes=["kb-layout"],
            tooltip_text=service.bind("kb_layout", tooltip) if service else "",
            on_click=lambda _: service and service.switch_kb_layout(),
            child=Widget.Box(
                child=[
                    Widget.Label(
                        label=service.bind("kb_layout", lambda v: v[:2].lower())
                    ),
                ]
            )
            if service
            else Widget.Box(),
        )
