import pygame
import enum
from map import Location, Offset, Entity
from the_game.castle import Castle
from the_game.map import MapView


class State(enum.IntEnum):
    SPAWNING = 0
    SEARCHING = 1
    MOVING = 2
    HITTING = 3


class Monster:

    def __init__(self, map_view: MapView, color):
        self.entity = Entity.MONSTER
        self.next_loc = None
        self.speed = 4
        self.offset = Offset()
        self.map_view = map_view
        self.map_view.register(self)
        self.color = color
        self.state = State.SPAWNING
        self.trace = []
        self.state_counter = 0
        self.damage = 5
        self.attack_delay = 100

    def _transit(self, new_state: State):
        self.state = new_state
        self.state_counter = -1

    def action(self):
        self.state_counter += 1
        loc = self.map_view.center
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
        elif self.state == State.MOVING:
            if abs(self.offset.dx) + self.speed >= 40 or abs(self.offset.dy) + self.speed >= 40:
                self.trace.append(self.map_view.center)
                self.map_view.relocate(self.next_loc)
                self.next_loc = None
                self._transit(State.SEARCHING)
            else:
                cell_offset = self.next_loc - loc
                self.offset = cell_offset * self.state_counter * self.speed
                print(f"offset = {self.offset}")
        elif self.state == State.HITTING:
            castle = self.map_view.get_castle(self.next_loc)
            castle.get_hit(self.damage)

    def draw(self, screen):
        color = self.color
        loc = self.map_view.center
        if self.state == State.SPAWNING:
            # self.scene.get_coordinate(self.loc)
            y = loc.row * 40
            x = loc.col * 40
            pygame.draw.rect(screen, self.color, pygame.Rect(x, y, 40, 40))
        elif self.state == State.SEARCHING:
            # self.scene.get_coordinate(self.loc)
            y = loc.row * 40
            x = loc.col * 40
            pygame.draw.rect(screen, self.color, pygame.Rect(x, y, 40, 40))
        elif self.state == State.MOVING:
            # self.scene.get_coordinate(self.loc)
            y = loc.row * 40 + self.offset.dy
            x = loc.col * 40 + self.offset.dx
            pygame.draw.rect(screen, self.color, pygame.Rect(x, y, 40, 40))
        elif self.state == State.HITTING:
            if self.state_counter % 2 == 0:
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
