from ignis.services.audio import AudioService
from ignis.utils.debounce import debounce
from ignis.widgets import Widget

from modules.types import WindowName
from widgets.stream_slider import StreamVolume

audio = AudioService.get_default()


class OSD(Widget.Window):
    def __init__(self):
        super().__init__(
            namespace=WindowName.osd,
            layer="overlay",
            anchor=["bottom"],
            visible=False,
            child=Widget.Box(
                css_classes=["osd"],
                child=[
                    Widget.Icon(
                        pixel_size=26,
                        style="margin-right: 0.5rem;",
                        image=audio.speaker.bind("icon_name"),
                    ),
                    StreamVolume(stream=audio.speaker, sensitive=False),
                ],
            ),
        )

    def set_property(self, property_name, value):
        if property_name == "visible":
            self.__update_visible()

        super().set_property(property_name, value)

    @debounce(3000)
    def __update_visible(self) -> None:
        super().set_property("visible", False)
