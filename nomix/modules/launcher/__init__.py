import asyncio
import re

from gi.repository import Gtk  # type: ignore
from ignis.app import IgnisApp
from ignis.menu_model import IgnisMenuItem, IgnisMenuModel, IgnisMenuSeparator
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

class BaseItem(Widget.Button):
    def __init__(
        self,
        icon_name: str = "",
        label: str = "",
        vertical: bool = False,
        css_classes: list[str] = [],
        **kwargs,
    ):
        super().__init__(
            css_classes=["app-item", *css_classes],
            child=Widget.Box(
                vertical=vertical,
                valign="center",
                child=[
                    Widget.Icon(image=icon_name, pixel_size=48),
                    Widget.Label(
                        label=label,
                        ellipsize="end",
                        max_width_chars=30,
                    ),
                ],
            ),
            **kwargs,
        )


class AppItem(BaseItem):
    def __init__(self, application: Application, vertical: bool = False) -> None:
        self._application = application

        super().__init__(
            icon_name=application.icon,
            label=application.name,
            vertical=vertical,
            on_click=lambda _: self.launch(),
            on_right_click=lambda _: self._menu.popup(),
            tooltip_text=application.name if vertical else None,
        )
        self._sync_menu()
        self._application.connect("notify::is-pinned", lambda *_: self._sync_menu())

    def launch(self) -> None:
        self._application.launch()
        app.close_window(ModuleWindow.LAUNCHER)

    def launch_action(self, action: ApplicationAction) -> None:
        action.launch()
        app.close_window(ModuleWindow.LAUNCHER)

    def _sync_menu(self) -> None:
        pin = None

        if PIN_APPS:
            pin = IgnisMenuItem(
                label="Unpin" if self._application.is_pinned else "Pin",
                on_activate=lambda _: self._application.unpin()
                if self._application.is_pinned
                else self._application.pin(),
            )

        self._menu = Widget.PopoverMenu(
            model=IgnisMenuModel(
                IgnisMenuItem(label="Launch", on_activate=lambda _: self.launch()),
                pin,  # type: ignore
                IgnisMenuSeparator(),
                *(
                    IgnisMenuItem(
                        label=i.name,
                        on_activate=lambda _, action=i: self.launch_action(action),
                    )
                    for i in self._application.actions
                ),
            )
        )
        self.child.append(self._menu)


def _get_default_browser_icon() -> str:
    desktop = exec_sh("xdg-settings get default-web-browser").stdout.strip()
    desktop = str(desktop).strip(".desktop")

    if icon := get_app_icon_name(desktop):
        return icon
    else:
        return ""


class SearchWebItem(BaseItem):
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
            icon_name=self.icon,
            label=label,
            on_click=lambda _: self.launch(),
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
    def __init__(self, valign: ALIGN = "start", halign: ALIGN = "center"):
        self._items: list[AppItem] = self._generate_items(applications.apps)

        self._layout = Widget.Box()
        self._scroll = Widget.EventBox(
            css_classes=["app-list"],
            homogeneous=True,
            on_scroll_up=lambda _: self._entry.grab_focus(),
            on_scroll_down=lambda _: self._entry.grab_focus(),
            child=[self._layout],
        )

        self._entry = Widget.Entry(
            placeholder_text="Search...",
            hexpand=True,
            on_change=lambda _: self._search(),
            on_accept=lambda _: self._on_accept(),
        )

        self._window_box = Widget.Box(
            css_classes=["launcher"],
            vertical=True,
            child=[
                Widget.Box(
                    css_classes=["search-entry"],
                    child=[
                        Widget.Icon(
                            icon_name="system-search-symbolic",
                            pixel_size=24,
                        ),
                        self._entry,
                    ],
                ),
                Widget.Scroll(height_request=450, child=self._scroll),
            ],
        )

        super().__init__(
            valign=valign,
            halign=halign,
            namespace=ModuleWindow.LAUNCHER,
            setup=lambda self: self.connect(
                "notify::visible", lambda *_: self._on_open()
            ),
            child=[self._window_box],
        )

        applications.connect("notify::apps", lambda *_: self._sync_items())
        self._update_layout()
        """
        USER_OPTIONS.launcher.connect_option("grid", lambda *_: self._update_layout())  # type: ignore
        USER_OPTIONS.launcher.connect_option(
            "grid_columns", lambda *_: self._update_layout()
        )  # type: ignore
        """

        def on_keypressed(event_key, keyval: int, keycode: int, state):
            if keycode not in (111, 113, 114, 116):
                self._entry.grab_focus_without_selecting()

        key_controller = Gtk.EventControllerKey()
        self.add_controller(key_controller)
        key_controller.connect("key-pressed", on_keypressed)

    def _search(self) -> None:
        query = self._entry.text

        if not query:
            self._layout.child = self._items
        else:
            apps = applications.search(applications.apps, query)

            if not apps:
                self._layout.child = [SearchWebItem(query)]
            else:
                self._layout.child = self._generate_items(apps)

    def _on_open(self) -> None:
        if not self.visible:
            return

        self._entry.text = ""
        self._entry.grab_focus()

    def _on_accept(self) -> None:
        if len(self._layout.child) > 0:
            self._layout.child[0].launch()

    def _update_layout(self):
        css_class = "grid"

        if USER_OPTIONS.launcher.grid:
            self._window_box.add_css_class(css_class)
            self._layout = Widget.Grid(
                column_num=USER_OPTIONS.launcher.grid_columns, child=self._items
            )
        else:
            self._window_box.remove_css_class(css_class)
            self._layout = Widget.Box(vertical=True, child=self._items)

        self._scroll.child = [self._layout]

    def _generate_items(self, source: list[Application]) -> list[AppItem]:
        return [AppItem(i, USER_OPTIONS.launcher.grid) for i in source]

    def _sync_items(self):
        self._items = self._generate_items(applications.apps)
        self._layout.child = self._items
