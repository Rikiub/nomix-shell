from typing import Literal

from ignis.app import IgnisApp
from ignis.base_service import BaseService
from ignis.services.hyprland import HyprlandService
from ignis.services.niri import NiriService
from ignis.widgets import Widget

from nomix.utils.constants import WindowName

hyprland = HyprlandService.get_default()
niri = NiriService.get_default()

app = IgnisApp.get_default()


class BaseWorkspaces(Widget.EventBox):
    def __init__(
        self, service: BaseService, monitor: str = "", enumerated: bool = False
    ) -> None:
        self.service = service
        self.monitor = monitor

        self.enumerated = enumerated

        super().__init__(
            on_scroll_up=lambda _: self.scroll("up"),
            on_scroll_down=lambda _: self.scroll("down"),
            on_right_click=lambda _: app.toggle_window(WindowName.launcher),
            css_classes=["workspaces"],
            spacing=5,
            child=self.service.bind(
                "workspaces",
                transform=lambda value: [
                    self.button(i)
                    for i in value
                    if self.monitor and i["output"] == self.monitor
                ],
            ),
        )

    def active_workspace_id(self) -> int: ...

    def is_workspace_active(self, workspace: dict) -> bool: ...

    def button(self, workspace: dict) -> Widget.Button:
        css_classes = ["workspace-item"]

        if self.is_workspace_active(workspace):
            css_classes.append("active")

        if self.enumerated:
            css_classes.append("enumerated")

        idx = workspace["idx"]
        widget = Widget.Button(
            css_classes=css_classes,
            on_click=lambda _, id=idx: self.service.switch_to_workspace(id),
            child=Widget.Label(label=str(idx) if self.enumerated else ""),
        )

        return widget

    def scroll(self, direction: Literal["up", "down"]) -> None:
        current = self.active_workspace_id()

        if direction == "up":
            current = current + 1
        elif direction == "down":
            current = current - 1

        self.service.switch_to_workspace(current)


class HyprlandWorkspace(BaseWorkspaces):
    def __init__(self) -> None:
        super().__init__(hyprland, "")

    def active_workspace_id(self) -> int:
        return hyprland.active_workspace["id"]  # type: ignore

    def is_workspace_active(self, workspace: dict) -> bool:
        if workspace["id"] == self.active_workspace_id():
            return True
        return False


class NiriWorkspaces(BaseWorkspaces):
    def __init__(self, monitor: str) -> None:
        super().__init__(niri, monitor)

    def active_workspace_id(self) -> int:
        filtered = [
            w
            for w in niri.workspaces  # type: ignore
            if w["is_active"] and w["output"] == self.monitor
        ]
        current: int = filtered[0]["idx"]
        return current

    def is_workspace_active(self, workspace: dict) -> bool:
        if workspace["is_active"]:
            return True
        return False


def Workspaces(monitor: str) -> Widget.EventBox:
    if hyprland.is_available:
        workspace = HyprlandWorkspace()
    elif niri.is_available:
        workspace = NiriWorkspaces(monitor)
    else:
        return Widget.EventBox()

    return workspace
