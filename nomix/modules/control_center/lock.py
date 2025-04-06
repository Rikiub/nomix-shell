import asyncio

from ignis.utils.shell import exec_sh_async
from ignis.widgets import Widget

from nomix.utils.options import USER_OPTIONS


class LockButton(Widget.Button):
    def __init__(self, **kwargs):
        super().__init__(
            css_classes=["lock-button"],
            tooltip_text="Lock Screen",
            on_click=lambda _: asyncio.create_task(
                exec_sh_async(USER_OPTIONS.control_center.screenlocker)
            ),
            child=Widget.Icon(image="lock-symbolic"),
            **kwargs,
        )
