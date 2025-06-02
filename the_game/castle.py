import enum
import pygame
from map import MapView, Entity


class State(enum.IntEnum):
    ALIVE = 0
    DESTROYED = 1


class Castle:
    def __init__(self, map_view: MapView, color, scene, castle_config):
        self.map_view = map_view
        self.map_view.register(self)
        self.health = castle_config["castle"]["health"]
        self.state = State.ALIVE
        self.color = color
        self.scene = scene
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
        p = self.scene.get_point(self.map_view.center)
        pygame.draw.rect(screen, self.color, pygame.Rect(p.x, p.y, self.scene.cell_width, self.scene.cell_height))

    def is_destroyed(self) -> bool:
        return self.state == State.DESTROYED
