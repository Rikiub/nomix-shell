from ignis.services.audio import AudioService
from ignis.utils.debounce import debounce
from ignis.widgets import Widget

from nomix.utils.constants import ModuleWindow
from nomix.widgets.stream_slider import StreamVolume

audio = AudioService.get_default()


class OSD(Widget.Window):
    def __init__(self, anchor: list["str"] = ["bottom"]):
        super().__init__(
            namespace=ModuleWindow.osd,
            anchor=anchor,
            visible=False,
            layer="overlay",
            style="background-color: transparent;",
            child=Widget.Box(
                css_classes=["osd"],
                child=[StreamVolume(stream=audio.speaker, sensitive=False)],
            ),
        )

    def set_property(self, property_name, value):
        if property_name == "visible":
            self.__update_visible()

        super().set_property(property_name, value)

    @debounce(3000)
    def __update_visible(self) -> None:
        super().set_property("visible", False)
