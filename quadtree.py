
from typing import Tuple, Union


Color = Tuple[int, int, int]


class Point:
    """docstring for Point"""
    __slots__ = 'x', 'y'

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, point):
        return isinstance(point, Point) and \
            self.x == point.x and self.y == point.y

    def __str__(self):
        return f'Point: {self.x}, {self.y}'


class Pixel(Point):
    """docstring for Pixel"""
    __slots__ = 'x', 'y', 'color'

    def __init__(self, x: int, y: int, color: Color):
        super(Pixel, self).__init__(x, y)
        self.color = color

    def __eq__(self, pixel):
        return isinstance(pixel, Point) and \
            self.x == pixel.x and self.y == pixel.y and \
            self.color == pixel.color

    def get_color(self):
        return self.color


class Area:
    """docstring for Area"""
    __slots__ = 'start', 'end', 'color'
    point_data = Union[Point, Tuple[int, int]]

    def __init__(self, start: point_data, end: point_data, color: Color):
        self.start = start if isinstance(start, Point) else Point(*start)
        self.end = end if isinstance(end, Point) else Point(*end)
        self.color = color

    def __contains__(self, point: Point):
        return self.start.x <= point.x < self.end.x and \
            self.start.y <= point.y < self.end.y

    def is_pixel(self):
        return (self.end.x - self.start.x) * (self.end.y - self.start.y) == 1

    def __str__(self):
        return f'Area: {self.start}, {self.end}, {self.color}'


class Quadtree:
    """docstring for Quadtree"""
    __slots__ = (
        'area',
        'north_west', 'north_east',
        'sourth_west', 'sourth_east'
    )

    def __init__(self, area):
        self.area = area
        self.clear_childs()

    def _subdivide(self) -> None:
        north_west_end = (self.area.start.x + self.area.end.x) // 2, \
                         (self.area.start.y + self.area.end.y) // 2
        self.north_west = Quadtree(
            Area(self.area.start, north_west_end, self.area.color)
        )
        sourth_east_start = north_west_end[0], north_west_end[1]
        self.sourth_east = Quadtree(
            Area(sourth_east_start, self.area.end, self.area.color)
        )
        north_east_start = north_west_end[0], self.area.start.y
        north_east_end = self.area.end.x, north_west_end[1]
        self.north_east = Quadtree(
            Area(north_east_start, north_east_end, self.area.color)
        )
        sourth_west_start = self.area.start.x, north_west_end[1]
        sourth_west_end = north_west_end[0], self.area.end.y
        self.sourth_west = Quadtree(
            Area(sourth_west_start, sourth_west_end, self.area.color)
        )

    def is_divided(self) -> bool:
        return bool(self.north_west)

    def insert(self, pixel: Pixel) -> bool:
        if pixel not in self.area:
            return False
        if not self.is_divided() and pixel.color == self.area.color:
            return True
        if self.area.is_pixel():
            self.area.color = pixel.color
            return True
        if not self.is_divided():
            self._subdivide()
        # Simplest solution, just trying to insert our pixel to one child
        return self.north_west.insert(pixel) or \
            self.north_east.insert(pixel) or \
            self.sourth_east.insert(pixel) or \
            self.sourth_west.insert(pixel)

    def collapse(self) -> None:
        if not self.is_divided():
            return
        self.north_west.collapse()
        self.north_east.collapse()
        self.sourth_east.collapse()
        self.sourth_west.collapse()
        if max(self.north_west.is_divided(),
               self.north_east.is_divided(),
               self.sourth_east.is_divided(),
               self.sourth_west.is_divided()):
            return
        color = self.north_west.area.color
        if self.north_east.area.color == color and \
           self.sourth_east.area.color == color and \
           self.sourth_west.area.color == color:
            self.area.color = color
            self.clear_childs()

    def unite(self, unite_childs=False):
        if not self.is_divided():
            return
        if max(self.north_west.is_divided(),
               self.north_east.is_divided(),
               self.sourth_east.is_divided(),
               self.sourth_west.is_divided()):
            if not unite_childs:
                print('nope.')
                return
            self.north_west.unite(unite_childs)
            self.north_east.unite(unite_childs)
            self.sourth_east.unite(unite_childs)
            self.sourth_west.unite(unite_childs)
        self.area.color = tuple(
            map(lambda x: sum(x) // len(x),
                zip(self.north_west.area.color,
                    self.north_east.area.color,
                    self.sourth_east.area.color,
                    self.sourth_west.area.color))
        )
        self.clear_childs()

    def clear_childs(self) -> None:
        self.north_west = None
        self.north_east = None
        self.sourth_east = None
        self.sourth_west = None

    def depth(self) -> int:
        if not self.is_divided():
            return 1
        return 1 + max(self.north_west.depth(),
                       self.north_east.depth(),
                       self.sourth_east.depth(),
                       self.sourth_west.depth())

    def __iter__(self):
        # iteration through all nodes
        #
        # returns itself, first child, its first child...
        # than returns second child ... and to third one
        yield self
        if self.is_divided():
            for node in self.north_west:
                yield node
            for node in self.north_east:
                yield node
            for node in self.sourth_east:
                yield node
            for node in self.sourth_west:
                yield node


if __name__ == '__main__':
    tree = Quadtree(Area((0, 0), (15, 15), (0, 0, 0)))
    tree.insert(Pixel(0, 0, (255, 255, 255)))
    tree.insert(Pixel(0, 7, (255, 255, 255)))
    tree.insert(Pixel(8, 8, (255, 255, 255)))
    print('-' * 10)
    print(f'Tree depth: {tree.depth()}')
    print('-' * 10)
    tree.collapse()
    print(f'Tree depth: {tree.depth()}')
    print('-' * 10)
    for i in tree:
        print(f'I\'m {i}, my depth: {i.depth()}')
    print('-' * 10)
