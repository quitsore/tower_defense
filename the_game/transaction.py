from operator import truediv

import pygame

from the_game.map import Map, MapView, Entity
from the_game.scene import Point, Scene
from the_game.shop import ItemType
from the_game.tower import Tower, StoneTower, MeteorTower, TowerFactory


class Transaction:
    def __init__(self, item, player, scene: Scene, game_map: Map, tower_factory: TowerFactory):
        self.item = item
        self.player = player
        self.game_map = game_map
        self.mouse_cursor_image = None
        self.cover = None
        self.scene = scene
        self.change_cursor(self.item.image)
        self.on_tower_placement = False
        self.tower_factory = tower_factory

    def __del__(self):
        self.change_cursor(None)

    def confirm(self):
        self.player.spend_gold(self.item.price)

    def change_cursor(self, image):
        if image:
            # pygame.mouse.set_visible(False)
            self.cover = pygame.surface.Surface(image.get_size())
            self.cover.fill((255, 255, 255))
            self.cover.set_alpha(100)
            self.mouse_cursor_image = image
        else:
            pygame.mouse.set_visible(True)
            self.mouse_cursor_image = None
            self.cover = None

    def action(self, mouse_point: Point, clicked: bool):
        loc = self.scene.get_location(mouse_point)
        if self.game_map.on_map(loc):
            # we need to know if location belongs to tower placement
            # if so, set self.on_tower_placement to remove cover from the cursor
            self.on_tower_placement = self.game_map.is_tower_placement(loc)
            placement_is_free = len(self.game_map.cell(loc).get_entity(Entity.TOWER)) == 0
            if self.on_tower_placement and clicked and placement_is_free:
                self.confirm()
                return self.spawn_item(loc, self.item)
        return None

    def spawn_item(self, loc, item):
        if item.item_type == ItemType.STONE:
            return self.tower_factory.create_stone_tower(game_map=self.game_map, loc=loc)
        elif item.item_type == ItemType.METEOR:
            return self.tower_factory.create_meteor_tower(game_map=self.game_map, loc=loc)
        return None

    def draw(self, screen):
        if self.mouse_cursor_image:
            screen.blit(self.mouse_cursor_image, pygame.mouse.get_pos())
            if self.on_tower_placement:
                screen.blit(self.cover, pygame.mouse.get_pos())
