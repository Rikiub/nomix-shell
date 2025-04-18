from typing import Literal

from ignis.app import IgnisApp
from ignis.gobject import Binding
from ignis.services.hyprland import HyprlandService, HyprlandWorkspace
from ignis.services.niri import NiriService, NiriWorkspace
from ignis.utils import Utils
from ignis.widgets import Widget

from nomix.widgets.actionable_button import ActionableButton

hyprland = HyprlandService.get_default()
niri = NiriService.get_default()

app = IgnisApp.get_default()

Service = HyprlandService | NiriService
Workspace = HyprlandWorkspace | NiriWorkspace


class BaseWorkspaces(Widget.EventBox):
    def __init__(self, service: Service, enumerated: bool) -> None:
        self.service = service
        self.enumerated = enumerated

        super().__init__(
            on_scroll_up=lambda _: self.scroll("up"),
            on_scroll_down=lambda _: self.scroll("down"),
            css_classes=["workspaces"],
            spacing=5,
            child=self.button_generator(),
        )

    def button_generator(self) -> Binding: ...

    def is_workspace_active(self, workspace: Workspace) -> bool: ...

    def active_workspace(self) -> Workspace:
        for i in self.service.workspaces:
            if i.is_active:
                return i

        raise ValueError("Niri has not active workspace")

    def button(self, workspace: Workspace) -> ActionableButton:
        css_classes = ["workspace-item"]

        if self.is_workspace_active(workspace):
            css_classes.append("active")

        if self.enumerated:
            css_classes.append("enumerated")

        idx = workspace.idx
        widget = ActionableButton(
            css_classes=css_classes,
            on_click=lambda _, id=idx: self.service.switch_to_workspace(id),
            child=Widget.Label(label=str(idx) if self.enumerated else ""),
        )

        return widget

    def scroll(self, direction: Literal["up", "down"]) -> None:
        idx = self.active_workspace().idx

        if direction == "up":
            current = idx + 1
        elif direction == "down":
            current = idx - 1

        self.service.switch_to_workspace(current)


class HyprlandWorkspaces(BaseWorkspaces):
    def __init__(self, enumerated: bool) -> None:
        super().__init__(hyprland, enumerated)

    def button_generator(self) -> Binding:
        return self.service.bind(
            "workspaces", lambda value: [self.button(i) for i in value]
        )

    def active_workspace(self) -> Workspace:
        return self.service.active_workspace

    def is_workspace_active(self, workspace: Workspace) -> bool:
        return workspace.id == self.active_workspace().id


class NiriWorkspaces(BaseWorkspaces):
    def __init__(self, monitor: int, enumerated: bool) -> None:
        self.monitor = Utils.get_monitor(monitor).get_connector()  # type: ignore
        super().__init__(niri, enumerated)

    def button_generator(self) -> Binding:
        return self.service.bind(
            "workspaces",
            lambda value: [self.button(i) for i in value if i.output == self.monitor],
        )

    def active_workspace(self) -> Workspace:
        for w in self.service.workspaces:
            if w.is_active:
                return w

        raise ValueError("Niri has not active workspace")

    def is_workspace_active(self, workspace: Workspace) -> bool:
        return workspace.is_active


def Workspaces(monitor: int, enumerated: bool = False) -> Widget.EventBox:
    if hyprland.is_available:
        workspace = HyprlandWorkspaces(enumerated)
    elif niri.is_available:
        workspace = NiriWorkspaces(monitor, enumerated)
    else:
        return Widget.EventBox()

    return workspace
