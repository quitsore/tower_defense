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

    def __init__(self, damage, start_location: Location, scene: Scene, target):
        self.target = target
        self.point = scene.get_point(start_location, scene.cell_center())
        self.scene = scene
        self.state = State.FLYING
        self.color = (0, 0, 0)
        self.abs_speed = 5
        self.damage = damage

    def action(self):
        if self.state == State.FLYING:
            next_point = self.calculate_next_point()
            if next_point.distance_to(self.target.center_point()) <= (self.abs_speed / 2 + 1):
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
