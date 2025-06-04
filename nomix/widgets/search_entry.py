from typing import Callable

from gi.repository import Gtk  # type: ignore
from ignis.base_widget import BaseWidget
from ignis.gobject import IgnisProperty


class SearchEntry(Gtk.SearchEntry, BaseWidget):  # type: ignore
    def __init__(
        self,
        on_accept: Callable | None = None,
        on_change: Callable | None = None,
        **kwargs,
    ):
        Gtk.SearchEntry.__init__(self)
        self._on_accept = on_accept
        self._on_change = on_change
        BaseWidget.__init__(self, **kwargs)

        self.connect(
            "activate",
            lambda x: self.on_accept(x) if self.on_accept else None,
        )
        self.connect(
            "search-changed",
            lambda x: self.on_change(x) if self.on_change else None,
        )

    @IgnisProperty
    def on_accept(self) -> Callable:  # type: ignore
        """
        The function that will be called when the user hits the Enter key.
        """
        return self._on_accept  # type: ignore

    @on_accept.setter
    def on_accept(self, value: Callable) -> None:
        self._on_accept = value

    @IgnisProperty
    def on_change(self) -> Callable:  # type: ignore
        """
        The function that will be called when the text in the widget is changed (e.g., when the user types something into the entry).
        """
        return self._on_change  # type: ignore

    @on_change.setter
    def on_change(self, value: Callable) -> None:
        self._on_change = value
