
from typing import Tuple, Union


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
    __slots__ = 'x', 'y'

    def __init__(self, x, y):
        super(Pixel, self).__init__(x, y)

    def __eq__(self, pixel):
        return isinstance(pixel, Point) and \
            self.x == pixel.x and self.y == pixel.y

    def get_color(self):
        return 255, 255, 255


class Area:
    """docstring for Area"""
    __slots__ = 'start', 'end'
    point_data = Union[Point, Tuple[int, int]]

    def __init__(self, start: point_data, end: point_data):
        self.start = start if isinstance(start, Point) else Pixel(*start)
        self.end = end if isinstance(end, Point) else Pixel(*end)

    def __contains__(self, point: Point):
        return self.start.x <= point.x < self.end.x and \
            self.start.y <= point.y < self.end.y

    def __str__(self):
        return f'Area: {self.start}, {self.end}'


class Quadtree:
    """docstring for Quadtree"""
    __slots__ = 'bounds', 'pixel', \
                'north_west', 'north_east', \
                'sourth_west', 'sourth_east'

    def __init__(self, bounds, pixel=None):
        self.bounds = bounds
        self.pixel = None
        self.clear_childs()

    def _subdivide(self) -> None:
        north_west_end = (self.bounds.start.x + self.bounds.end.x) // 2, \
                         (self.bounds.start.y + self.bounds.end.y) // 2
        self.north_west = Quadtree(Area(self.bounds.start, north_west_end))
        sourth_east_start = north_west_end[0], north_west_end[1]
        self.sourth_east = Quadtree(Area(sourth_east_start, self.bounds.end))
        north_east_start = north_west_end[0], self.bounds.start.y
        north_east_end = self.bounds.end.x, north_west_end[1]
        self.north_east = Quadtree(Area(north_east_start, north_east_end))
        sourth_west_start = self.bounds.start.x, north_west_end[1]
        sourth_west_end = north_west_end[0], self.bounds.end.y
        self.sourth_west = Quadtree(Area(sourth_west_start, sourth_west_end))

    def is_divided(self) -> bool:
        return bool(self.north_west)

    def insert(self, pixel: Pixel) -> bool:
        if pixel not in self.bounds:
            return False
        if not self.is_divided() and not self.pixel:
            self.pixel = pixel
            return True
        if not self.is_divided():
            self._subdivide()
        # Simplest solution, just trying to insert our pixel to one child
        if self.pixel:
            self.north_west.insert(self.pixel) or \
                self.north_east.insert(self.pixel) or \
                self.sourth_east.insert(self.pixel) or \
                self.sourth_west.insert(self.pixel)
            self.pixel = None
        return self.north_west.insert(pixel) or \
            self.north_east.insert(pixel) or \
            self.sourth_east.insert(pixel) or \
            self.sourth_west.insert(pixel)

    def delete(self, pixel: Pixel) -> bool:
        if pixel not in self.bounds:
            return False
        if not self.is_divided() and self.pixel == pixel:
            self.pixel = None
            return True
        elif self.is_divided():
            return self.north_west.delete(pixel) or \
                self.north_east.delete(pixel) or \
                self.sourth_east.delete(pixel) or \
                self.sourth_west.delete(pixel)
        return False

    def is_empty(self) -> bool:
        return not self.is_divided() and not self.pixel

    def collapse(self) -> None:
        if not self.is_divided():
            return
        self.north_west.collapse()
        self.north_east.collapse()
        self.sourth_east.collapse()
        self.sourth_west.collapse()
        child_count = not self.north_west.is_empty()
        child_count += not self.north_east.is_empty()
        child_count += not self.sourth_east.is_empty()
        child_count += not self.sourth_west.is_empty()
        if child_count <= 1:
            self.pixel = self.north_west.pixel or \
                self.north_east.pixel or \
                self.sourth_east.pixel or \
                self.sourth_west.pixel
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

    def pixels(self):
        if self.pixel:
            yield self.pixel
        elif self.is_divided():
            for pixel in self.north_west.pixels():
                yield pixel
            for pixel in self.north_east.pixels():
                yield pixel
            for pixel in self.sourth_east.pixels():
                yield pixel
            for pixel in self.sourth_west.pixels():
                yield pixel

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
    tree = Quadtree(Area((0, 0), (15, 15)))
    tree.insert(Pixel(0, 0))
    tree.insert(Pixel(0, 7))
    tree.insert(Pixel(8, 8))
    print('-' * 10)
    print(f'Tree depth: {tree.depth()}')
    for pixel in tree.pixels():
        print(pixel)
    print('-' * 10)
    tree.delete(Pixel(0, 7))
    tree.collapse()
    print(f'Tree depth: {tree.depth()}')
    for pixel in tree.pixels():
        print(pixel)
    print('-' * 10)
    for i in tree:
        print(f'I\'m {i}, my depth: {i.depth()}')
    print('-' * 10)
