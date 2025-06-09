import pygame
from scene import Point
from platformdirs import user_data_dir
from pathlib import Path
import tomllib


class MenuTile:
    def __init__(self, number, screen, block, x, y, size, text_font, col, row, image, is_unlocked):
        self.btn = None
        self.number = number
        self.rect = pygame.Rect(x, y, image.get_width(), image.get_height())
        self.screen = screen
        self.block = block
        self.x, self.y = x, y
        self.size = size
        self.text_font = text_font
        self.col, self.row = col, row
        self.cover = pygame.surface.Surface(image.get_size())
        self.cover.fill((255, 255, 255))
        self.cover.set_alpha(100)
        self.is_clicked = False
        self.is_unlocked = is_unlocked

    def action(self):
        pass

    def on_mouse_clicked_down(self):
        self.is_clicked = True

    def on_mouse_clicked_up(self):
        self.is_clicked = False

    def draw(self):
        extra = 0
        pygame.draw.rect(self.screen, (0, 0, 0),
                         pygame.Rect((self.col + 1) * 90 + self.size * self.col + 5,
                                     (self.row + 1) * 80 + self.size * self.row + 5, self.size, self.size))
        if self.is_clicked and self.is_unlocked:
            extra = 5
        self.screen.blit(self.block, (self.x + extra, self.y + extra))
        self._draw_text(self.screen, f"{self.number}", self.text_font, (255, 255, 255),
                        (self.col + 1) * 90 + self.size * self.col + self.size / 2 + extra,
                        (self.row + 1) * 80 + self.size * self.row + self.size / 2 + extra)
        if not self.is_unlocked:
            self.screen.blit(self.cover, (self.rect.x + extra, self.rect.y + extra))

    @staticmethod
    def _draw_text(screen, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        img_rect = img.get_rect(center=(x, y))
        screen.blit(img, (img_rect.x, img_rect.y))


class Menu:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.width, self.height = 1280, 720
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.mixer.music.load("../resources/menu_track.mp3")
        self.text_font = pygame.font.Font("../resources/MotionControl-Bold.otf", 50)
        self.text_font_project = pygame.font.Font("../resources/DAGGERSQUARE.otf", 22)
        self.logo = pygame.image.load("../resources/Title.png").convert()
        self.placement = pygame.image.load("../resources/brick-80x80.png").convert()
        self.exit_button = pygame.image.load("../resources/Exit_button.png").convert()
        self.is_work = True
        self.background = pygame.surface.Surface([self.width, self.height])
        self.background.fill((0, 0, 0))
        self.active_tile = None
        self.played = False
        self.app_name = "TowerDefense"
        data_dir = Path(user_data_dir(self.app_name, appauthor=False))
        data_dir.mkdir(parents=True, exist_ok=True)
        self.config_file = data_dir / "saves.toml"
        print(f"config file {self.config_file}")
        self.config = self.load_data()
        if self.config is None:
            last_unlocked_level = 1
        else:
            last_unlocked_level = self.config["levels"]["last_unlocked"]
        self.tiles = []
        level = 0
        self.size = 80
        self.space = 80
        self.left_space = 90
        for row in range(4):
            for col in range(5):
                level += 1
                x, y = (col + 1) * self.left_space + self.size * col, (row + 1) * self.space + self.size * row
                menu_tile = MenuTile(level, self.screen, self.placement, x, y, self.size, self.text_font, col, row,
                                     self.placement, level <= last_unlocked_level)
                self.tiles.append(menu_tile)

    def load_data(self):
        if self.config_file.exists():
            with open(self.config_file, "rb") as f:
                config = tomllib.load(f)
                return config
        return None

    def action(self):
        self.play_music()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_work = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                btn = pygame.mouse.get_pressed(num_buttons=3)
                if btn[0]:
                    pos = pygame.mouse.get_pos()
                    for tile in self.tiles:
                        if tile.rect.collidepoint(pos):
                            tile.on_mouse_clicked_down()
                            self.active_tile = tile
                            break

            if event.type == pygame.MOUSEBUTTONUP:
                if self.active_tile:
                    self.active_tile.on_mouse_clicked_up()
                    self.active_tile = None

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        pygame.draw.rect(self.screen, (0, 255, 0), pygame.Rect(0, 0, 960, 720))
        self.draw_levels()
        self.screen.blit(self.exit_button, (1040, 580))
        self.screen.blit(self.logo, (960, 0))
        self._draw_text(self.screen, "A school project", self.text_font_project, (255, 255, 255), 1120, 340)
        self._draw_text(self.screen, "by Robert Seifert", self.text_font_project, (255, 255, 255), 1120, 365)
        pygame.display.update()

    def run(self):
        while self.is_work:
            self.check_events()
            self.action()
            self.draw()

    def draw_levels(self):
        for tile in self.tiles:
            tile.draw()

    def play_music(self):
        if not pygame.mixer.music.get_busy() and not self.played:
            pygame.mixer.music.play()
            self.played = True
        elif not pygame.mixer.music.get_busy():
            pygame.mixer.music.play()
            pygame.mixer.music.set_pos(9.624)

    @staticmethod
    def _draw_text(screen, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        img_rect = img.get_rect(center=(x, y))
        screen.blit(img, (img_rect.x, img_rect.y))


menu = Menu()
menu.run()
