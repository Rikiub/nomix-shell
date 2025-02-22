from pathlib import Path
from typing import Literal
from ignis.utils.file_monitor import FileMonitor
from nomix.services.color_scheme.service import ColorSchemeService
from nomix.utils.constants import CACHE_DIR, USER_CACHE_DIR
from nomix.utils.user_options import cache_options, user_options

from ignis.base_service import BaseService
from ignis.utils.get_current_dir import get_current_dir
from ignis.utils.exec_sh import exec_sh_async, exec_sh

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
        self.matugen_template = CURRENT_DIR / "template.scss"

        self.matugen_config.write_text(MATUGEN_STRING)
        self.matugen_template.touch(exist_ok=True)

        self.swww_path = USER_CACHE_DIR / "swww"
        self.swww_current_image = self.get_current_image()

        FileMonitor(
            path=str(self.swww_path), recursive=True, callback=self.on_update_image
        )

        if user_options.force_dark_theme:
            cache_options.theme_dark = True

            if self.swww_current_image:
                self.generate_matugen(self.swww_current_image, "dark")
        else:
            color_scheme.connect(
                "notify::is-dark",
                lambda *_: self.swww_current_image
                and self.generate_matugen(
                    self.swww_current_image,
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
            self.swww_current_image = Path(image)

        self.generate_matugen(
            image,
            "dark" if cache_options.theme_dark or color_scheme.is_dark else "light",
        )

    def get_current_image(self) -> Path | None:
        output = exec_sh("swww query").stdout
        output = str(output)
        output = output.split("image:", 1)

        if output:
            image = output[1].strip()
            return Path(image)

        return None

    def generate_matugen(self, image: Path | str, mode: Literal["light", "dark"]):
        exec_sh_async(
            f"matugen --config {self.matugen_config} --mode {mode} image {image}"
        )
