"""Cool."""
import numpy as np
from PIL import Image

from math import log2

from .quadtree import Quadtree, Area, Color


def close_size(cord_x: int, cord_y: int):
    """Return closest size, that's a power of two."""
    return 2 ** round(log2(max(cord_x, cord_y)) + 0.49)


class TreeConstractor:
    """Class, that creates quadtrees from images."""

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

    def create_tree(self, image_path: str) -> Quadtree:
        """Load image from given path and return compressed quadtree."""
        image = self.parse_image(image_path)
        tree = Quadtree(Area(image.shape[0], image.shape[0]))
