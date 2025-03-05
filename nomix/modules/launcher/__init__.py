import asyncio
import re

from ignis.app import IgnisApp
from ignis.services.applications import (
    Application,
    ApplicationAction,
    ApplicationsService,
)
from ignis.utils.icon import get_app_icon_name
from ignis.utils.shell import exec_sh, exec_sh_async
from ignis.widgets import Widget

from nomix.utils.constants import ModuleWindow
from nomix.utils.options import USER_OPTIONS
from nomix.utils.types import ALIGN
from nomix.widgets.popup_window import PopupWindow

app = IgnisApp.get_default()
applications = ApplicationsService.get_default()

PIN_APPS = False


class LauncherAppItem(Widget.Button):
    def __init__(self, application: Application, vertical: bool = False) -> None:
        self._application = application

        super().__init__(
            on_click=lambda _: self.launch(),
            on_right_click=lambda _: self._menu.popup(),
            tooltip_text=application.name if vertical else None,
            css_classes=["launcher-app"],
            child=Widget.Box(
                vertical=vertical,
                child=[
                    Widget.Icon(image=application.icon, pixel_size=48),
                    Widget.Label(
                        label=application.name,
                        ellipsize="end",
                        max_width_chars=30,
                        css_classes=["launcher-app-label"],
                    ),
                ],
            ),
        )
        self._sync_menu()
        application.connect("notify::is-pinned", lambda *_: self._sync_menu())

    def launch(self) -> None:
        self._application.launch()
        app.close_window(ModuleWindow.LAUNCHER)

    def launch_action(self, action: ApplicationAction) -> None:
        action.launch()
        app.close_window(ModuleWindow.LAUNCHER)

    def _sync_menu(self) -> None:
        pin = (
            [
                Widget.MenuItem(
                    label="Pin", on_activate=lambda _: self._application.pin()
                )
                if not self._application.is_pinned
                else Widget.MenuItem(
                    label="Unpin", on_activate=lambda _: self._application.unpin()
                ),
            ]
            if PIN_APPS
            else []
        )

        self._menu = Widget.PopoverMenu(
            items=[
                Widget.MenuItem(label="Launch", on_activate=lambda _: self.launch()),
            ]
            + pin
            + [Widget.Separator()]
            + [
                Widget.MenuItem(
                    label=i.name,
                    on_activate=lambda _, action=i: self.launch_action(action),
                )
                for i in self._application.actions
            ]
        )
        self.child.append(self._menu)


def _get_default_browser_icon() -> str:
    desktop = exec_sh("xdg-settings get default-web-browser").stdout.strip()
    desktop = str(desktop).strip(".desktop")

    if icon := get_app_icon_name(desktop):
        return icon
    else:
        return ""


class SearchWebButton(Widget.Button):
    icon = _get_default_browser_icon()

    def __init__(self, query: str):
        self._query = query
        self._url = ""

        if not query.startswith(("http://", "https://")) and "." in query:
            query = "https://" + query

        if self._is_url(query):
            label = f"Visit {query}"
            self._url = query
        else:
            label = "Search in Google"
            self._url = f"https://www.google.com/search?q={query.replace(' ', '+')}"

        super().__init__(
            on_click=lambda _: self.launch(),
            css_classes=["launcher-app", "launcher-web-search"],
            child=Widget.Box(
                child=[
                    Widget.Icon(image=self.icon, pixel_size=48),
                    Widget.Label(
                        label=label,
                        css_classes=["launcher-app-label"],
                    ),
                ]
            ),
        )

    def _is_url(self, url: str) -> bool:
        regex = re.compile(
            r"^(?:http|ftp)s?://"  # http:// or https://
            r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"  # domain
            r"localhost|"  # localhost
            r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|"  # or ipv4
            r"\[?[A-F0-9]*:[A-F0-9:]+\]?)"  # or ipv6
            r"(?::\d+)?"  # optional port
            r"(?:/?|[/?]\S+)$",
            re.IGNORECASE,
        )
        return re.match(regex, url) is not None

    def launch(self) -> None:
        asyncio.create_task(exec_sh_async(f"xdg-open {self._url}"))
        app.close_window(ModuleWindow.LAUNCHER)


class Launcher(PopupWindow):
    def __init__(
        self,
        valign: ALIGN = "start",
        halign: ALIGN = "center",
        grid: bool = USER_OPTIONS.launcher.grid,
        grid_columns: int = USER_OPTIONS.launcher.grid_columns,
    ):
        self.grid = grid
        self.apps: list[LauncherAppItem] = self._gen_apps()

        if self.grid:
            self._app_list = Widget.Grid(
                column_num=grid_columns,
                child=self.apps,
            )
        else:
            self._app_list = Widget.Box(
                vertical=True,
                child=self.apps,
            )

        applications.connect("notify::apps", lambda *_: self._sync())

        self._entry = Widget.Entry(
            hexpand=True,
            placeholder_text="Search...",
            on_change=self._search,
            on_accept=self._on_accept,
        )

        main_box = Widget.Box(
            vertical=True,
            valign=valign,
            halign=halign,
            css_classes=["launcher"],
            child=[
                Widget.Box(
                    css_classes=["launcher-search"],
                    child=[
                        Widget.Icon(
                            icon_name="system-search-symbolic",
                            style="margin-right: 0.5rem;",
                            pixel_size=24,
                        ),
                        self._entry,
                    ],
                ),
                Widget.Box(style="margin: 5px 0;"),
                Widget.Scroll(
                    height_request=450,
                    child=Widget.EventBox(
                        css_classes=["launcher-app-list"],
                        on_scroll_up=lambda _: self._entry.grab_focus(),
                        on_scroll_down=lambda _: self._entry.grab_focus(),
                        homogeneous=True,
                        child=[self._app_list],
                    ),
                ),
            ],
        )

        if self.grid:
            main_box.add_css_class("launcher-grid")

        super().__init__(
            namespace=ModuleWindow.LAUNCHER,
            setup=lambda self: self.connect("notify::visible", self._on_open),
            child=[main_box],
        )

    def _search(self, *_) -> None:
        query = self._entry.text

        if not query:
            self._app_list.child = self.apps
        else:
            apps = applications.search(applications.apps, query)

            if not apps:
                self._app_list.child = [SearchWebButton(query)]
            else:
                self._app_list.child = [LauncherAppItem(i, self.grid) for i in apps]

    def _gen_apps(self) -> list[LauncherAppItem]:
        return [LauncherAppItem(i, self.grid) for i in applications.apps]

    def _sync(self):
        self.apps = self._gen_apps()
        self._app_list.child = self.apps

    def _on_open(self, *_) -> None:
        if not self.visible:
            return

        self._entry.text = ""
        self._entry.grab_focus()

    def _on_accept(self, *_) -> None:
        if len(self._app_list.child) > 0:
            self._app_list.child[0].launch()
