from ignis.services.audio import AudioService
from ignis.utils.debounce import debounce
from ignis.widgets import Widget

from nomix.utils.constants import ModuleWindow
from nomix.widgets.stream_slider import StreamVolume

audio = AudioService.get_default()


class OSD(Widget.Window):
    def __init__(self, anchor: list["str"] = ["bottom"]):
        self._persist = False

        def on_hover():
            self._persist = True
            self.__update_visible()

        def on_hover_lost():
            self._persist = False
            self.__update_visible()

        super().__init__(
            namespace=ModuleWindow.OSD,
            anchor=anchor,
            visible=False,
            layer="overlay",
            style="background-color: transparent; border: unset;",
            child=Widget.EventBox(
                css_classes=["osd"],
                on_hover=lambda _: on_hover(),
                on_hover_lost=lambda _: on_hover_lost(),
                child=[StreamVolume(stream=audio.speaker, muteable=False)],
            ),
        )

    def set_property(self, property_name, value):
        if property_name == "visible":
            self.__update_visible()

        super().set_property(property_name, value)

    @debounce(3000)
    def __update_visible(self) -> None:
        if not self._persist:
            super().set_property("visible", False)
