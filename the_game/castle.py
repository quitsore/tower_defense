import enum
import pygame
from map import MapView, Entity


class State(enum.IntEnum):
    ALIVE = 0
    DESTROYED = 1


class Castle:
    def __init__(self, map_view: MapView, color):
        self.map_view = map_view
        self.map_view.register(self)
        self.health = 100
        self.state = State.ALIVE
        self.color = color
        self.entity = Entity.CASTLE

    def action(self):
        if self.state == State.ALIVE:
            if self.health <= 0:
                self.state = State.DESTROYED
        elif self.state == State.DESTROYED:
            pass

    def get_hit(self, damage):
        self.health -= damage
        print("ouch")

    def draw(self, screen):
        color = (255, 255, 0)
        x = 880
        y = 40
        pygame.draw.rect(screen, color, pygame.Rect(x, y, 40, 40))

    def is_destroyed(self) -> bool:
        return self.state == State.DESTROYED
