from ignis import widgets

from nomix.modules.bar.clock import Clock
from nomix.modules.bar.keyboard import KeyboardLayout
from nomix.modules.bar.notificationcenter import NotificationCenter
from nomix.modules.bar.statuspill import StatusPill
from nomix.modules.bar.systemtray import SystemTray
from nomix.modules.bar.workspaces import Workspaces


class Bar(widgets.Window):
    def __init__(self, monitor: int = 0):
        self.monitor_id: int = monitor

        super().__init__(
            exclusivity="exclusive",
            kb_mode="on_demand",
            anchor=["left", "top", "right"],
            namespace=f"bar_{self.monitor_id}",
            monitor=self.monitor_id,
            style="background-color: transparent; border: unset;",
            child=widgets.CenterBox(
                css_classes=["bar"],
                start_widget=self.start(),
                center_widget=self.center(),
                end_widget=self.end(),
            ),
        )

    def start(self) -> widgets.Box:
        return widgets.Box(
            css_classes=["bar-start"],
            child=[
                Workspaces(
                    self.monitor_id,
                    enumerated=False,
                    css_classes=["button-start"],
                ),
            ],
        )

    def center(self) -> widgets.Box:
        return widgets.Box(
            css_classes=["bar-center"],
            child=[
                Clock(),
            ],
        )

    def end(self) -> widgets.Box:
        return widgets.Box(
            css_classes=["bar-end"],
            child=[
                SystemTray(),
                widgets.Separator(),
                KeyboardLayout(),
                widgets.Box(
                    css_classes=["button-group"],
                    child=[
                        NotificationCenter(css_classes=["start"]),
                        StatusPill(css_classes=["end", "button-end"]),
                    ],
                ),
            ],
        )
