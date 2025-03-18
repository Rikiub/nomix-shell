from ignis.widgets import Widget

from nomix.modules.bar.clock import Clock
from nomix.modules.bar.keyboard import KeyboardLayout
from nomix.modules.bar.launcher import LauncherButton
from nomix.modules.bar.notification import NotificationCenterButton
from nomix.modules.bar.pill import StatusPill
from nomix.modules.bar.systemtray import SystemTray
from nomix.modules.bar.workspaces import Workspaces


class Bar(Widget.Window):
    def __init__(self, monitor: int = 0):
        self.monitor_id: int = monitor

        super().__init__(
            exclusivity="exclusive",
            anchor=["left", "top", "right"],
            namespace=f"bar_{self.monitor_id}",
            monitor=self.monitor_id,
            kb_mode="on_demand",
            style="background-color: transparent;",
            child=Widget.CenterBox(
                css_classes=["bar"],
                start_widget=self.left(),
                center_widget=self.center(),
                end_widget=self.right(),
            ),
        )

    def left(self) -> Widget.Box:
        return Widget.Box(
            child=[Workspaces(self.monitor_id, enumerated=False)],
            css_classes=["bar-left"],
            spacing=10,
        )

    def center(self) -> Widget.Box:
        return Widget.Box(
            child=[Clock(), LauncherButton()],
            css_classes=["bar-center"],
            spacing=10,
        )

    def right(self) -> Widget.Box:
        return Widget.Box(
            child=[
                SystemTray(),
                Widget.Separator(),
                KeyboardLayout(),
                NotificationCenterButton(),
                StatusPill(),
            ],
            css_classes=["bar-right"],
            spacing=15,
        )
