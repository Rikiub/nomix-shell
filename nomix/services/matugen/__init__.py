from pathlib import Path
import asyncio
from typing import Literal
from ignis.utils.file_monitor import FileMonitor
from nomix.services.color_scheme.service import ColorSchemeService
from nomix.utils.constants import CACHE_DIR, USER_CACHE_DIR
from nomix.utils.user_options import cache_options, user_options

from ignis.base_service import BaseService
from ignis.utils.exec_sh import exec_sh_async
from ignis.utils.get_current_dir import get_current_dir

color_scheme = ColorSchemeService.get_default()

CURRENT_DIR = Path(get_current_dir())
MATUGEN_STRING = f"""
[config]

[templates.ignis]
input_path = '{CURRENT_DIR}/template.scss'
output_path = '{CACHE_DIR}/override.scss'
"""


class MatugenService(BaseService):
    def __init__(self) -> None:
        super().__init__()

        self.matugen_config = CURRENT_DIR / "config.toml"
        self.matugen_config.write_text(MATUGEN_STRING)

        self.swww_cache = USER_CACHE_DIR / "swww"
        self.wallpaper = cache_options.last_wallpaper

        FileMonitor(
            path=str(self.swww_cache),
            callback=self.on_update_image,
            recursive=True,
        )

        if user_options.force_dark_theme:
            cache_options.theme_dark = True

            if self.wallpaper:
                self.generate_matugen(self.wallpaper, "dark")
        else:
            color_scheme.connect(
                "notify::is-dark",
                lambda *_: self.wallpaper
                and self.generate_matugen(
                    self.wallpaper,
                    "dark"
                    if cache_options.theme_dark or color_scheme.is_dark
                    else "light",
                ),
            )

    def on_update_image(self, event: FileMonitor, path: str, _):
        file = Path(path)

        if not file.is_file():
            return

        with file.open() as f:
            image = f.readline().strip()

            cache_options.last_wallpaper = image
            self.wallpaper = Path(image)

        self.generate_matugen(
            image,
            "dark" if cache_options.theme_dark or color_scheme.is_dark else "light",
        )

    def generate_matugen(self, image: Path | str, mode: Literal["light", "dark"]):
        asyncio.create_task(
            exec_sh_async(
                f"matugen --config {self.matugen_config} --mode {mode} image {image}"
            )
        )
