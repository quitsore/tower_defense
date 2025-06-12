import tomllib
import tomli_w
from pathlib import Path

import pygame
from platformdirs import user_data_dir

from .game import Game
from .menu import Menu
from .paths import *

FPS = 60
APP_NAME = "TowerDefense"


class AppConfig:

    def __init__(self, app_name):
        self.app_name = app_name
        data_dir = Path(user_data_dir(self.app_name, appauthor=False))
        data_dir.mkdir(parents=True, exist_ok=True)
        self.save_config_file = data_dir / "saves.toml"
        self.save_config = self.load_save_config()
        self.game_config = self.load_game_config()

    def load_save_config(self):
        if self.save_config_file.exists():
            with open(self.save_config_file, "rb") as f:
                config = tomllib.load(f)
                return config
        else:
            return {"levels": {"last_unlocked": 1}}

    def load_game_config(self):
        with open(CONFIG_DIR / "game_config.toml", mode="rb") as fp:
            game_config = tomllib.load(fp)
            return game_config

    def get_last_unlocked_level(self):
        return self.save_config["levels"]["last_unlocked"]

    def set_last_unlocked_level(self, level):
        self.save_config["levels"]["last_unlocked"] = level
        toml_str = tomli_w.dumps(self.save_config)
        with open(self.save_config_file, "w", encoding="utf-8") as f:
            f.write(toml_str)

    def level_completed(self, level):
        if level == self.get_last_unlocked_level():
            self.set_last_unlocked_level(level + 1)


class App:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Tower Defense")
        pygame.mixer.init()
        self.clock = pygame.time.Clock()
        self.width, self.height = 1280, 720
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.background = pygame.surface.Surface([self.width, self.height])
        self.background.fill((0, 0, 0))
        self.app_config = AppConfig(APP_NAME)
        self.menu = Menu(screen=self.screen)
        self.game = Game(screen=self.screen, config=self.app_config.game_config)
        self.activity = self.menu
        self.activity.on_activate(level=self.app_config.get_last_unlocked_level())
        self.current_level = None
        self.played = False

    def select_activity(self):
        if self.activity.is_completed:
            pygame.mixer.music.unload()
            self.played = False
            if type(self.activity) is Menu:
                pygame.mixer.music.load(AUDIO_DIR / "battle_music.mp3")
                self.current_level = self.activity.selected_level
                level = self.current_level
                self.activity = self.game
            elif type(self.activity) is Game:
                if self.activity.succeeded:
                    self.app_config.level_completed(self.current_level)
                    self.current_level = None
                level = self.app_config.get_last_unlocked_level()
                self.activity = self.menu
                pygame.mixer.music.load(AUDIO_DIR / "menu_track.mp3")
            else:
                raise NotImplementedError()
            self.activity.on_activate(level)

    def check_events(self):
        return self.activity.check_events()

    def action(self):
        self.activity.action()
        self.play_music()

    def play_music(self):
        if not pygame.mixer.music.get_busy() and not self.played:
            pygame.mixer.music.play()
            self.played = True
        elif not pygame.mixer.music.get_busy():
            pygame.mixer.music.play()
            pygame.mixer.music.set_pos(9.624)

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.activity.draw()
        pygame.display.update()

    def run(self):
        while True:
            self.select_activity()
            if not self.check_events():
                break
            self.action()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()


def main():
    app = App()
    app.run()


if __name__ == "__main__":
    main()
