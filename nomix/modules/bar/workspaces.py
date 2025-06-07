import asyncio
from typing import Literal

from ignis import widgets
from ignis.app import IgnisApp
from ignis.gobject import Binding
from ignis.services.hyprland import HyprlandService, HyprlandWorkspace
from ignis.services.niri import NiriService, NiriWorkspace
from ignis.utils.monitor import get_monitor
from ignis.utils.shell import exec_sh_async

from nomix.widgets.action_button import ActionButton
from nomix.widgets.popup_window import OPENED_POPUP

hyprland = HyprlandService.get_default()
niri = NiriService.get_default()

app = IgnisApp.get_default()

Service = HyprlandService | NiriService
Workspace = HyprlandWorkspace | NiriWorkspace


class BaseWorkspaces(ActionButton):
    def __init__(
        self,
        service: Service,
        enumerated: bool,
        css_classes: list[str] = [],
        **kwargs,
    ) -> None:
        self.service = service
        self.enumerated = enumerated

        super().__init__(
            on_scroll_up=lambda _: self.scroll("up"),
            on_scroll_down=lambda _: self.scroll("down"),
            tooltip_text="Workspaces",
            css_classes=["workspaces", *css_classes],
            child=widgets.Box(child=self.button_generator()),
            **kwargs,
        )

    def button_generator(self) -> Binding: ...

    def is_workspace_active(self, workspace: Workspace) -> bool: ...

    def active_workspace(self) -> Workspace:
        for i in self.service.workspaces:
            if i.is_active:
                return i

        raise ValueError("Niri has not active workspace")

    def button(self, workspace: Workspace) -> widgets.Box:
        css_classes = ["workspace-item"]

        if self.is_workspace_active(workspace):
            css_classes.append("active")

        if self.enumerated:
            css_classes.append("enumerated")

        idx = workspace.idx
        widget = widgets.Box(
            css_classes=css_classes,
            # on_click=lambda _, id=idx: self.service.switch_to_workspace(id),
            child=[widgets.Label(label=str(idx) if self.enumerated else "")],
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
    def __init__(
        self,
        enumerated: bool,
        css_classes: list[str] = [],
    ) -> None:
        super().__init__(hyprland, enumerated, css_classes)

    def button_generator(self) -> Binding:
        return self.service.bind(
            "workspaces", lambda value: [self.button(i) for i in value]
        )

    def active_workspace(self) -> Workspace:
        return self.service.active_workspace

    def is_workspace_active(self, workspace: Workspace) -> bool:
        return workspace.id == self.active_workspace().id


class NiriWorkspaces(BaseWorkspaces):
    def __init__(
        self,
        monitor_id: int,
        enumerated: bool,
        css_classes: list[str] = [],
    ) -> None:
        self.monitor = None
        if monitor := get_monitor(monitor_id):
            self.monitor = monitor.get_connector()

        super().__init__(
            niri,
            enumerated,
            css_classes,
            on_click=lambda _: asyncio.create_task(
                exec_sh_async("niri msg action toggle-overview")
            ),
        )

        niri.connect(
            "notify::overview-opened",
            lambda *_: self._toggle_overview_cssclass(),
        )

    def _toggle_overview_cssclass(self):
        if niri.overview_opened:
            self._button.add_css_class("active-command")
        else:
            self._button.remove_css_class("active-command")

        OPENED_POPUP.value = ""

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


def Workspaces(
    monitor_id: int,
    enumerated: bool = False,
    css_classes: list[str] = [],
) -> widgets.EventBox:
    if hyprland.is_available:
        workspace = HyprlandWorkspaces(enumerated, css_classes)
    elif niri.is_available:
        workspace = NiriWorkspaces(monitor_id, enumerated, css_classes)
    else:
        return widgets.EventBox()

    return workspace
