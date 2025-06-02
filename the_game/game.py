import datetime
import pygame
from map import Map, Location, MapView, Tag
from monster import Monster, Goblin, Orc
from castle import Castle
from map import Entity
from scene import Scene, Point
from player import Player
from the_game.info_panel import InfoPanel
from the_game.monster import State, Spider
from the_game.shop import Shop
from the_game.transaction import Transaction
from tower import Tower
import logging
import tomllib

logging.basicConfig(level=logging.DEBUG)


class Game:

    def __init__(self):
        self.mouse_cursor_image = None
        self.background = None
        self.config = None
        with open("game_config.toml", mode="rb") as fp:
            self.config = tomllib.load(fp)
        pygame.init()
        self.width, self.height = 1280, 720
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Tower defense")
        self.path = pygame.image.load("../resources/path-40x40.png").convert()
        self.grass = pygame.image.load("../resources/grass-40x40.png").convert()
        self.placement = pygame.image.load("../resources/brick-40x40.png").convert()
        self.cursorPX, self.curserPY = self.width // 2, self.height // 2
        self.clock = pygame.time.Clock()
        self.is_work = True
        self.timer = None
        self.FPS = 60
        self.game_map = Map("terrain.txt")
        self.spawn_point = self.game_map.find_spawn_point()
        self.background = pygame.surface.Surface([self.width, self.height])
        self.background.fill((0, 0, 0))
        self.player = Player(self.config["player"]["start_gold"])
        self.scene = Scene(cell_width=40, cell_height=40)
        castle_loc = self.game_map.find_castle_place()
        self.castle = Castle(MapView(self.game_map, castle_loc, width=1, height=1),
                             color=pygame.Color(0, 215, 0), scene=self.scene, castle_config=self.config)
        self.time_for_next_monster = None
        self.bullets = []
        self.monsters = []
        self.towers = []
        self.monster_index = 0
        self.mouse_click_point = None
        self.mouse_point = None
        self.shop = Shop(self.player, self.config["towers"])
        self.text_font = pygame.font.SysFont("Arial", 30)
        self.info_panel = InfoPanel(self.player)
        self.transaction = None
        self.shop_open = False
        self.waves = self.config["level1"]["waves"]
        self.wave = None

    def take_next_wave(self):
        wave = None
        if self.waves:
            wave = self.waves[0]
            self.waves = self.waves[1:]
        return wave

    def load_next_level(self):
        pass

    def draw(self):
        # clear screen
        self.screen.blit(self.background, (0, 0))
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
        # draw dynamics
        if self.transaction:
            self.transaction.draw(self.screen)

        # show fps
        self.show_fps()
        # pygame.display.flip()
        pygame.display.update()

    def check_events(self):
        self.mouse_click_point = None
        mouse_pos = pygame.mouse.get_pos()
        self.mouse_point = Point(mouse_pos[0], mouse_pos[1])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_work = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                btn = pygame.mouse.get_pressed(num_buttons=3)
                if btn[0]:
                    self.mouse_click_point = self.mouse_point
                if btn[2] and self.transaction:
                    self.transaction = None
                print(f"mouse clicked: {self.mouse_click_point}")

    def action(self):
        if len(self.monsters) == 0:
            if not self.shop_open:
                self.shop_open = True
                self.info_panel.init_counter(self.config["wave"]["shopping_time_s"])
                self.wave = self.take_next_wave()
                if not self.wave:
                    logging.warning("NEXT LEVEL")
                    exit(1)
        if not self.transaction:
            item = self.shop.action(mouse_click_point=self.mouse_click_point, shop_open=self.shop_open)
            if item:
                self.transaction = Transaction(item, self.player, self.scene, self.game_map, self.config["towers"])
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
            self.is_work = False

    def draw_map(self):
        color = None
        for row_idx, row in enumerate(self.game_map.map):
            for col_idx, cell in enumerate(row):
                if cell.tag == Tag.FREE:
                    self.screen.blit(self.path, (col_idx * 40, row_idx * 40))
                elif cell.tag == Tag.TERRAIN:
                    self.screen.blit(self.grass, (col_idx * 40, row_idx * 40))
                elif cell.tag == Tag.TOWER:
                    self.screen.blit(self.placement, (col_idx * 40, row_idx * 40))
                elif cell.tag == Tag.CASTLE:
                    self.castle.draw(self.screen)
                elif cell.tag == Tag.SPAWN_POINT:
                    self.screen.blit(self.path, (col_idx * 40, row_idx * 40))

    def show_fps(self):
        fps = int(self.clock.get_fps())
        show_fps = self.text_font.render(str(fps), True, (255, 255, 255))
        self.screen.blit(show_fps, (0, 0))

    def spawn_monster(self):
        now = datetime.datetime.now()
        if self.time_for_next_monster and now >= self.time_for_next_monster:
            if self.wave:
                monster_type = self.wave[0]
                self.wave = self.wave[1:]
            else:
                monster_type = None
            if monster_type == "G":
                self.monsters.append(
                    Goblin(map_view=MapView(self.game_map, self.spawn_point, width=3, height=3),
                           index=self.monster_index,
                           scene=self.scene,
                           goblin_config=self.config["monsters"]["goblin"], color=(255, 0, 0)))
            elif monster_type == "O":
                self.monsters.append(
                    Orc(map_view=MapView(self.game_map, self.spawn_point, width=3, height=3),
                        index=self.monster_index,
                        scene=self.scene,
                        orc_config=self.config["monsters"]["orc"], color=(0, 255, 0)))
            elif monster_type == "S":
                self.monsters.append(
                    Spider(map_view=MapView(self.game_map, self.spawn_point, width=3, height=3),
                           index=self.monster_index,
                           scene=self.scene,
                           spider_config=self.config["monsters"]["spider"], color=(0, 0, 255)))

            self.monster_index += 1
            if monster_type is None:
                self.time_for_next_monster = None
            else:
                self.time_for_next_monster += datetime.timedelta(milliseconds=self.config["wave"]["period_ms"])

    def remove_dead_monsters(self):
        for monster in self.monsters:
            if monster.state == State.DEATH:
                self.player.gold += monster.gold_value
                self.monsters.remove(monster)

    def run(self):
        while self.is_work:
            self.check_events()
            self.remove_dead_monsters()
            self.spawn_monster()
            self.action()
            self.draw()
            self.clock.tick(self.FPS)
        print("Game over")


game = Game()
game.run()
