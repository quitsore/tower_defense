import pygame
import enum

from map import Location, Offset
from the_game.map import MapView


class State(enum.IntEnum):
    SPAWNING = 0
    SEARCHING = 1
    MOVING = 2
    HITTING = 3


class Monster:

    def __init__(self, loc: Location, map_view: MapView):
        self.loc = loc
        self.next_loc = None
        self.speed = 2
        self.offset = Offset()
        self.map_view = map_view
        self.color = pygame.Color(255, 0, 0, 255)
        self.state = State.SPAWNING
        self.trace = []
        self.state_counter = 0

    def _transit(self, new_state: State):
        self.state = new_state
        self.state_counter = -1

    def action(self):
        self.state_counter += 1
        if self.state == State.SPAWNING:
            self._transit(State.SEARCHING)
        elif self.state == State.SEARCHING:
            next_loc = None
            for nl in filter(self.has_not_visited, self.loc.directions()):
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
                self.trace.append(self.loc)
                self.loc = self.next_loc
                self.next_loc = None
                self.map_view.relocate(self.loc)
                self._transit(State.SEARCHING)
            else:
                cell_offset = self.next_loc - self.loc
                self.offset = cell_offset * self.state_counter * self.speed
                print(f"offset = {self.offset}")
        elif self.state == State.HITTING:
            pass

    def draw(self, screen):
        if self.state == State.SPAWNING:
            # self.scene.get_coordinate(self.loc)
            y = self.loc.row * 40
            x = self.loc.col * 40
            pygame.draw.rect(screen, self.color, pygame.Rect(x, y, 40, 40))
        elif self.state == State.SEARCHING:
            # self.scene.get_coordinate(self.loc)
            y = self.loc.row * 40
            x = self.loc.col * 40
            pygame.draw.rect(screen, self.color, pygame.Rect(x, y, 40, 40))
        elif self.state == State.MOVING:
            # self.scene.get_coordinate(self.loc)
            y = self.loc.row * 40 + self.offset.dy
            x = self.loc.col * 40 + self.offset.dx
            pygame.draw.rect(screen, self.color, pygame.Rect(x, y, 40, 40))
        elif self.state == State.HITTING:
            pass

    def has_not_visited(self, location):
        # check if location in trace
        if self.map_view.in_sight(location) and self.trace.count(location) == 0:
            return True
        else:
            return False
