import enum
from pathlib import Path
from typing import List

import pygame

from .bullet import Bullet
from .map import MapView, Entity, Location
import logging

from .paths import *

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class State(enum.IntEnum):
    SEARCHING = 1
    SHOOTING = 2
    RELOADING = 3


class Tower:
    def __init__(self, map_view: MapView, images, scene, owner, tower_config, lag, bullet_lag):
        self.entity = Entity.TOWER
        self.state_counter = 0
        self.map_view = map_view
        self.map_view.register(self)
        self.images = images
        self.scene = scene
        self.owner = owner
        self.state = State.SEARCHING
        self.target = None
        self.reloading_counter = 0
        self.reloading_duration = tower_config["attack_speed_ms"]
        self.damage = tower_config["damage"]
        self.draw_counter = 0
        self.lag = lag
        self.bullet_lag = bullet_lag

    def location(self) -> Location:
        return self.map_view.center

    def action(self) -> Bullet | None:
        self.state_counter += 1
        if self.state == State.SEARCHING:
            monsters = list(filter(lambda m: m.is_alive(), self.map_view.find(Entity.MONSTER)))
            if monsters:
                # find first monster
                self.state = State.SHOOTING
                target = None
                for monster in monsters:
                    print(monster.index)
                    if not target or monster.index < target:
                        target = monster.index
                        self.target = monster
                logger.debug(f"Found monster: {self.target}")
            return None
        elif self.state == State.SHOOTING:
            if self.map_view.in_sight(self.target.location()) and self.target.is_alive():
                logger.debug(f"Shooting monster: {self.target}")
                self.state = State.RELOADING
                # shoot
                return Bullet(self.damage, self.images["bullet"], self.location(), self.scene, self.target,
                              self.bullet_lag)
            else:
                self.target = None
                self.state = State.SEARCHING
                return None
        elif self.state == State.RELOADING:
            self.reloading_counter += 1
            if self.reloading_counter == self.reloading_duration:
                self.reloading_counter = 0
                self.state = State.SHOOTING
            return None
        return None

    def draw(self, screen):
        self.draw_counter += 1
        p = self.scene.get_point(self.map_view.center)
        screen.blit(self.images["tower"][(self.draw_counter // self.lag) % len(self.images)], (p.x, p.y))


class StoneTower(Tower):

    def __init__(self, map_view, images, scene, owner, stone_tower_config, lag):
        super().__init__(map_view, images, scene, owner, stone_tower_config, lag, bullet_lag=5)


class MeteorTower(Tower):

    def __init__(self, map_view, images, scene, owner, meteor_tower_config, lag):
        super().__init__(map_view, images, scene, owner, meteor_tower_config, lag, bullet_lag=6)


class TowerFactory:

    def __init__(self, scene, owner, towers_config):
        self.scene = scene
        self.owner = owner
        self.towers_config = towers_config
        self.meteor_tower_sprites = {"tower": TowerFactory.load_sprites(IMAGES_DIR / "meteor_tower"),
                                     "bullet": {"bullet": pygame.image.load(IMAGES_DIR / "meteor.png").convert_alpha(),
                                                "explosion": TowerFactory.load_sprites(
                                                    IMAGES_DIR / "meteor-explosion")}}
        self.stone_tower_sprites = {"tower": TowerFactory.load_sprites(IMAGES_DIR / "stone_tower"),
                                    "bullet": {"bullet": pygame.image.load(IMAGES_DIR / "stone.png").convert_alpha(),
                                               "explosion": TowerFactory.load_sprites(
                                                   IMAGES_DIR / "stone-explosion")}}

    def create_meteor_tower(self, game_map, loc):
        return MeteorTower(map_view=MapView(game_map=game_map, center=loc, width=self.towers_config["meteor"]["range"],
                                            height=self.towers_config["meteor"]["range"]),
                           images=self.meteor_tower_sprites,
                           meteor_tower_config=self.towers_config["meteor"],
                           scene=self.scene,
                           owner=self.owner,
                           lag=8)

    def create_stone_tower(self, game_map, loc):
        return StoneTower(map_view=MapView(game_map=game_map, center=loc, width=self.towers_config["stone"]["range"],
                                           height=self.towers_config["stone"]["range"]),
                          images=self.stone_tower_sprites,
                          stone_tower_config=self.towers_config["stone"],
                          scene=self.scene,
                          owner=self.owner,
                          lag=8)

    @staticmethod
    def load_sprites(tower_dir: Path):
        sprites = [pygame.image.load(tower_dir / f.name).convert_alpha() for f in
                   TowerFactory.sorted_files(tower_dir)]
        return sprites

    @staticmethod
    def sorted_files(files_dir: Path) -> List[Path]:
        files = sorted((f for f in
                        files_dir.iterdir() if f.is_file()), key=lambda f: f.name)
        return files
