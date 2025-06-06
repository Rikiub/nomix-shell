import asyncio
import tempfile
from pathlib import Path
from typing import cast, get_args

from ignis import utils
from ignis.base_service import BaseService

from nomix.services.color_scheme.service import ColorSchemeService
from nomix.utils.constants import OVERRIDE_FILE
from nomix.utils.helpers import do_niri_transition, send_notification
from nomix.utils.options import CACHE_OPTIONS, USER_OPTIONS
from nomix.utils.types import StrPath

from .constants import (
    CURRENT_DIR,
    MATUGEN_DARK,
    MATUGEN_LIGHT,
    MATUGEN_SCHEME,
    MODE,
    SWWW_CACHE,
)

color_scheme = ColorSchemeService.get_default()
schemes = get_args(MATUGEN_SCHEME)


class MatugenService(BaseService):
    def __init__(self) -> None:
        super().__init__()

        utils.FileMonitor(
            path=str(SWWW_CACHE),
            callback=lambda monitor, path, event: self._on_update_wallpaper(
                monitor, path, event
            ),
        )

        # Dark theme
        def update_preference():
            if USER_OPTIONS.prefer_dark_shell:
                CACHE_OPTIONS.theme_is_dark = True
                self._override_styles("dark")
            else:
                CACHE_OPTIONS.theme_is_dark = False
                self._override_styles(self._get_mode())

        update_preference()
        USER_OPTIONS.connect_option("prefer_dark_shell", lambda *_: update_preference())

        color_scheme.connect(
            "notify::is-dark",
            lambda *_: not CACHE_OPTIONS.theme_is_dark
            and self._override_styles(self._get_mode()),
        )

        # Scheme
        def update_scheme():
            if (
                CACHE_OPTIONS.wallpaper
                and USER_OPTIONS.matugen.scheme != CACHE_OPTIONS.matugen_scheme
            ):
                if USER_OPTIONS.matugen.scheme not in schemes:
                    text = f"{USER_OPTIONS.matugen.scheme} is not a valid matugen scheme, please check your config and try again"
                    send_notification("Matugen Error", text, icon_name="dialog-warning")
                    return

                self._update_and_apply_scheme(CACHE_OPTIONS.wallpaper)
                CACHE_OPTIONS.matugen_scheme = USER_OPTIONS.matugen.scheme

        update_scheme()
        USER_OPTIONS.matugen.connect_option("scheme", lambda *_: update_scheme())

    def _on_update_wallpaper(self, monitor: utils.FileMonitor, path: str, event: str):
        if event == "changes_done_hint":
            file = Path(path)

            if not file.is_file():
                return

            with file.open() as f:
                lines = f.readlines()

                if len(lines) >= 2:
                    image = lines[1].strip()
                else:
                    return

            if image == CACHE_OPTIONS.wallpaper:
                return

            CACHE_OPTIONS.wallpaper = image

            self._update_and_apply_scheme(image)

    def _update_and_apply_scheme(self, image: StrPath):
        def callback():
            do_niri_transition()
            self._override_styles(self._get_mode())

        asyncio.create_task(self._gen_schemes(image)).add_done_callback(
            lambda _: callback()
        )

        if USER_OPTIONS.matugen.run_user_config:
            asyncio.create_task(
                self._run_matugen(
                    image=image,
                    mode=self._get_mode(),
                    scheme=USER_OPTIONS.matugen.scheme,  # type: ignore
                    prefer_user_config=True,
                )
            )

    def _get_mode(self) -> MODE:
        return (
            "dark" if CACHE_OPTIONS.theme_is_dark or color_scheme.is_dark else "light"
        )

    def _override_styles(self, mode: MODE):
        target = MATUGEN_DARK if mode == "dark" else MATUGEN_LIGHT
        content = target.read_text()

        OVERRIDE_FILE.write_text(content)

    async def _gen_schemes(self, image: StrPath):
        scheme = cast(MATUGEN_SCHEME, USER_OPTIONS.matugen.scheme)
        CACHE_OPTIONS.matugen_scheme = scheme

        light = self._run_matugen(image, "light", scheme)
        dark = self._run_matugen(image, "dark", scheme)

        await light
        await dark

    async def _run_matugen(
        self,
        image: StrPath,
        mode: MODE,
        scheme: MATUGEN_SCHEME,
        prefer_user_config: bool = False,
    ):
        type = "scheme-" + scheme

        with tempfile.NamedTemporaryFile() as f:
            command = ""

            if not prefer_user_config:
                template = f"""
                [config]

                [templates.ignis]
                input_path = '{CURRENT_DIR}/template.scss'
                output_path = '{MATUGEN_DARK if mode == "dark" else MATUGEN_LIGHT}'
                """

                path = Path(f.name)
                path.write_text(template)

                command = f"--config '{path}'"

            try:
                await utils.exec_sh_async(
                    f"matugen {command} --mode {mode} --type {type} image {image}"
                )
            except Exception:
                if prefer_user_config:
                    send_notification(
                        "Invalid Matugen Config",
                        "Check <b>~/.config/matugen/config.toml</b> and try again.",
                    )
