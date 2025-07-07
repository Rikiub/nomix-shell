from __future__ import annotations

import asyncio
from dataclasses import dataclass

from gi.repository import Gio  # type: ignore
from ignis import utils
from ignis.app import IgnisApp
from ignis.services.niri import NiriService
from ignis.utils.shell import exec_sh_async

from nomix.utils.constants import USER_CONFIG_DIR

app = IgnisApp.get_initialized()
niri = NiriService.get_default()


def monitor_gtk4_css():
    """Auto reload ignis on ~/.config/gtk-4.0/gtk.css changes"""

    utils.FileMonitor(
        str(USER_CONFIG_DIR / "gtk-4.0" / "gtk.css"),
        callback=lambda *_: app.reload(),
    )


def send_notification(title: str, message: str, icon_name: str = ""):
    asyncio.create_task(
        exec_sh_async(
            f"notify-send --app-name 'Ignis' --icon '{icon_name}' '{title}' '{message}'"
        )
    )


def do_niri_transition():
    if niri.is_available:
        asyncio.create_task(exec_sh_async("niri msg action do-screen-transition"))


@dataclass
class AppInfo:
    name: str
    icon: str
    description: str

    @property
    def symbolic_icon(self):
        if self.icon:
            return self.icon + "-symbolic"
        else:
            return None

    @classmethod
    def from_app_name(cls, app_name: str) -> AppInfo | None:
        if desktop := cls._get_desktop_info(app_name):
            return cls(
                desktop.get_name(),
                desktop.get_string("Icon") or "",
                desktop.get_description() or "",
            )

    @classmethod
    def _get_desktop_info(cls, name: str) -> Gio.DesktopAppInfo | None:
        try:
            desktop = Gio.DesktopAppInfo.new(f"{name}.desktop")
        except TypeError:
            return None

        if not desktop:
            return None

        return desktop
