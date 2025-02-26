import asyncio
import tempfile
from pathlib import Path
from typing import cast, get_args

from ignis.base_service import BaseService
from ignis.utils.shell import exec_sh_async
from ignis.utils.file_monitor import FileMonitor

from nomix.services.color_scheme.service import ColorSchemeService
from nomix.utils.constants import OVERRIDE_FILE
from nomix.utils.global_options import cache_options, user_options
from nomix.utils.helpers import send_notification
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

        if user_options.matugen.scheme not in schemes:
            text = f"{user_options.matugen.scheme} is not a valid matugen scheme, please check your config and restart Ignis again"
            send_notification(
                "Matugen Service Disabled", text, icon_name="dialog-warning"
            )
            return

        FileMonitor(
            path=str(SWWW_CACHE),
            callback=lambda monitor, path, event: self._on_update_wallpaper(
                monitor, path, event
            ),
        )

        if user_options.prefer_dark_shell:
            cache_options.theme_is_dark = True
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
            and user_options.matugen.scheme != cache_options.matugen_scheme
        ):
            self._update_and_apply_scheme(cache_options.wallpaper)
            cache_options.matugen_scheme = user_options.matugen.scheme

    def _on_update_wallpaper(self, monitor: FileMonitor, path: str, event: str):
        if event == "changes_done_hint":
            file = Path(path)

            if not file.is_file():
                return

            with file.open() as f:
                image = f.readline().strip()

            if image == cache_options.wallpaper:
                return
            cache_options.wallpaper = image

            self._update_and_apply_scheme(image)

    def _update_and_apply_scheme(self, image: StrPath):
        asyncio.create_task(self._gen_schemes(image)).add_done_callback(
            lambda _: self._override_styles(self._get_mode())
        )

        if user_options.matugen.run_user_config:
            asyncio.create_task(
                self._run_matugen(
                    image=image,
                    mode=self._get_mode(),
                    scheme=user_options.matugen.scheme,  # type: ignore
                    prefer_user_config=True,
                )
            )

    def _get_mode(self) -> MODE:
        return (
            "dark" if cache_options.theme_is_dark or color_scheme.is_dark else "light"
        )

    def _override_styles(self, mode: MODE):
        target = MATUGEN_DARK if mode == "dark" else MATUGEN_LIGHT
        content = target.read_text()

        OVERRIDE_FILE.write_text(content)

    async def _gen_schemes(self, image: StrPath):
        scheme = cast(MATUGEN_SCHEME, user_options.matugen.scheme)
        cache_options.matugen_scheme = scheme

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
                await exec_sh_async(
                    f"matugen {command} --mode {mode} --type {type} image {image}"
                )
            except Exception:
                if prefer_user_config:
                    send_notification(
                        "Invalid Matugen Config",
                        "Check <b>~/.config/matugen/config.toml</b> and try again.",
                    )
