import logging
import tomllib
from copy import deepcopy

logging.basicConfig(level=logging.INFO)

import datetime
import pygame
from .map import Map, MapView, Tag
from .monster import MonsterFactory, State
from .castle import Castle
from .scene import Scene, Point
from .player import Player
from .info_panel import InfoPanel
from .shop import Shop
from .transaction import Transaction
from .tower import TowerFactory
from .paths import *


class Game:

    def __init__(self, screen, config):
        self.mouse_cursor_image = None
        self.config = config
        self.screen = screen
        self.path = pygame.image.load(IMAGES_DIR / "brick-60x60.png").convert()
        self.grass = pygame.image.load(IMAGES_DIR / "grass-60x60.png").convert()
        self.placement = pygame.image.load(IMAGES_DIR / "brick3-60x60.png").convert()
        self.defeat = pygame.image.load(IMAGES_DIR / "defeat.png").convert_alpha()
        self.mission_completed = pygame.image.load(IMAGES_DIR / "mission_completed.png").convert_alpha()
        self.game_map = None
        self.spawn_point = None
        self.player = Player(self.config["player"]["start_gold"])
        self.scene = Scene(cell_width=60, cell_height=60)
        self.monster_factory = MonsterFactory(self.scene, self.config["monsters"])
        self.tower_factory = TowerFactory(scene=self.scene, owner=self.player, towers_config=self.config["towers"])
        self.castle = None
        self.time_for_next_monster = None
        self.bullets = []
        self.monsters = []
        self.towers = []
        self.monster_index = 0
        self.mouse_click_point = None
        self.mouse_point = None
        self.shop = Shop(self.player, self.config["towers"])
        self.info_panel = None
        self.transaction = None
        self.shop_open = False
        self.waves = None
        self.wave = None
        self.is_completed = False
        self.is_game_over = False
        self.succeeded = False

    def on_activate(self, level):
        self.is_completed = False
        self.succeeded = False
        self.is_game_over = False
        self.load_next_level(level)

    def game_over(self, succeeded):
        self.is_game_over = True
        self.succeeded = succeeded
        self.info_panel.action()
        self.bullets = []

    def load_next_level(self, level):
        level_tag = f"level{level}"
        if level_tag in self.config:
            level_cfg = self.config[level_tag]
            self.player.gold = level_cfg["gold"]
            self.game_map = Map(TERRAINS_DIR / level_cfg["map"])
            self.spawn_point = self.game_map.find_spawn_point()
            castle_loc = self.game_map.find_castle_place()
            self.castle = Castle(MapView(self.game_map, castle_loc, width=1, height=1),
                                 color=pygame.Color(0, 215, 0), scene=self.scene, castle_config=self.config)
            self.info_panel = InfoPanel(self.player, self.screen, self.castle, level)
            self.waves = deepcopy(level_cfg["waves"])
            self.wave = None
            self.towers = []
            self.monsters = []

    def take_next_wave(self):
        wave = None
        print(self.waves)
        if self.waves:
            wave = self.waves[0]
            self.waves.pop(0)
        return wave

    def draw(self):
        # draw map
        self.draw_map()
        self.shop.draw(self.screen)
        # draw side panel
        self.info_panel.draw(self.screen)
        for monster in self.monsters:
            monster.draw(self.screen)
        for tower in self.towers:
            tower.draw(self.screen)
        for bullet in self.bullets:
            bullet.draw(self.screen)
        self.castle.draw(self.screen)
        # draw dynamics
        if self.transaction:
            self.transaction.draw(self.screen)
        if self.is_game_over:
            if self.succeeded:
                self.screen.blit(self.mission_completed, (224, 200))
            else:
                self.screen.blit(self.defeat, (224, 200))

    def check_events(self):
        self.mouse_click_point = None
        mouse_pos = pygame.mouse.get_pos()
        self.mouse_point = Point(mouse_pos[0], mouse_pos[1])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                btn = pygame.mouse.get_pressed(num_buttons=3)
                if btn[0]:
                    self.mouse_click_point = self.mouse_point
                if btn[2] and self.transaction:
                    self.transaction = None
                if self.is_game_over:
                    self.is_completed = True
        return True

    def action(self):
        if self.is_game_over:
            return
        self.remove_dead_monsters()
        self.spawn_monster()
        if len(self.monsters) == 0:
            if not self.shop_open:
                self.wave = self.take_next_wave()
                if not self.wave:
                    self.game_over(succeeded=True)
                else:
                    self.shop_open = True
                    self.info_panel.init_counter(self.config["wave"]["shopping_time_s"])
        if not self.transaction:
            item = self.shop.action(mouse_click_point=self.mouse_click_point, shop_open=self.shop_open)
            if item:
                self.transaction = Transaction(item, self.player, self.scene, self.game_map, self.tower_factory)
        else:
            tower = self.transaction.action(self.mouse_point, not self.mouse_click_point is None)
            if tower:
                self.towers.append(tower)
                self.transaction = None
        is_timer_over = self.info_panel.action()
        if is_timer_over and self.shop_open:
            self.shop_open = False
            self.time_for_next_monster = datetime.datetime.now()
        for monster in self.monsters:
            monster.action()
        for tower in self.towers:
            bullet = tower.action()
            if bullet:
                self.bullets.append(bullet)
        for bullet in self.bullets:
            bullet.action()
        self.castle.action()
        if self.castle.is_destroyed():
            self.game_over(succeeded=False)
            self.info_panel.action()

    def draw_map(self):
        for row_idx, row in enumerate(self.game_map.map):
            for col_idx, cell in enumerate(row):
                if cell.tag == Tag.FREE:
                    self.screen.blit(self.path, (col_idx * self.scene.cell_width, row_idx * self.scene.cell_height))
                elif cell.tag == Tag.TERRAIN or cell.tag == Tag.CASTLE:
                    self.screen.blit(self.grass, (col_idx * self.scene.cell_width, row_idx * self.scene.cell_height))
                elif cell.tag == Tag.TOWER:
                    self.screen.blit(self.placement,
                                     (col_idx * self.scene.cell_width, row_idx * self.scene.cell_height))
                elif cell.tag == Tag.SPAWN_POINT:
                    self.screen.blit(self.path, (col_idx * self.scene.cell_width, row_idx * self.scene.cell_height))

    def spawn_monster(self):
        now = datetime.datetime.now()
        if self.time_for_next_monster and now >= self.time_for_next_monster:
            if self.wave:
                monster_type = self.wave[0]
                self.wave = self.wave[1:]
            else:
                monster_type = None
            monster = None
            if monster_type == "G":
                monster = self.monster_factory.create_goblin(self.game_map, self.spawn_point, self.monster_index)
            elif monster_type == "O":
                monster = self.monster_factory.create_orc(self.game_map, self.spawn_point, self.monster_index)
            elif monster_type == "S":
                monster = self.monster_factory.create_spider(self.game_map, self.spawn_point, self.monster_index)
            if monster_type is None:
                self.time_for_next_monster = None
            else:
                assert monster is not None
                self.monster_index += 1
                self.monsters.append(monster)
                self.time_for_next_monster += datetime.timedelta(milliseconds=self.config["wave"]["period_ms"])

    def remove_dead_monsters(self):
        for monster in self.monsters:
            if monster.state == State.DEATH:
                self.player.gold += monster.gold_value
                self.monsters.remove(monster)
