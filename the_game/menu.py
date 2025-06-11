import pygame
from scene import Point
from platformdirs import user_data_dir
from pathlib import Path
import tomllib


class MenuTile:
    def __init__(self, number, menu, screen, x, y, size, text_font, col, row):
        self.btn = None
        self.menu = menu
        self.number = number
        self.image = pygame.image.load("../resources/brick-80x80.png").convert()
        self.rect = pygame.Rect(x, y, self.image.get_width(), self.image.get_height())
        self.screen = screen
        self.x, self.y = x, y
        self.size = size
        self.text_font = text_font
        self.col, self.row = col, row
        self.cover = pygame.surface.Surface(self.image.get_size())
        self.cover.fill((255, 255, 255))
        self.cover.set_alpha(100)
        self.is_clicked = False
        self.is_unlocked = False

    def action(self):
        pass

    def on_mouse_clicked_down(self):
        self.is_clicked = True

    def on_mouse_clicked_up(self, on_tile):
        self.is_clicked = False
        if on_tile and self.is_unlocked:
            self.menu.on_selected(self.number)

    def draw(self):
        extra = 0
        pygame.draw.rect(self.screen, (0, 0, 0),
                         pygame.Rect((self.col + 1) * 90 + self.size * self.col + 5,
                                     (self.row + 1) * 80 + self.size * self.row + 5, self.size, self.size))
        if self.is_clicked and self.is_unlocked:
            extra = 5
        self.screen.blit(self.image, (self.x + extra, self.y + extra))
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


class ExitButton:

    def __init__(self, x, y):
        self.image = pygame.image.load("../resources/Exit_button.png").convert()
        self.rect = pygame.Rect(x, y, self.image.get_width(), self.image.get_height())

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))


class HelpButton:

    def __init__(self, x, y):
        self.image = pygame.image.load("../resources/Help_button.png").convert()
        self.rect = pygame.Rect(x, y, self.image.get_width(), self.image.get_height())

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))


class Menu:
    def __init__(self, screen):
        self.screen = screen
        pygame.mixer.music.load("../resources/menu_track.mp3")
        self.text_font = pygame.font.Font("../resources/MotionControl-Bold.otf", 50)
        self.text_font_project = pygame.font.Font("../resources/DAGGERSQUARE.otf", 22)
        self.logo = pygame.image.load("../resources/Title.png").convert()
        self.exit_button = ExitButton(1040, 580)
        self.help_button = HelpButton(1040, 480)
        self.active_tile = None
        self.played = False
        self.tiles = []
        level = 0
        self.size = 80
        self.space = 80
        self.left_space = 90
        self.is_completed = False
        self.selected_level = None
        self.show_help = False
        for row in range(4):
            for col in range(5):
                level += 1
                x, y = (col + 1) * self.left_space + self.size * col, (row + 1) * self.space + self.size * row
                menu_tile = MenuTile(number=level, menu=self, screen=self.screen, x=x, y=y,
                                     size=self.size, text_font=self.text_font, col=col, row=row)
                self.tiles.append(menu_tile)

    def on_activate(self, level):
        self.is_completed = False
        self.selected_level = None
        for i in range(level):
            self.tiles[i].is_unlocked = True

    def on_selected(self, level):
        self.selected_level = level
        self.is_completed = True
        self.played = False

    def action(self):
        self.play_music()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                btn = pygame.mouse.get_pressed(num_buttons=3)
                if btn[0]:
                    pos = pygame.mouse.get_pos()
                    if self.show_help:
                        self.show_help = False
                    elif self.exit_button.rect.collidepoint(pos):
                        return False
                    elif self.help_button.rect.collidepoint(pos):
                        self.show_help = True
                    else:
                        for tile in self.tiles:
                            if tile.rect.collidepoint(pos):
                                tile.on_mouse_clicked_down()
                                self.active_tile = tile
                                break

            if event.type == pygame.MOUSEBUTTONUP:
                if self.active_tile:
                    pos = pygame.mouse.get_pos()
                    on_tile = self.active_tile.rect.collidepoint(pos)
                    self.active_tile.on_mouse_clicked_up(on_tile)
                    self.active_tile = None
        return True

    def draw(self):
        pygame.draw.rect(self.screen, (0, 255, 0), pygame.Rect(0, 0, 960, 720))
        self.draw_levels()
        self.help_button.draw(self.screen)
        self.exit_button.draw(self.screen)
        self.screen.blit(self.logo, (960, 0))
        self._draw_text(self.screen, "A school project", self.text_font_project, (255, 255, 255), 1120, 340)
        self._draw_text(self.screen, "by Robert Seifert", self.text_font_project, (255, 255, 255), 1120, 365)
        if self.show_help:
            self._draw_text(self.screen, "Help!", self.text_font_project, (255, 255, 255), 120, 340)

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
