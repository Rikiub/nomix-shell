import asyncio
from pathlib import Path
import tempfile
from typing import cast, get_args

from ignis.base_service import BaseService
from ignis.utils.exec_sh import exec_sh_async
from ignis.utils.file_monitor import FileMonitor

from nomix.services.color_scheme.service import ColorSchemeService
from nomix.utils.constants import OVERRIDE_FILE
from nomix.utils.helpers import send_notification
from nomix.utils.types import StrPath
from nomix.utils.user_options import cache_options, user_options

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

        if user_options.matugen.scheme not in schemes:
            text = f"{user_options.matugen.scheme} is not a valid matugen scheme, please check your config and restart Ignis again"
            send_notification(
                "Matugen Service Disabled", text, icon_name="dialog-warning"
            )

            return

        FileMonitor(path=str(SWWW_CACHE), callback=self._on_update_wallpaper)

        if user_options.force_dark_theme:
            cache_options.force_dark = True
            color_scheme._update_style()

            self._override_styles("dark")
        else:
            color_scheme.connect(
                "notify::is-dark",
                lambda *_: self._override_styles(
                    "dark" if color_scheme.is_dark else "light"
                ),
            )

        if (
            cache_options.wallpaper
            and cache_options.matugen_scheme != user_options.matugen.scheme
        ):
            self._update_and_apply_scheme(cache_options.wallpaper)
            cache_options.matugen_scheme = user_options.matugen.scheme

    def _override_styles(self, mode: MODE):
        target = MATUGEN_DARK if mode == "dark" else MATUGEN_LIGHT
        content = target.read_text()

        OVERRIDE_FILE.write_text(content)

    def _on_update_wallpaper(self, event: FileMonitor, path: str, _):
        file = Path(path)

        if not file.is_file():
            return

        with file.open() as f:
            image = f.readline().strip()
            cache_options.wallpaper = image

        self._update_and_apply_scheme(image)

    def _update_and_apply_scheme(self, image: StrPath):
        asyncio.create_task(self._gen_schemes(image)).add_done_callback(
            lambda _: self._override_styles(
                "dark" if cache_options.force_dark or color_scheme.is_dark else "light"
            )
        )

    async def _gen_schemes(self, image: StrPath):
        scheme = cast(MATUGEN_SCHEME, user_options.matugen.scheme)
        cache_options.matugen_scheme = scheme

        light = self._run_matugen(image, "light", scheme)
        dark = self._run_matugen(image, "dark", scheme)

        await light
        await dark

    async def _run_matugen(self, image: StrPath, mode: MODE, scheme: MATUGEN_SCHEME):
        config = f"""
        [config]

        [templates.ignis]
        input_path = '{CURRENT_DIR}/template.scss'
        output_path = '{MATUGEN_DARK if mode == "dark" else MATUGEN_LIGHT}'
        """

        type = "scheme-" + scheme

        with tempfile.NamedTemporaryFile() as f:
            Path(f.name).write_text(config)

            await exec_sh_async(
                f"matugen --config {f.name} --mode {mode} --type {type} image {image}"
            )
