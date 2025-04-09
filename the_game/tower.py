import enum

from the_game.map import MapView


class State(enum.IntEnum):
    RESTING = 1
    SEARCHING = 2
    SHOOTING = 3

class Tower:
    def __init__(self, map_view: MapView):
        pass

    def action(self):
        pass

    def draw(self):
        pass