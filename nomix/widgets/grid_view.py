from typing import Callable, Generic, TypeVar
from gi.repository import Gio, Gtk  # type: ignore

from ignis.base_widget import BaseWidget


class SearchEntry(Gtk.SearchEntry, BaseWidget):  # type: ignore
    def __init__(self, **kwargs):
        Gtk.SearchEntry.__init__(self)
        BaseWidget.__init__(self, **kwargs)


T = TypeVar(name="T")


class GridLayout(Generic[T], Gtk.GridView, BaseWidget):  # type: ignore
    def __init__(
        self,
        items: list[T],
        setup: Callable[[], BaseWidget],
        bind: Callable[[BaseWidget, T], None],
        filter: Callable[[str, T], bool] | None = None,
        **kwargs,
    ):
        self.search_entry = Gtk.SearchEntry()
        self.search_entry.connect("search-changed", self._on_search_changed)

        self._store = Gio.ListStore(item_type=type(items[0]))
        self._filter = Gtk.CustomFilter()

        self._setup = setup
        self._bind = bind
        self._filter_func = filter

        self._factory = Gtk.SignalListItemFactory()
        self._factory.connect("setup", lambda _, item: self._on_factory_setup(item))
        self._factory.connect("bind", lambda _, item: self._on_factory_bind(item))

        Gtk.GridView.__init__(
            self,
            css_classes=["grid-view"],
            model=Gtk.NoSelection(
                model=Gtk.FilterListModel(
                    model=self._store,
                    filter=self._filter,
                )
            ),
            factory=self._factory,
        )
        BaseWidget.__init__(self, **kwargs)

        for i in items:
            self._store.append(i)  # type: ignore

    def _on_factory_setup(self, list_item: Gtk.ListItem):
        list_item.set_child(self._setup())

    def _on_factory_bind(self, list_item: Gtk.ListItem):
        widget = list_item.get_child()
        item = list_item.get_item()

        if not (widget or item):
            raise ValueError()

        self._bind(widget, item)  # type: ignore

    def _on_search_changed(self, entry):
        if func := self._filter_func:
            self._filter.set_filter_func(
                lambda item, text=entry.get_text(): func(entry.get_text(), item)
            )
