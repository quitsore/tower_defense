import datetime
import pygame
from map import Map, Location, MapView, Tag
from monster import Monster
from castle import Castle
from map import Entity
from scene import Scene, Point
from player import Player
from the_game.info_panel import InfoPanel
from the_game.monster import State
from the_game.shop import Shop
from the_game.transaction import Transaction
from tower import Tower
import logging

logging.basicConfig(level=logging.DEBUG)


class Game:

    def __init__(self):
        self.mouse_cursor_image = None
        self.background = None
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
        self.background = pygame.surface.Surface([self.width, self.height])
        self.background.fill((0, 0, 0))
        self.player = Player(1000)
        self.scene = Scene(cell_width=40, cell_height=40)
        self.castle = Castle(MapView(self.game_map, Location(1, 22), width=1, height=1),
                             color=pygame.Color(255, 215, 0))
        self.time_for_next_monster = datetime.datetime.now()
        self.bullets = []
        self.monsters = []
        self.towers = []
        self.monster_index = 0
        self.wave_value = 50
        self.mouse_click_point = None
        self.mouse_point = None
        self.shop = Shop(self.player)
        self.text_font = pygame.font.SysFont("Arial", 30)
        self.info_panel = InfoPanel(self.player)
        self.transaction = None

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
        if not self.transaction:
            item = self.shop.action(self.mouse_click_point)
            if item:
                self.transaction = Transaction(item, self.player, self.scene, self.game_map)
        else:
            tower = self.transaction.action(self.mouse_point, not self.mouse_click_point is None)
            if tower:
                self.towers.append(tower)
                self.transaction = None
        self.info_panel.action()
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
                if cell.tag == Entity.MONSTER:
                    color = pygame.Color(93, 93, 93, 255)
                    pygame.draw.rect(self.screen, color,
                                     pygame.Rect(col_idx * 40, row_idx * 40, 40, 40))

    def show_fps(self):
        fps = int(self.clock.get_fps())
        show_fps = self.text_font.render(str(fps), True, (255, 255, 255))
        self.screen.blit(show_fps, (0, 0))

    def spawn_monster(self):
        if self.monster_index < self.wave_value:
            if self.time_for_next_monster <= datetime.datetime.now():
                self.monster_index += 1
                self.monsters.append(
                    Monster(map_view=MapView(self.game_map, Location(1, 0), width=3, height=3),
                            name=str(self.monster_index),
                            scene=self.scene))
                self.time_for_next_monster += datetime.timedelta(seconds=2)

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
