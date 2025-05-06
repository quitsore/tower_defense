import pygame
import enum
import logging
from map import Location, LocationDiff, Entity
from the_game.castle import Castle
from the_game.map import MapView
from the_game.scene import Scene, Offset, Point

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class State(enum.IntEnum):
    SPAWNING = 0
    SEARCHING = 1
    MOVING = 2
    HITTING = 3


class Monster:

    def __init__(self, scene: Scene, map_view: MapView, color, name):
        self.entity = Entity.MONSTER
        self.name = name
        self.next_loc = None
        self.abs_speed = 1
        self.speed = Offset()
        self.offset = Offset()
        self.scene = scene
        self.map_view = map_view
        self.map_view.register(self)
        self.color = color
        self.state = State.SPAWNING
        self.trace = []
        self.state_counter = 0
        self.damage = 5
        self.health = 10
        self.attack_delay = 50

    def get_hit(self, damage):
        self.health -= damage
        logger.info(f"got hit by {damage} points. rest health = {self.health}")

    def _transit(self, new_state: State):
        self.state = new_state
        self.state_counter = -1

    def location(self):
        return self.map_view.center

    def point(self) -> Point:
        return self.scene.get_point(self.location(), self.offset)

    def action(self):
        self.state_counter += 1
        loc = self.location()
        if self.state == State.SPAWNING:
            self._transit(State.SEARCHING)
        elif self.state == State.SEARCHING:
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
                self.speed = Offset(dx=loc_diff.dcol * self.abs_speed, dy=loc_diff.drow*self.abs_speed)
        elif self.state == State.MOVING:
            next_offset = self.offset + self.speed
            if self.scene.out_of_cell_bounds(next_offset):
                self.trace.append(self.location())
                self.map_view.relocate(self.next_loc)
                self.next_loc = None
                self._transit(State.SEARCHING)
            else:
                self.offset = next_offset
                logger.debug(f"offset = {self.offset}")
        elif self.state == State.HITTING:
            castle = self.map_view.get_castle(self.next_loc)
            if self.state_counter % self.attack_delay == 0:
                castle.get_hit(self.damage)

    def draw(self, screen):
        color = self.color
        loc = self.location()
        if self.state == State.SPAWNING:
            p = self.scene.get_point(self.map_view.center)
            pygame.draw.rect(screen, self.color, pygame.Rect(p.x, p.y, self.scene.cell_width, self.scene.cell_height))
        elif self.state == State.SEARCHING:
            p = self.scene.get_point(self.map_view.center)
            pygame.draw.rect(screen, self.color, pygame.Rect(p.x, p.y, self.scene.cell_width, self.scene.cell_height))
        elif self.state == State.MOVING:
            y = loc.row * 40 + self.offset.dy
            x = loc.col * 40 + self.offset.dx
            pygame.draw.rect(screen, self.color, pygame.Rect(x, y, 40, 40))
        elif self.state == State.HITTING:
            if self.state_counter % self.attack_delay == 0:
                color = (255, 255, 255)
            else:
                color = (255, 0, 0)
            y = loc.row * 40 + self.offset.dy
            x = loc.col * 40 + self.offset.dx
            pygame.draw.rect(screen, color, pygame.Rect(x, y, 40, 40))

    def has_not_visited(self, location):
        # check if location in trace
        if self.map_view.in_sight(location) and self.trace.count(location) == 0:
            return True
        else:
            return False

    def __str__(self):
        return f"monster: {self.name}, location: {self.location()}, offset: {self.offset}, health: {self.health}, entity: {self.entity}"
