from pathlib import Path

import sys
from pathlib import Path

# When frozen by PyInstaller, extract path via _MEIPASS:
if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys._MEIPASS)
else:
    # normal package layout:
    BASE_DIR = Path(__file__).resolve().parent

RESOURCES_DIR = BASE_DIR / "resources"
IMAGES_DIR = RESOURCES_DIR / "images"
FONTS_DIR = RESOURCES_DIR / "fonts"
TERRAINS_DIR = RESOURCES_DIR / "terrains"
AUDIO_DIR = RESOURCES_DIR / "audio"
CONFIG_DIR = RESOURCES_DIR / "config"
