import asyncio

from ignis import utils, widgets

from nomix.utils.options import USER_OPTIONS


class LockButton(widgets.Button):
    def __init__(self, **kwargs):
        super().__init__(
            css_classes=["lock-button"],
            tooltip_text="Lock Screen",
            on_click=lambda _: asyncio.create_task(
                utils.exec_sh_async(USER_OPTIONS.control_center.screenlocker)
            ),
            child=widgets.Icon(image="lock-symbolic"),
            **kwargs,
        )
