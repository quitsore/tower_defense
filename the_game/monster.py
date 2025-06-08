from typing import List

import pygame
import enum
import logging

from map import Entity, Map
from map import MapView
from the_game.scene import Scene, Offset, Point
from pathlib import Path

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class State(enum.IntEnum):
    SPAWNING = 0
    SEARCHING = 1
    MOVING = 2
    HITTING = 3
    END_OF_LIVE = 4
    DEATH = 5


class Monster:

    def __init__(self, scene: Scene, map_view: MapView, index, monster_config, sprites, lag):
        self.entity = Entity.MONSTER
        self.index = index
        self.next_loc = None
        self.abs_speed = monster_config["speed"]
        self.speed = Offset()
        self.offset = Offset()
        self.scene = scene
        self.map_view = map_view
        self.map_view.register(self)
        self.state = State.SPAWNING
        self.trace = []
        self.state_counter = 0
        self.draw_counter = 0
        self.damage = monster_config["damage"]
        self.health = monster_config["health"]
        self.gold_value = monster_config["value"]
        self.attack_delay = monster_config["attack_speed"]
        self.hurt_counter = 0
        self.running_images = sprites["running"]
        self.hitting_images = sprites["hitting"]
        self.dying_images = sprites["dying"]
        self.hurting_images = sprites["hurting"]
        self.death_counter = 0
        self.lag = lag
        assert lag > 0

    def get_hit(self, damage):
        self.health -= damage
        self.hurt_counter = 20
        logger.info(f"{self.index} got hit by {damage} points. rest health = {self.health}")

    def is_alive(self) -> bool:
        return True if self.health > 0 else False

    def _transit(self, new_state: State):
        logger.info(f"Transiting from {self.state.name} to {new_state.name}")
        self.state = new_state
        self.state_counter = -1
        if new_state == State.DEATH:
            logger.info(f"{self.death_counter} dead")
            self.map_view.unregister(self)
        elif new_state == State.END_OF_LIVE:
            self.draw_counter = 0
            self.death_counter = self.get_death_counter()
            logger.info(f"{self.death_counter} death detected")

    def location(self):
        return self.map_view.center

    def point(self) -> Point:
        return self.scene.get_point(self.location(), self.offset)

    def center_point(self) -> Point:
        return self.point() + self.scene.cell_center()

    def running_image(self, draw_counter):
        return self.running_images[(draw_counter // self.lag) % len(self.running_images)]

    def hitting_image(self, draw_counter):
        return self.hitting_images[(draw_counter // self.lag) % len(self.hitting_images)]

    def dying_image(self, draw_counter):
        return self.dying_images[(draw_counter // self.lag) % len(self.dying_images)]

    def get_death_counter(self):
        return len(self.dying_images) * self.lag - self.lag

    def hurting_image(self, draw_counter):
        return self.hurting_images[(draw_counter // self.lag) % len(self.hurting_images)]

    def action(self):
        self.state_counter += 1
        loc = self.location()
        if self.state == State.SPAWNING:
            self._transit(State.SEARCHING)
        elif self.state == State.SEARCHING:
            if not self.is_alive():
                self._transit(State.END_OF_LIVE)
            else:
                next_loc = None
                for nl in filter(self.has_not_visited, loc.directions()):
                    if self.map_view.is_castle(nl):
                        next_loc = nl
                        self._transit(State.HITTING)
                    elif self.map_view.is_free(nl):
                        next_loc = nl
                        self._transit(State.MOVING)
                    if next_loc:
                        break
                if not next_loc:
                    raise Exception("Unexpectedly no available next location")
                else:
                    self.next_loc = next_loc
                    self.offset = Offset()
                    loc_diff = self.next_loc - loc
                    self.speed = Offset(dx=loc_diff.dcol * self.abs_speed, dy=loc_diff.drow * self.abs_speed)
        elif self.state == State.MOVING:
            if not self.is_alive():
                self._transit(State.END_OF_LIVE)
            else:
                next_offset = self.offset + self.speed
                if self.scene.out_of_cell_bounds(next_offset):
                    self.trace.append(self.location())
                    self.map_view.relocate(self.next_loc)
                    self.next_loc = None
                    self.offset = Offset()
                    self._transit(State.SEARCHING)
                else:
                    self.offset = next_offset
                    logger.debug(f"offset = {self.offset}")
        elif self.state == State.HITTING:
            if not self.is_alive():
                self._transit(State.END_OF_LIVE)
            else:
                castle = self.map_view.get_castle(self.next_loc)
                if self.state_counter % self.attack_delay == 0:
                    castle.get_hit(self.damage)
        elif self.state == State.DEATH:
            pass
        elif self.state == State.END_OF_LIVE:
            if self.death_counter > 0:
                self.death_counter -= 1
                logger.info(f"death counter reached {self.death_counter}")
            else:
                self._transit(State.DEATH)

    def draw(self, screen):
        self.draw_counter += 1
        loc = self.location()
        y = loc.row * self.scene.cell_height + self.offset.dy
        x = loc.col * self.scene.cell_width + self.offset.dx
        if self.state == State.SPAWNING:
            screen.blit(self.running_image(self.draw_counter), (x, y))
        elif self.state == State.MOVING or self.state == State.SEARCHING:
            if self.hurt_counter == 0:
                screen.blit(self.running_image(self.draw_counter), (x, y))
            else:
                screen.blit(self.hurting_image(self.draw_counter), (x, y))
                self.hurt_counter -= 1
        elif self.state == State.HITTING:
            screen.blit(self.hitting_image(self.draw_counter), (x, y))
        elif self.state == State.END_OF_LIVE:
            screen.blit(self.dying_image(self.draw_counter), (x, y))

    def has_not_visited(self, location):
        # check if location in trace
        if self.map_view.in_sight(location) and self.trace.count(location) == 0:
            return True
        else:
            return False

    def __str__(self):
        return f"monster: {self.index}, location: {self.location()}, offset: {self.offset}, health: {self.health}, entity: {self.entity}"


class Goblin(Monster):

    def __init__(self, scene: Scene, map_view: MapView, index, goblin_config, sprites, lag):
        super().__init__(scene, map_view, index, goblin_config, sprites, lag)


class Orc(Monster):
    def __init__(self, scene: Scene, map_view: MapView, index, orc_config, sprites, lag):
        super().__init__(scene, map_view, index, orc_config, sprites, lag)


class Spider(Monster):
    def __init__(self, scene: Scene, map_view: MapView, index, spider_config, sprites, lag):
        super().__init__(scene, map_view, index, spider_config, sprites, lag)


class MonsterFactory:

    def __init__(self, scene: Scene, monsters_config):
        self.scene = scene
        self.monsters_config = monsters_config
        self.spider_sprites = MonsterFactory.load_sprites(Path('../resources/spider'))
        self.goblin_sprites = MonsterFactory.load_sprites(Path('../resources/goblin'))
        self.orc_sprites = MonsterFactory.load_sprites(Path('../resources/orc'))

    def create_goblin(self, game_map, spawn_point, monster_index):
        return Goblin(map_view=MapView(game_map, spawn_point, width=3, height=3),
                      index=monster_index,
                      scene=self.scene,
                      goblin_config=self.monsters_config["goblin"],
                      sprites=self.goblin_sprites,
                      lag=2)

    def create_orc(self, game_map, spawn_point, monster_index):
        return Orc(map_view=MapView(game_map, spawn_point, width=3, height=3),
                   index=monster_index,
                   scene=self.scene,
                   orc_config=self.monsters_config["orc"],
                   sprites=self.orc_sprites,
                   lag=2)

    def create_spider(self, game_map, spawn_point, monster_index):
        return Spider(map_view=MapView(game_map, spawn_point, width=3, height=3),
                      index=monster_index,
                      scene=self.scene,
                      spider_config=self.monsters_config["spider"],
                      sprites=self.spider_sprites,
                      lag=1)

    @staticmethod
    def load_sprites(monster_dir: Path):
        sprites = {}
        running_dir = monster_dir / 'running'
        sprites["running"] = [pygame.image.load(running_dir / f.name).convert_alpha() for f in
                              MonsterFactory.sorted_files(running_dir)]
        hitting_dir = monster_dir / 'hitting'
        sprites["hitting"] = [pygame.image.load(hitting_dir / f.name).convert_alpha() for f in
                              MonsterFactory.sorted_files(hitting_dir)]
        hurting_dir = monster_dir / 'hurting'
        sprites["hurting"] = [pygame.image.load(hurting_dir / f.name).convert_alpha() for f in
                              MonsterFactory.sorted_files(hurting_dir)]
        dying_dir = monster_dir / 'dying'
        sprites["dying"] = [pygame.image.load(dying_dir / f.name).convert_alpha() for f in
                            MonsterFactory.sorted_files(dying_dir)]
        return sprites

    @staticmethod
    def sorted_files(files_dir: Path) -> List[Path]:
        files = sorted((f for f in
                        files_dir.iterdir() if f.is_file()), key=lambda f: f.name)
        return files
