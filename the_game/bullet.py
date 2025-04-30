import enum
import pygame
import math

from the_game.map import MapView, Location
from the_game.scene import Offset, Scene, Point


class State(enum.IntEnum):
    FLYING = 1
    STRIKING = 2
    DONE = 3

class Bullet:

    def __init__(self, damage, start_point: Point, scene: Scene, target):
        self.target = target
        self.point = start_point
        self.scene = scene
        self.state = State.FLYING
        self.color = (0,0,0)
        self.abs_speed = 5
        self.damage = damage

    def action(self):
        if self.state == State.FLYING:
            next_point = self.calculate_next_point()
            if next_point.distance_to(self.target.point()) <= 1:
                 self.state = State.STRIKING
            else:
                self.point = next_point
        elif self.state == State.STRIKING:
            self.target.get_hit(self.damage)
            self.state = State.DONE
        elif self.state == State.DONE:
            pass

    def draw(self, screen):
        if self.state == State.FLYING:
            pygame.draw.rect(screen, self.color, pygame.Rect(self.point.x, self.point.y, 8, 8))
        else:
            pass

    def calculate_next_point(self) -> Point:
        pass