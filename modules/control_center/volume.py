from typing import Literal

from ignis.services.audio import AudioService, Stream
from ignis.widgets import Widget

from modules.user_options import user_options
from widgets.menu_devices import DeviceItem, DeviceMenu
from widgets.stream_slider import StreamVolume

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
            on_click=lambda x: setattr(audio, stream_type, stream),
        )


class StreamMenu(DeviceMenu):
    def __init__(self, stream_type: Literal["speaker", "microphone"]):
        data = AUDIO_TYPES[stream_type]

        super().__init__(
            name=f"volume-{stream_type}",
            header=Widget.Box(
                child=[
                    Widget.Icon(
                        image=data["menu_icon"],
                        pixel_size=24,
                        style="margin-right: 5px;",
                    ),
                    Widget.Label(
                        label=data["menu_label"],
                        halign="start",
                    ),
                ],
            ),
            devices=audio.bind(
                stream_type + "s",
                lambda value: [StreamItem(i, stream_type) for i in value],
            ),
            settings_label="Sound Settings",
            settings_command=user_options.control_center.sound_app,
        )


class Volume(Widget.Box):
    def __init__(self, stream_type: Literal["speaker", "microphone"]):
        stream = getattr(audio, stream_type)

        device_menu = StreamMenu(stream_type=stream_type)
        scale = StreamVolume(
            stream=stream,
        )
        arrow = Widget.Button(
            child=Widget.Arrow(pixel_size=20, rotated=device_menu.bind("reveal_child")),
            on_click=lambda x: device_menu.toggle(),
            css_classes=["volume-arrow"],
        )

        super().__init__(
            vertical=True,
            child=[
                Widget.Box(
                    css_classes=["volume-slider", f"volume-{stream_type}"],
                    child=[scale, arrow],
                ),
                device_menu,
            ],
        )
