import pygame
from typing import List, Self
import pathlib

class Offset:

    def __init__(self, dx=0, dy=0):
        self.dx = dx
        self.dy = dy

    def __mul__(self, factor) -> Self:
        self.dx = self.dx * factor
        self.dy = self.dy * factor
        return self

    def __repr__(self):
        return f"dy={self.dy}, dx={self.dx}"

class Location:

    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __repr__(self):
        return f"location: {self.row},{self.col}"

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

    def north(self) -> Self:
        return Location(self.row - 1, self.col)

    def south(self) -> Self:
        return Location(self.row + 1, self.col)

    def west(self) -> Self:
        return Location(self.row, self.col - 1)

    def east(self) -> Self:
        return Location(self.row, self.col + 1)

    def directions(self) -> List[Self]:
        return [self.north(), self.east(), self.south(), self.west()]

    def __sub__(self, other: Self) -> Offset:
        return Offset(dy=self.row - other.row, dx=self.col - other.col)


class Map:
    FREE = 0
    TERRAIN = 1
    TOWER = 2
    CASTLE = 3
    TRAP = 4
    BOT = 6

    def __init__(self, arg: str|List[List[int]]):
        # create map out of file content
        if type(arg) is str:
            self.map: List[List[int]] = Map._load_map(arg)
        else:
            self.map: List[List[int]] = arg
        self.height = len(self.map)
        self.width = len(self.map[0])

    @staticmethod
    def _load_map(filename):
        loaded_map: list[list[int]] = []
        matrix = open(filename, "r")

        lines = matrix.readlines()
        num_rows = int(lines[0])
        num_cols = int(lines[1])
        loaded_map = [[Map.FREE] * num_cols for _ in range(num_rows)]

        map_content = lines[2:]
        if len(map_content) != num_rows:
            raise Exception(f"Unexpected number of rows in the map. Expected={num_rows}. Got={len(map_content)}")
        for row_idx, row in enumerate(map_content):
            row = row.strip()
            if len(row) != num_cols:
                raise Exception(f"Unexpected number of cols in the map line. Expected={num_cols}. Got={len(row)}")
            for col_idx, ch in enumerate(row):
                x = int(ch)
                loaded_map[row_idx][col_idx] = x
        matrix.close()
        return loaded_map

    def get_available_locations(self, loc) -> List[Location]:
        result = []
        for next_loc in [loc.north(), loc.east(), loc.south(), loc.west()]:
            if self.is_available(next_loc):
                result.append(next_loc)
        return result

    def is_available(self, loc):
        return self.is_free(loc) or self.is_trap(loc)

    def get_castle_next_to(self, loc):
        castle_location = None
        for next_loc in self.get_available_locations(loc):
            if self.is_castle(loc):
                if not castle_location is None:
                    raise Exception("more than one castle found")
                castle_location = loc
        return castle_location

    def on_map(self, loc: Location) -> bool:
        return 0 <= loc.row < self.height and 0 <= loc.col < self.width

    def is_trap(self, loc: Location):
        return self.on_map(loc) and self.map[loc.row][loc.col] == Map.TRAP

    def is_free(self, loc: Location):
        return self.on_map(loc) and self.map[loc.row][loc.col] == Map.FREE

    def is_castle(self, loc: Location):
        return self.on_map(loc) and self.map[loc.row][loc.col] == Map.CASTLE

    def is_bot(self, loc: Location):
        return self.on_map(loc) and self.map[loc.row][loc.col] == Map.BOT

    def take_location(self, loc: Location, who: int):
        if self.is_free(loc):
            self.map[loc.row][loc.col] = who
        elif self.is_trap(loc):
            print("trap")
            exit()
        else:
            raise RuntimeError(f"{loc} was not free: {self.map[loc.row][loc.col]}")

    def free_location(self, loc: Location):
        if self.is_bot(loc):
            self.map[loc.row][loc.col] = Map.FREE
        else:
            raise RuntimeError(f"{loc} was not taken by Bot")

    def value(self, loc: Location) -> int|None:
        if self.on_map(loc):
            return self.map[loc.row][loc.col]
        else:
            return None



class MapView:

    def __init__(self, game_map: Map, center: Location, width: int, height: int):
        self.map = game_map
        self.center = center
        self.width = width
        self.height = height
        if self.width % 2 == 0 or self.height % 2 == 0:
            raise Exception("Expected odd numbers for width and height")

    def in_sight(self, loc: Location) -> bool:
        half_h = self.height // 2
        half_w = self.width // 2
        return ((self.center.row - half_h <= loc.row <= self.center.row + half_h)
                and (self.center.col - half_w <= loc.col <= self.center.col + half_w)
                and self.map.on_map(loc))

    def relocate(self, new_center: Location):
        self.center = new_center

    def is_free(self, loc: Location):
        return self.in_sight(loc) and self.map.is_free(loc)


    def find(self, tag: int) -> Location | None:
        # bot_location = self.map_view.find(GameMap.BOT)
        for i in range(self.height):
            loc = Location(self.center.row - self.height // 2 + i, self.center.col - self.width // 2)
            for j in range(self.width):
                if self.in_sight(loc) and self.map.value(loc) == tag:
                    return loc
                else:
                    loc = loc.east()

    def is_castle(self, nl):
        return self.in_sight(nl) and self.map.is_castle(nl)


#                col = self.center + width(j - vision)height(i - vision)


if __name__ == "__main__":
    the_map = Map([[1, 1, 1, 1],
               [6, 0, 0, 1],
               [1, 1, 6, 1],
               [1, 2, 0, 0]])
    view = MapView(the_map, Location(3, 1), 3, 3)
    assert view.find(6) == Location(2, 2)

    l1 = Location(1, 0)
    l2 = Location(1,1)
    diff1 = l2 - l1
    assert diff1.dx == 1 and diff1.dy == 0
    diff2 = l1 - l2
    assert diff2.dx == -1 and diff2.dy == 0

