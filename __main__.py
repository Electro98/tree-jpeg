"""Module that provides CLI to user."""

from PIL import Image

from .quadtree import Quadtree, Area, Pixel
from .image_drawer import draw


def main():
    with Image.open("practice_21\\images\\unknown.png") as input_img:
        # TODO: shrinking to 2^x size square
        size = height, width = 512, 512
        shrinked_img = input_img.resize(size, Image.ANTIALIAS)
        pixel_data = shrinked_img.getdata()
        tree = Quadtree(Area((0, 0), size, (0, 0, 0)))
        for j in range(height):
            for i in range(width):
                color = pixel_data[j * width + i]
                tree.insert(Pixel(i, j, color))
    tree.collapse()
    draw(tree)


if __name__ == '__main__':
    main()
