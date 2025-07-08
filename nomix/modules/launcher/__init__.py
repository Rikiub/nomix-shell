from gi.repository import Gdk, GLib, Gtk  # type: ignore
from ignis import widgets
from ignis.gobject import Binding
from ignis.menu_model import IgnisMenuItem, IgnisMenuModel, IgnisMenuSeparator
from ignis.services.applications import (
    Application,
    ApplicationAction,
    ApplicationsService,
)
from ignis.window_manager import WindowManager

from nomix.utils.constants import NAVIGATION_KEYS, ModuleWindow
from nomix.utils.options import USER_OPTIONS
from nomix.utils.types import ALIGN
from nomix.widgets.popup_window import PopupWindow
from nomix.widgets.search_entry import SearchEntry
from nomix.widgets.view import GridView

window_manager = WindowManager.get_default()
applications = ApplicationsService.get_default()

PIN_APPS = False


def launch_app(app: Application):
    app.launch()
    window_manager.close_window(ModuleWindow.LAUNCHER)


class AppItem(widgets.Box):
    def __init__(
        self,
        application: Application | None = None,
        css_classes: list[str] = [],
        **kwargs,
    ) -> None:
        self.icon = widgets.Icon(pixel_size=48)
        self.title = widgets.Label(
            wrap=True,
            wrap_mode="word_char",
            justify="center",
            ellipsize="end",
            lines=2,
        )
        self.menu = widgets.PopoverMenu()

        super().__init__(
            valign="center",
            css_classes=["app-item", *css_classes],
            child=[self.icon, self.title, self.menu],
            **kwargs,
        )

        if application:
            self.update(application)

    def launch_action(self, action: ApplicationAction) -> None:
        action.launch()
        window_manager.close_window(ModuleWindow.LAUNCHER)

    def update(self, app: Application):
        self.icon.image = app.icon
        self.title.label = app.name
        self.tooltip_text = app.name if self.vertical else None

        self.on_click = lambda _: launch_app(app)
        self.on_right_click = lambda _: self.menu.popup()

        self._update_menu(app)

    def _update_menu(self, app: Application) -> None:
        self.menu.model = IgnisMenuModel(
            IgnisMenuItem(label="Launch", on_activate=lambda _: launch_app(app)),
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


class Launcher(PopupWindow):
    def __init__(self, valign: ALIGN = "start", halign: ALIGN = "center"):
        def filters(search: str, app: Application):
            search = search.lower()

            if search in app.name.lower():
                return True
            if any(search in key.lower() for key in app.keywords):
                return True

            return False

        def on_change():
            self._grid.selected_position = 0

            def scroll_callback():
                vadj = self._scroll.get_vadjustment()
                vadj.set_value(0)
                return GLib.SOURCE_REMOVE

            GLib.idle_add(scroll_callback)

        self._grid = GridView(
            item_type=Application,
            on_setup=lambda: AppItem(vertical=USER_OPTIONS.launcher.grid),
            on_bind=lambda widget, app: widget.update(app),
            on_activate=lambda app: launch_app(app),
            on_change=on_change,
        )

        applications.connect(
            "notify::apps",
            lambda *_: self._grid.update_items(applications.apps),
        )

        self._search_entry = SearchEntry(
            placeholder_text="Search...",
            css_classes=["search-entry"],
            on_accept=lambda _: launch_app(self._grid.selected),
            on_change=lambda _: self._grid.search(self._search_entry.text, filters),
        )
        self._scroll = widgets.Scroll(
            css_classes=["scroll-container"],
            valign="center",
            vexpand=True,
            child=self._grid,
            visible=self._grid.bind(
                "total_items",
                lambda v: v != 0,
            ),
        )

        hidder: Binding = self._grid.bind("total_items", lambda v: v == 0)
        self._placeholder = widgets.Revealer(
            css_classes=["placeholder"],
            transition_type="crossfade",
            transition_duration=300,
            reveal_child=hidder,
            visible=hidder,
            child=widgets.Box(
                vertical=True,
                vexpand=True,
                hexpand=True,
                valign="center",
                halign="center",
                child=[
                    widgets.Icon(image="search-symbolic", pixel_size=80),
                    widgets.Label(label="No Results Found"),
                ],
            ),
        )

        super().__init__(
            valign=valign,
            halign=halign,
            namespace=ModuleWindow.LAUNCHER,
            on_close=lambda: self._search_entry.set_text(""),
            css_classes=[
                "launcher",
                "grid" if USER_OPTIONS.launcher.grid else "",
            ],
            child=[
                self._search_entry,
                self._scroll,
                self._placeholder,
            ],
        )

        key_controller = Gtk.EventControllerKey()
        key_controller.connect(
            "key-pressed",
            self._on_search_key_pressed,
        )
        self._search_entry.add_controller(key_controller)

        key_controller = Gtk.EventControllerKey()
        key_controller.connect(
            "key-pressed",
            self._on_key_pressed,
        )
        self.add_controller(key_controller)

        self.connect("notify::visible", lambda *_: self._on_open())

    def _on_open(self) -> None:
        if not self.visible:
            return

        self._search_entry.text = ""
        self._search_entry.grab_focus()

    def _on_search_key_pressed(self, controller, keyval, keycode, state):
        if keyval == Gdk.KEY_KP_Enter:
            self._grid.selected.launch()

        if keyval == Gdk.KEY_Escape:
            window_manager.close_window(ModuleWindow.LAUNCHER)

    def _on_key_pressed(self, controller, keyval, keycode, state):
        if keyval in NAVIGATION_KEYS:
            return

        unichar = Gdk.keyval_to_unicode(keyval)

        if unichar > 0:
            self._search_entry.grab_focus()

            current: str = self._search_entry.get_text()
            position = self._search_entry.get_position()

            if keyval == Gdk.KEY_BackSpace:
                new = current[:-1]
            else:
                char = chr(unichar)
                new = current[:position] + char + current[position:]

            self._search_entry.set_text(new)
            self._search_entry.set_position(position + 1)
