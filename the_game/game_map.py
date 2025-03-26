from typing import List, Self


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


class GameMap:
    FREE = 0
    TERRAIN = 1
    TOWER = 2
    CASTLE = 3
    TRAP = 4
    BOT = 6

    def __init__(self, filename):
        # create map out of file content
        self.map: List[List[int]] = GameMap._load_map(filename)
        self.height = len(self.map)
        self.width = len(self.map[0])

    @staticmethod
    def _load_map(filename):
        loaded_map: list[list[int]] = []
        matrix = open(filename, "r")

        lines = matrix.readlines()
        num_rows = int(lines[0])
        num_cols = int(lines[1])
        loaded_map = [[GameMap.FREE] * num_cols for _ in range(num_rows)]

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
        return self.on_map(loc) and self.map[loc.row][loc.col] == GameMap.TRAP

    def is_free(self, loc: Location):
        return self.on_map(loc) and self.map[loc.row][loc.col] == GameMap.FREE

    def is_castle(self, loc: Location):
        return self.on_map(loc) and self.map[loc.row][loc.col] == GameMap.CASTLE

    def is_bot(self, loc: Location):
        return self.on_map(loc) and self.map[loc.row][loc.col] == GameMap.BOT

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
            self.map[loc.row][loc.col] = GameMap.FREE
        else:
            raise RuntimeError(f"{loc} was not taken by Bot")
