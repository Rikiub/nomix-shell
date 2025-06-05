from typing import Callable, Generic, Type, TypeVar
from gi.repository import Gio, Gtk  # type: ignore

from ignis.base_widget import BaseWidget
from ignis.gobject import IgnisProperty


T = TypeVar(name="T")


class GridLayout(Generic[T], Gtk.GridView, BaseWidget):  # type: ignore
    def __init__(
        self,
        items: Type[T] | list[T],
        on_setup: Callable[[], BaseWidget],
        on_bind: Callable[[BaseWidget, T], None],
        on_activate: Callable[[T], None] | None = None,
        on_change: Callable[[], None] | None = None,
        filter: Callable[[str, T], bool] | None = None,
        **kwargs,
    ):
        if isinstance(items, list):
            self._store = Gio.ListStore(item_type=type(items[0]))
            self.update_items(items)
        else:
            self._store = Gio.ListStore(item_type=items)

        self._on_setup = on_setup
        self._on_bind = on_bind
        self._on_activate = on_activate
        self._on_change = on_change
        self._filter_func = filter

        self._factory = Gtk.SignalListItemFactory()
        self._factory.connect("setup", lambda _, item: self._on_factory_setup(item))
        self._factory.connect("bind", lambda _, item: self._on_factory_bind(item))

        self._filter = Gtk.CustomFilter()
        self._filter_model = Gtk.FilterListModel(model=self._store, filter=self._filter)
        self._selection_model = Gtk.SingleSelection(model=self._filter_model)

        Gtk.GridView.__init__(
            self,
            model=self._selection_model,
            factory=self._factory,
        )
        BaseWidget.__init__(self, **kwargs)

        self.connect("activate", self._activate)

    @IgnisProperty
    def on_activate(self) -> Callable[[T], None] | None:
        return self._on_activate

    @IgnisProperty
    def selected(self) -> T:
        position = self._selection_model.get_selected()
        item = self._filter_model.get_item(position)
        return item  # type: ignore

    @IgnisProperty
    def selected_position(self) -> int:  # type: ignore
        return self._selection_model.get_selected()

    @selected_position.setter
    def selected_position(self, position: int):
        self._selection_model.set_selected(position)

    def update_items(self, items: list[T]):
        self._store.remove_all()

        for i in items:
            self._store.append(i)  # type: ignore

    def search(self, search: str):
        if func := self._filter_func:
            self._filter.set_filter_func(lambda item: func(search, item))

        if self._on_change:
            self._on_change()

    def _activate(self, grid_view, position: int):
        if item := self._filter_model.get_item(position):
            if self._on_activate:
                self._on_activate(item)  # type: ignore

    def _on_factory_setup(self, list_item: Gtk.ListItem):
        list_item.set_child(self._on_setup())

    def _on_factory_bind(self, list_item: Gtk.ListItem):
        widget = list_item.get_child()
        item = list_item.get_item()

        if not (widget or item):
            raise ValueError()

        self._on_bind(widget, item)  # type: ignore
