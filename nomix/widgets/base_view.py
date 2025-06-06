from typing import Callable, Generic, TypeVar

from gi.repository import Gio, Gtk  # type: ignore
from ignis.base_widget import BaseWidget
from ignis.gobject import IgnisProperty

T = TypeVar(name="T")


class BaseView(Generic[T], BaseWidget):
    def __init__(
        self,
        item_type: type[T],
        on_setup: Callable[[], BaseWidget],
        on_bind: Callable[[BaseWidget, T], None],
        on_activate: Callable[[T], None] | None = None,
        on_change: Callable[[], None] | None = None,
        items: list[T] = [],
        **kwargs,
    ):
        self._store = Gio.ListStore(item_type=item_type)
        self.update_items(items)

        self._on_setup = on_setup
        self._on_bind = on_bind
        self._on_activate = on_activate
        self._on_change = on_change

        self._factory = Gtk.SignalListItemFactory()
        self._factory.connect("setup", self._setup)
        self._factory.connect("bind", self._bind)

        self._filter = Gtk.CustomFilter()
        self._filter_model = Gtk.FilterListModel(
            model=self._store,
            filter=self._filter,
        )
        self._selection_model = Gtk.SingleSelection(model=self._filter_model)

        super().__init__(model=self._selection_model, factory=self._factory, **kwargs)

        self.connect("activate", self._activate)

    def _setup(self, view, list_item: Gtk.ListItem):
        list_item.set_child(self._on_setup())

    def _bind(self, view, list_item: Gtk.ListItem):
        widget = list_item.get_child()
        item = list_item.get_item()

        if not (widget or item):
            raise ValueError()

        self._on_bind(widget, item)  # type: ignore

    def _activate(self, view, position):
        if item := self._filter_model.get_item(position):
            if f := self._on_activate:
                f(item)  # type: ignore

    def append_item(self, item: T):
        self._store.append(item)  # type: ignore

        self._total_items += 1
        self.notify("total_items")

    def remove_item(self, item: T):
        exists, position = self._store.find(item)  # type: ignore

        if exists:
            self._store.remove(position)

            self._total_items -= 1
            self.notify("total_items")

    def update_items(self, items: list[T]):
        self._store.remove_all()
        self._total_items = 0

        for i in items:
            self._store.append(i)  # type: ignore
            self._total_items += 1

        self.notify("total_items")

    def search(self, search: str, filter: Callable[[str, T], bool]):
        self._filter.set_filter_func(lambda item: filter(search, item))

        self._total_items = self._filter_model.get_n_items()
        self.notify("total_items")

        if f := self._on_change:
            f()


class GridView(Gtk.GridView, BaseView):  # type: ignore
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @IgnisProperty
    def on_activate(self) -> Callable[[T], None] | None:  # type: ignore
        return self._on_activate

    @IgnisProperty
    def total_items(self) -> int:
        return self._total_items

    @IgnisProperty
    def selected(self):
        position = self._selection_model.get_selected()
        item = self._filter_model.get_item(position)
        return item  # type: ignore

    @IgnisProperty
    def selected_position(self) -> int:  # type: ignore
        return self._selection_model.get_selected()

    @selected_position.setter
    def selected_position(self, position: int):
        self._selection_model.set_selected(position)


class ListView(Gtk.ListView, BaseView):  # type: ignore
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @IgnisProperty
    def on_activate(self) -> Callable[[T], None] | None:  # type: ignore
        return self._on_activate

    @IgnisProperty
    def total_items(self) -> int:
        return self._total_items

    @IgnisProperty
    def selected(self):
        position = self._selection_model.get_selected()
        item = self._filter_model.get_item(position)
        return item  # type: ignore

    @IgnisProperty
    def selected_position(self) -> int:  # type: ignore
        return self._selection_model.get_selected()

    @selected_position.setter
    def selected_position(self, position: int):
        self._selection_model.set_selected(position)
