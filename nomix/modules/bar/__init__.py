from ignis.widgets import Widget

from nomix.modules.bar.clock import Clock
from nomix.modules.bar.keyboard import KeyboardLayout
from nomix.modules.bar.launcher import Launcher
from nomix.modules.bar.notificationcenter import NotificationCenter
from nomix.modules.bar.statuspill import StatusPill
from nomix.modules.bar.systemtray import SystemTray
from nomix.modules.bar.workspaces import Workspaces


class Bar(Widget.Window):
    def __init__(self, monitor: int = 0):
        self.monitor_id: int = monitor

        super().__init__(
            exclusivity="exclusive",
            kb_mode="on_demand",
            anchor=["left", "top", "right"],
            namespace=f"bar_{self.monitor_id}",
            monitor=self.monitor_id,
            style="background-color: transparent; border: unset;",
            child=Widget.CenterBox(
                css_classes=["bar"],
                start_widget=self.start(),
                center_widget=self.center(),
                end_widget=self.end(),
            ),
        )

    def start(self) -> Widget.Box:
        return Widget.Box(
            css_classes=["bar-start"],
            child=[
                Workspaces(
                    self.monitor_id,
                    enumerated=False,
                    css_classes=["button-start"],
                ),
                Launcher(),
            ],
        )

    def center(self) -> Widget.Box:
        return Widget.Box(
            css_classes=["bar-center"],
            child=[
                Clock(),
            ],
        )

    def end(self) -> Widget.Box:
        return Widget.Box(
            css_classes=["bar-end"],
            child=[
                SystemTray(),
                Widget.Separator(),
                KeyboardLayout(),
                Widget.Box(
                    css_classes=["button-group"],
                    child=[
                        NotificationCenter(css_classes=["start"]),
                        StatusPill(css_classes=["end", "button-end"]),
                    ],
                ),
            ],
        )
