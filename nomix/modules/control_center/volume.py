from typing import Literal

from ignis.services.audio import AudioService, Stream
from ignis.widgets import Widget

from nomix.utils.options import USER_OPTIONS
from nomix.widgets.header_label import HeaderLabel
from nomix.widgets.menu_devices import DeviceItem, DeviceMenu
from nomix.widgets.stream_slider import StreamVolume

audio = AudioService.get_default()

AUDIO_TYPES = {
    "speaker": {
        "menu_icon": "audio-headphones-symbolic",
        "menu_label": "Sound Output",
    },
    "microphone": {
        "menu_icon": "microphone-sensitivity-high-symbolic",
        "menu_label": "Sound Input",
    },
}


class StreamItem(DeviceItem):
    def __init__(self, stream: Stream, stream_type: Literal["speaker", "microphone"]):
        super().__init__(
            icon_name="audio-card-symbolic",
            label=stream.description,
            active=stream.bind("is_default"),
            on_click=lambda _: setattr(audio, stream_type, stream),
        )


class StreamMenu(DeviceMenu):
    def __init__(self, stream_type: Literal["speaker", "microphone"]):
        data = AUDIO_TYPES[stream_type]
        devices = stream_type + "s"

        super().__init__(
            name=f"volume-{stream_type}",
            header=HeaderLabel(
                icon_name=data["menu_icon"],
                label=data["menu_label"],
                active=audio.bind(devices, lambda value: bool(value)),
            ),
            devices=audio.bind(
                devices, lambda value: [StreamItem(i, stream_type) for i in value]
            ),
            settings_label="Sound Settings",
            settings_command=USER_OPTIONS.control_center.settings_apps.sound,
        )


class Volume(Widget.Box):
    def __init__(self, stream_type: Literal["speaker", "microphone"]):
        stream = getattr(audio, stream_type)
        devices = stream_type + "s"

        device_menu = StreamMenu(stream_type=stream_type)
        scale = StreamVolume(stream=stream)
        arrow = Widget.Button(
            child=Widget.Arrow(pixel_size=20, rotated=device_menu.bind("reveal_child")),
            on_click=lambda _: device_menu.toggle(),
            css_classes=["volume-arrow"],
            visible=audio.bind(devices, lambda v: len(v) > 1),
        )

        super().__init__(
            visible=audio.bind(devices, lambda v: len(v) > 0),
            vertical=True,
            child=[
                Widget.Box(
                    css_classes=["volume-slider", f"volume-{stream_type}"],
                    child=[scale, arrow],
                ),
                device_menu,
            ],
        )
