from pathlib import Path

# __file__ → .../src/tower_defense/paths.py
# parents[2] → project root (tower_defense/)
BASE_DIR = Path(__file__).resolve().parent
RESOURCES_DIR = BASE_DIR / "resources"
IMAGES_DIR = RESOURCES_DIR / "images"
FONTS_DIR = RESOURCES_DIR / "fonts"
TERRAINS_DIR = RESOURCES_DIR / "terrains"
AUDIO_DIR = RESOURCES_DIR / "audio"
CONFIG_DIR = RESOURCES_DIR / "config"
