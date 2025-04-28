import enum
import pygame
from the_game.map import MapView, Entity
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class State(enum.IntEnum):
    SEARCHING = 1
    SHOOTING = 2


class Tower:
    def __init__(self, map_view: MapView, color):
        self.state_counter = 0
        self.map_view = map_view
        self.color = color
        self.state = State.SEARCHING
        self.target = None

    def action(self):
        self.state_counter += 1
        if self.state == State.SEARCHING:
            monsters = self.map_view.find(Entity.MONSTER)
            if monsters:
                # find first monster
                self.state = State.SHOOTING
                self.target = monsters[0]
                logger.debug(f"Found monster: {self.target}")
        elif self.state == State.SHOOTING:
            if self.map_view.in_sight(self.target.location()):
                logger.debug(f"Shooting monster: {self.target}")
            else:
                self.target = None
                self.state = State.SEARCHING


    def draw(self, screen):
        loc = self.map_view.center
        x = loc.col * 40
        y = loc.row * 40
        pygame.draw.rect(screen, self.color, pygame.Rect(x, y, 40, 40))
