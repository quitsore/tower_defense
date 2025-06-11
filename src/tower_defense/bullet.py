import enum
import logging

import pygame
import math

from .map import MapView, Location
from .scene import Offset, Scene, Point

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class State(enum.IntEnum):
    FLYING = 1
    STRIKING = 2
    DONE = 3


class Bullet:

    def __init__(self, damage, images, start_location: Location, scene: Scene, target, lag):
        self.target = target
        self.point = scene.get_point(start_location, scene.cell_center())
        self.scene = scene
        self.state = State.FLYING
        self.images = images
        self.abs_speed = 5
        self.damage = damage
        self.draw_counter = 0
        self.lag = lag
        self.strike_counter = len(self.images["explosion"]) * self.lag - self.lag

    def _transit(self, new_state):
        logger.info(f"Transiting from {self.state.name} to {new_state.name}")
        self.state = new_state
        if new_state == State.STRIKING:
            self.target.get_hit(self.damage)
            self.draw_counter = 0

    def action(self):
        if self.state == State.FLYING:
            next_point = self.calculate_next_point()
            if next_point.distance_to(self.target.center_point()) <= (self.abs_speed / 2 + 1):
                self._transit(State.STRIKING)
            else:
                self.point = next_point
        elif self.state == State.STRIKING:
            if self.strike_counter == 0:
                self._transit(State.DONE)
            else:
                self.strike_counter -= 1
        elif self.state == State.DONE:
            pass

    def draw(self, screen):
        self.draw_counter += 1
        if self.state == State.FLYING:
            screen.blit(self.images["bullet"], (self.point.x, self.point.y))
        elif self.state == State.STRIKING:
            logging.info(f"bullet: {self.draw_counter}, {self.lag}, {self.strike_counter}")
            screen.blit(self.images["explosion"][self.draw_counter // self.lag], (self.point.x, self.point.y))

    def calculate_next_point(self) -> Point:
        # given point, target and speed, calculate next point
        T = self.target.center_point()
        B = self.point
        Tx = Point(x=T.x, y=B.y)
        TB = T.distance_to(B)
        TTx = math.fabs(T.y - B.y)
        BTx = math.fabs(T.x - B.x)
        speed_dy = self.abs_speed * math.copysign(1, T.y - B.y)
        speed_dx = self.abs_speed * math.copysign(1, T.x - B.x)
        y = B.y + TTx * speed_dy / TB
        x = B.x + BTx * speed_dx / TB

        return Point(x, y)
