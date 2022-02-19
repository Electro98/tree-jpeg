"""Cool."""
import numpy as np
from PIL import Image

from math import log2, sqrt

from .quadtree import Quadtree, Area, Color


def close_size(cord_x: int, cord_y: int):
    """Return closest size, that's a power of two."""
    return 2 ** round(log2(max(cord_x, cord_y)) + 0.49)


def color_diff(first: Color, second: Color) -> float:
    """Compute color difference."""
    r0, g0, b0 = first
    r1, g1, b1 = second
    _red = (r0 + r1) / 2
    return sqrt(
        (2 + _red / 256) * (r0 - r1) ** 2
        +
        4 * (g0 - g1) ** 2
        +
        (2 + (255 - _red) / 256) * (b0 - b1) ** 2
    ) / 765


class TreeConstractor:
    """Class, that creates quadtrees from images."""
    def __init__(self, color_difference):
        # Just Noticeable Color Difference
        self.color_difference = color_difference

    @staticmethod
    def parse_image(image_path: str) -> np.ndarray:
        """Parse image to numpy matrix."""
        with Image.open(image_path) as input_img:
            size = close_size(*input_img.size)
            shrinked_img = input_img.resize((size, size), Image.ANTIALIAS)
            pixel_data = np.asarray(shrinked_img.convert("RGB"))
        return pixel_data

    @staticmethod
    def average_color(image: np.ndarray) -> Color:
        """Return average color of given image."""
        red, blue, green = image.mean((0, 1))
        return round(red), round(blue), round(green)

    @staticmethod
    def min_color(image: np.ndarray):
        """Return min color of given image."""
        return tuple(image.min((0, 1)))

    @staticmethod
    def max_color(image: np.ndarray):
        """Return max color of given image."""
        return tuple(image.max((0, 1)))

    def is_consistent_color(self, image_part: np.ndarray):
        """Check is color near the same in this image."""
        average_color = TreeConstractor.average_color(image_part)
        min_color = TreeConstractor.min_color(image_part)
        max_color = TreeConstractor.max_color(image_part)
        return all((
            color_diff(average_color, min_color) <= self.color_difference,
            color_diff(average_color, max_color) <= self.color_difference,
        ))

    def create_tree(self, image_path: str) -> Quadtree:
        """Load image from given path and return compressed quadtree."""
        image = self.parse_image(image_path)
        tree = Quadtree(Area((0, 0), (image.shape[0], image.shape[0])))
        for node in tree:
            x0, y0 = node.area.start
            x1, y1 = node.area.end
            print(x0, x1, y0, y1, sep=", ")
            image_part = image[y0:y1, x0:x1]
            if self.is_consistent_color(image_part):
                node.area.color = self.average_color(image_part)
            else:
                node.subdivide()
        return tree
