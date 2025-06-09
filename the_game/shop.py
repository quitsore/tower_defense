import enum
import math

import pygame
from scene import Point


class ItemType(enum.IntEnum):
    STONE = 1
    METEOR = 2
    FIRE = 3


class Item:

    def __init__(self, item_type, available, price, point: Point, image):
        self.item_type = item_type
        self.available = available
        self.price = price
        self.rect = pygame.Rect(point.x, point.y, image.get_width(), image.get_height())
        self.image = image
        self.cover = pygame.surface.Surface(image.get_size())
        self.cover.fill((255, 255, 255))
        self.cover.set_alpha(100)

    def is_selected(self, mouse_click_position: Point) -> bool:
        return self.available and self.rect.collidepoint(mouse_click_position.x, mouse_click_position.y)

    def draw(self, screen):
        if not self.available:
            self.image.set_alpha(100)
        else:
            self.image.set_alpha(255)
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def __repr__(self):
        return f"item: available = {self.available}, price = {self.price}"


class Shop:

    def __init__(self, player, towers_config):
        self.items = {
            ItemType.STONE:
                Item(ItemType.STONE, True, towers_config["stone"]["price"], Point(1020, 250),
                     pygame.image.load("../resources/stone_tower/stone_turret0.png").convert_alpha()),
            ItemType.METEOR:
                Item(ItemType.METEOR, True, towers_config["meteor"]["price"], Point(1160, 250),
                     pygame.image.load("../resources/meteor_tower/meteor_turret0.png").convert_alpha()),
            ItemType.FIRE:
                Item(ItemType.FIRE, False, towers_config["fire"]["price"], Point(1105, 250),
                     pygame.image.load("../resources/bomb_01.png").convert_alpha())}

        self.text_font = pygame.font.Font("../resources/MotionControl-Bold.otf", 40)
        self.tower_shop = pygame.image.load("../resources/tower-32x40.png").convert()
        self.bomb_shop = pygame.image.load("../resources/bomb_01.png").convert()
        self.coin = pygame.image.load("../resources/coin.png").convert_alpha()
        self.player = player
        self.shop_open = False

    def action(self, mouse_click_point: Point, shop_open: bool):
        self.shop_open = shop_open
        for item in self.items.values():
            item.available = shop_open
        if shop_open and mouse_click_point:
            for item_type, item in self.items.items():
                if item.is_selected(mouse_click_point) and item.price <= self.player.gold:
                    return item
        return None

    def draw(self, screen):
        self._draw_text(screen, "Stone", self.text_font, (255, 255, 255), 1050, 330)
        self.items[ItemType.STONE].draw(screen)
        self.items[ItemType.METEOR].draw(screen)
        self._draw_text(screen, "Meteor", self.text_font, (255, 255, 255), 1190, 330)
        self._draw_text(screen, "30", self.text_font, (255, 255, 255), 1060, 365)
        self._draw_text(screen, "50", self.text_font, (255, 255, 255), 1200, 365)
        screen.blit(self.coin, (1010, 350))
        screen.blit(self.coin, (1150, 350))
        #        self._draw_text(screen, "Mortar", self.text_font, (255, 255, 255), 1030, 350)
        pygame.draw.line(screen, (255, 255, 255), (960, 207), (1280, 207), 3)
        pygame.draw.line(screen, (255, 255, 255), (960, 445), (1280, 445), 3)

    @staticmethod
    def _draw_text(screen, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        img_rect = img.get_rect(center=(x, y))
        screen.blit(img, (img_rect.x, img_rect.y))
