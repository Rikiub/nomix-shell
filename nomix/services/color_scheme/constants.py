import os
from typing import Literal

COLOR_SCHEME = Literal["default", "prefer-light", "prefer-dark"]

# Template for generated file
STYLE_VARIABLE_NAME = "DARK"

# Only adw-gtk3 supported because styles bugs
CHANGE_THEME = True
GTK_THEME_LIGHT = "adw-gtk3"
GTK_THEME_DARK = "adw-gtk3-dark"

CHANGE_ICON = False
GTK_ICON_LIGHT = os.getenv("GTK_ICON_LIGHT") or ""
GTK_ICON_DARK = os.getenv("GTK_ICON_DARK") or ""
