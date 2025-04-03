from typing import List
import pathlib


class Location:

    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __repr__(self):
        return f"location: {self.row},{self.col}"

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col


class OldMap:
    FREE = 0
    TERRAIN = 1
    TOWER = 2
    CASTLE = 3
    TRAP = 4
    BOT = 6

    def __init__(self, arg: pathlib.Path|List[List[int]]):
        # create map out of file content
        if type(arg) is pathlib.Path:
            self.map: List[List[int]] = OldMap._load_map(arg)
        else:
            self.map: List[List[int]] = arg


    @staticmethod
    def _load_map(filename):
        loaded_map: list[list[int]] = []
        matrix = open(filename, "r")

        lines = matrix.readlines()
        num_rows = int(lines[0])
        num_cols = int(lines[1])
        loaded_map = [[OldMap.FREE] * num_cols for _ in range(num_rows)]

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

    def get_available_locations(self, location) -> List[Location]:
        result = []
        for loc in [self.north(location), self.east(location), self.south(location), self.west(location)]:
            if not loc is None and self.is_available(loc):
                result.append(loc)
        return result

    def is_available(self, location):
        return self.is_free(location) or self.is_trap(location)

    def get_castle_next_to(self, location):
        castle_location = None
        for loc in [self.north(location), self.east(location), self.south(location), self.west(location)]:
            if not loc is None and self.is_castle(loc):
                if not castle_location is None:
                    raise Exception("more than one castle found")
                castle_location = loc
        return castle_location

    def is_trap(self, location: Location):
        return self.map[location.row][location.col] == OldMap.TRAP

    def is_free(self, location: Location):
        return self.map[location.row][location.col] == OldMap.FREE

    def is_castle(self, location: Location):
        return self.map[location.row][location.col] == OldMap.CASTLE

    def is_bot(self, location: Location):
        return self.map[location.row][location.col] == OldMap.BOT

    def take_location(self, location: Location, who: int):
        if self.is_free(location):
            self.map[location.row][location.col] = who
        elif self.is_trap(location):
            print("trap")
            exit()
        else:
            raise RuntimeError(f"{location} was not free: {self.map[location.row][location.col]}")

    def free_location(self, location: Location):
        if self.is_bot(location):
            self.map[location.row][location.col] = OldMap.FREE
        else:
            raise RuntimeError(f"{location} was not taken by Bot")

    def north(self, location: Location) -> Location | None:
        if location.row > 0:
            return Location(location.row - 1, location.col)
        else:
            return None

    def east(self, location) -> Location | None:
        if location.col + 1 < len(self.map[0]):
            return Location(location.row, location.col + 1)
        else:
            return None

    def south(self, location) -> Location | None:
        if location.row + 1 < len(self.map):
            return Location(location.row + 1, location.col)
        else:
            return None

    def west(self, location) -> Location | None:
        if location.col > 0:
            return Location(location.row, location.col - 1)
        else:
            return None


class Bot:
    def __init__(self, start_location: Location):
        self.location = start_location
        self.trace = []

    def move(self, next_location):
        self.trace.append(self.location)
        self.location = next_location

    def forget(self):
        self.trace = []

    def has_visited(self, location):
        # check if location in trace
        if self.trace.count(location) > 0:
            return True
        else:
            return False

    def __repr__(self):
        return f"bot: {self.location}"


def walk_maze(game_map, bot):
    walk_finished = False
    if not game_map.is_available(bot.location):
        print("You are on an unreachable position")
        return
    print(bot.location)
    game_map.take_location(bot.location, OldMap.BOT)
    while not walk_finished:
        loc = bot.location
        for next_loc in game_map.get_available_locations(loc):
            if not bot.has_visited(next_loc):
                game_map.free_location(bot.location)
                bot.move(next_loc)
                game_map.take_location(next_loc, OldMap.BOT)
                print(next_loc)
                break
        if game_map.is_trap(bot.location):
            print("Fall through trap")
            return
        walk_finished = (loc == bot.location)
    if game_map.get_castle_next_to(bot.location):
        print("I'll destroy this castle")
        bot.forget()
    else:
        print("Castle not found")
    game_map.free_location(bot.location)


if __name__ == "__main__":
    game_map = OldMap("terrain.txt")

    bot = Bot(Location(2, 0))
    walk_maze(game_map, bot)
