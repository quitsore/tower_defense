from typing import List


class Location:

    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __repr__(self):
        return f"location: {self.row},{self.col}"

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

class Map:

    FREE = 0
    TERRAIN = 1
    TOWER  = 2
    CASTLE = 3
    TRAP = 4

    def __init__(self, filename):
        # create map out of file content
        self.map = Map._load_map(filename)

    @staticmethod
    def _load_map(filename):
        loaded_map: list[list[int]] = []
        matrix = open(filename, "r")
        symmetrical = None

        for row in matrix.readlines():
            row = row.strip()
            if symmetrical is None:
                symmetrical = len(row)
            if symmetrical != len(row):
                print("the map is not symmetrical")
                exit()
            loaded_map.append([])
            for ch in row:
                if not ch.isnumeric():
                    continue
                x = int(ch)
                loaded_map[-1].append(x)
        matrix.close()
        return loaded_map

    def get_available_location(self, location) -> List[Location]:
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
        return self.map[location.row][location.col] == Map.TRAP

    def is_free(self, location: Location):
        return self.map[location.row][location.col] == Map.FREE

    def is_castle(self, location: Location):
        return self.map[location.row][location.col] == Map.CASTLE

    def north(self, location: Location) -> Location|None:
        if location.row > 0:
            return Location(location.row - 1, location.col)
        else:
            return None

    def east(self, location) -> Location|None:
        if location.col + 1 < len(self.map[0]):
            return Location(location.row, location.col + 1)
        else:
            return None

    def south(self, location) -> Location|None:
        if location.row  + 1 < len(self.map):
            return Location(location.row + 1, location.col)
        else:
            return None

    def west(self, location) -> Location|None:
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
    while not walk_finished:
        loc = bot.location
        for next_loc in game_map.get_available_location(loc):
            if not bot.has_visited(next_loc):
                bot.move(next_loc)
                print(next_loc)
                break
        if game_map.is_trap(bot.location):
            print("Fall through trap")
            return
        walk_finished = (loc == bot.location)
    if game_map.get_castle_next_to(bot.location):
        print("I'll destroy this castle")
    else:
        print("Castle not found")

location =  Location(0, 2)
location2 =  Location(0, 2)

game_map = Map("maze.txt")
print(location == location2)
bot = Bot(Location(1, 0))
walk_maze(game_map, bot)
print("++++++++++++++++++++++++++++++++++++++++++++++")
walk_maze(game_map, bot)
