import enum
import pygame

from the_game.bullet import Bullet
from the_game.map import MapView, Entity, Location
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class State(enum.IntEnum):
    SEARCHING = 1
    SHOOTING = 2
    RELOADING = 3


class Tower:
    def __init__(self, map_view: MapView, color, scene, owner):
        self.entity = Entity.TOWER
        self.state_counter = 0
        self.map_view = map_view
        self.map_view.register(self)
        self.color = color
        self.scene = scene
        self.owner = owner
        self.state = State.SEARCHING
        self.target = None
        self.reloading_counter = 0
        self.reloading_duration = 50

    def check_monster_alive(self, m):
        return m.is_alive()

    def location(self) -> Location:
        return self.map_view.center

    def action(self) -> Bullet | None:
        self.state_counter += 1
        if self.state == State.SEARCHING:
            monsters = list(filter(lambda m: m.is_alive(), self.map_view.find(Entity.MONSTER)))
            if monsters:
                # find first monster
                self.state = State.SHOOTING
                self.target = monsters[0]
                logger.debug(f"Found monster: {self.target}")
            return None
        elif self.state == State.SHOOTING:
            if self.map_view.in_sight(self.target.location()) and self.target.is_alive():
                logger.debug(f"Shooting monster: {self.target}")
                self.state = State.RELOADING
                # shoot
                return Bullet(10, self.location(), self.scene, self.target)
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
        p = self.scene.get_point(self.map_view.center)
        pygame.draw.rect(screen, self.color, pygame.Rect(p.x, p.y, self.scene.cell_width, self.scene.cell_height))
