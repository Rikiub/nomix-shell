import os
from typing import Literal

from nomix.utils.constants import CACHE_DIR

COLOR_SCHEME = Literal["default", "prefer-light", "prefer-dark"]

STYLE_FILE = CACHE_DIR / "_dark.scss"

# Template for generated file
STYLE_DISCLAIMER = "DON'T MODIFY THIS FILE, WILL BE OVERWRITED"
STYLE_VARIABLE_NAME = "is-dark"

# Only adw-gtk3 supported because styles bugs
CHANGE_THEME = True
GTK_THEME_LIGHT = "adw-gtk3"
GTK_THEME_DARK = "adw-gtk3-dark"

CHANGE_ICON = False
GTK_ICON_LIGHT = os.getenv("GTK_ICON_LIGHT") or ""
GTK_ICON_DARK = os.getenv("GTK_ICON_DARK") or ""