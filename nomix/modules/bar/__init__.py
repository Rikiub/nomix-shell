from ignis.utils import Utils
from ignis.widgets import Widget

from nomix.modules.bar.clock import Clock
from nomix.modules.bar.keyboard import KeyboardLayout
from nomix.modules.bar.notification import NotificationIcon
from nomix.modules.bar.pill import StatusPill
from nomix.modules.bar.systemtray import SystemTray
from nomix.modules.bar.workspaces import Workspaces


class Bar(Widget.Window):
    def __init__(self, monitor: int = 0):
        self.monitor_name = Utils.get_monitor(monitor).get_connector()  # type: ignore

        super().__init__(
            exclusivity="exclusive",
            anchor=["left", "top", "right"],
            namespace=f"bar_{monitor}",
            monitor=monitor,
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
            child=[Workspaces(self.monitor_name)],
            spacing=10,
        )

    def center(self) -> Widget.Box:
        return Widget.Box(
            child=[Clock()],
            spacing=10,
        )

    def right(self) -> Widget.Box:
        return Widget.Box(
            child=[
                SystemTray(),
                Widget.Separator(),
                KeyboardLayout(),
                NotificationIcon(),
                StatusPill(),
            ],
            spacing=15,
        )
