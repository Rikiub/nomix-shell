import asyncio
import random
import re

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
from nomix.widgets.grid_view import GridLayout
from nomix.widgets.popup_window import PopupWindow

ignis_app = IgnisApp.get_default()
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
        self.icon = Widget.Icon(image=icon_name, pixel_size=48)
        self.text_label = Widget.Label(
            label=label,
            ellipsize="end",
            max_width_chars=30,
        )
        self.menu = Widget.PopoverMenu()

        super().__init__(
            css_classes=["app-item", *css_classes],
            child=Widget.Box(
                vertical=vertical,
                valign="center",
                child=[self.icon, self.text_label, self.menu],
            ),
            **kwargs,
        )


class AppItem(BaseItem):
    def __init__(
        self,
        application: Application | None = None,
        vertical: bool = False,
    ) -> None:
        self._vertical = vertical
        super().__init__(vertical=self._vertical)

        if application:
            self.update(application)

    def launch(self, app: Application) -> None:
        app.launch()
        ignis_app.close_window(ModuleWindow.LAUNCHER)

    def launch_action(self, action: ApplicationAction) -> None:
        action.launch()
        ignis_app.close_window(ModuleWindow.LAUNCHER)

    def update(self, app: Application):
        self.icon.icon_name = app.icon
        self.text_label.label = app.name
        self.tooltip_text = app.name if self._vertical else None

        self.on_click = lambda _: self.launch(app)
        self.on_right_click = lambda _: self.menu.popup()

        self._update_menu(app)

    def _update_menu(self, app: Application) -> None:
        self.menu.model = IgnisMenuModel(
            IgnisMenuItem(label="Launch", on_activate=lambda _: self.launch(app)),
            IgnisMenuItem(
                label="Unpin" if app.is_pinned else "Pin",
                on_activate=lambda _: app.unpin() if app.is_pinned else app.pin(),
            )
            if PIN_APPS
            else None,  # type: ignore
            IgnisMenuSeparator(),
            *(
                IgnisMenuItem(
                    label=i.name,
                    on_activate=lambda *_: self.launch_action(i),
                )
                for i in app.actions
            ),
        )

        if PIN_APPS:
            app.connect("notify::is-pinned", lambda *_: self._update_menu(app))


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
        ignis_app.close_window(ModuleWindow.LAUNCHER)


class Launcher(PopupWindow):
    def __init__(self, valign: ALIGN = "start", halign: ALIGN = "center"):
        def filters(search: str, app: Application):
            search = search.lower()

            if search in app.name.lower():
                return True
            if any(search in key.lower() for key in app.keywords):
                return True

            return False

        self._grid = GridLayout(
            applications.apps,
            setup=lambda: AppItem(vertical=USER_OPTIONS.launcher.grid),
            bind=lambda widget, app: widget.update(app),
            filter=filters,
        )

        self._search_entry = self._grid.search_entry
        self._search_entry.add_css_class("search-entry")
        self._search_entry.set_placeholder_text("Search...")

        super().__init__(
            valign=valign,
            halign=halign,
            namespace=ModuleWindow.LAUNCHER,
            css_classes=["launcher"],
            on_close=lambda: self._search_entry.set_text(""),
            child=[
                self._search_entry,
                Widget.Scroll(css_classes=["scroll-container"], child=self._grid),
            ],
        )

        if USER_OPTIONS.launcher.grid:
            self.panel.add_css_class("grid")

        self.connect("notify::visible", lambda *_: self._on_open())

    def _on_open(self) -> None:
        if not self.visible:
            return

        self._search_entry.set_text("")
        self._search_entry.grab_focus()

    def _on_accept(self) -> None:
        if len(self._layout.child) > 0:
            self._layout.child[0].launch()
