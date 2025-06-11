import math
from typing import Self

from .map import Location


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

    def __add__(self, other) -> Self:
        return Offset(dx=self.dx + other.dx, dy=self.dy + other.dy)


class Point:

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __str__(self):
        return f"Point: x = {self.x}, y = {self.y}"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __sub__(self, other) -> Offset:
        return Offset(dx=self.x - other.x, dy=self.y - other.y)

    def __add__(self, offset: Offset) -> Self:
        return Point(x=self.x + offset.dx, y=self.y + offset.dy)

    def distance_to(self, other: Self) -> float:
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    # TODO: to be removed
    def slope_of_vector_to(self, other: Self) -> float:
        """angle of slope of a vector build by pointing from the self point to the other point, assuming
        that X axis is pointing to the right from the point"""
        ox_unit = Offset(dx=1, dy=0)
        vector = Offset()
        dot_product = self.x * other.x + self.y * other.y
        norm_self = math.sqrt(self.x ** 2 + self.y ** 2)
        norm_other = math.sqrt(other.x ** 2 + other.y ** 2)
        cos_theta = dot_product / (norm_self * norm_other)
        angle_rad = math.acos(cos_theta)
        return angle_rad


class Scene:
    def __init__(self, cell_height, cell_width):
        self.cell_height = cell_height
        self.cell_width = cell_width

    def cell_center(self) -> Offset:
        return Offset(self.cell_width / 2, self.cell_height / 2)

    def get_point(self, loc: Location, offset=Offset(0, 0)) -> Point:
        y = loc.row * self.cell_height + offset.dy
        x = loc.col * self.cell_width + offset.dx
        return Point(x, y)

    def out_of_cell_bounds(self, offset: Offset) -> bool:
        """return true if offset is higher than some cell bounds"""
        return abs(offset.dx) >= self.cell_width or abs(offset.dy) >= self.cell_height

    def get_location(self, point: Point) -> Location:
        col = point.x // self.cell_width
        row = point.y // self.cell_height
        return Location(col=col, row=row)


if __name__ == "__main__":
    # 2. scene = Scene(40, 40, game_map)
    scene = Scene(40, 40)
    # 3. test get_point out of location
    assert scene.get_point(Location(1, 1)) == Point(x=40, y=40)
    # 4. test get_point out of location and offset
    assert scene.get_point(Location(1, 1), Offset(10, 10)) == Point(x=50, y=50)
    # 5. test for has_moved_away returns false
    assert scene.out_of_cell_bounds(Offset(10, 10)) == False
    # 6. test for has_moved_away returns true
    assert scene.out_of_cell_bounds(Offset(45, 10)) == True
    # 7. distance between points
    point = Point(1, 2)
    assert point.distance_to(Point(2, 2)) == 1.0
    # 8. slope
    point = Point(0, 0)
    # assert point.slope_of_vector_to(Point(1, 0)) == 0
    # 9. point to location
    assert scene.get_location(Point(0, 0)) == Location(0, 0)
    assert scene.get_location(Point(45, 45)) == Location(1, 1)
