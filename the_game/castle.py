import enum
import pygame
from map import MapView, Entity
from the_game.scene import Scene, Offset


class State(enum.IntEnum):
    ALIVE = 0
    DESTROYED = 1


class Castle:
    def __init__(self, map_view: MapView, color, scene, castle_config):
        self.map_view = map_view
        self.map_view.register(self)
        self.health = castle_config["castle"]["health"]
        self.initial_health = self.health
        self.state = State.ALIVE
        self.color = color
        self.scene = scene
        self.entity = Entity.CASTLE
        self.castle_image = [pygame.image.load("../resources/castle1.png"),
                             pygame.image.load("../resources/castle2.png"),
                             pygame.image.load("../resources/castle3.png"),
                             pygame.image.load("../resources/castle4.png")]
        castle_image_offset = Offset(dx=-10, dy=self.scene.cell_height - self.castle_image[0].get_rect().height + 2)
        self.p = self.scene.get_point(self.map_view.center)
        self.p += castle_image_offset

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
        if self.health >= self.initial_health * 0.66:
            image_idx = 0
        elif self.health >= self.initial_health * 0.33:
            image_idx = 1
        elif self.health > 0:
            image_idx = 2
        else:
            image_idx = 3
        screen.blit(self.castle_image[image_idx], (self.p.x, self.p.y))

    def is_destroyed(self) -> bool:
        return self.state == State.DESTROYED
