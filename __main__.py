"""Module that provides CLI to user."""

import argparse

from .tree_constructor import TreeConstractor
from .image_drawer import draw
from .image_saver import compress_image


def main():
    parser = argparse.ArgumentParser(description='Compress image by tree')
    parser.add_argument('src',
                        help='Converted image')
    parser.add_argument('--color_difference', '-cd', default=0.12, type=float,
                        help='Color difference in dole.')
    parser.add_argument('--border', '-b',
                        default=False,
                        action="store_true",
                        help='Run or not pygame window.')
    parser.add_argument('--interactive', '-i',
                        default=False,
                        action="store_true",
                        help='Run or not pygame window.')
    args = vars(parser.parse_args())
    constractor = TreeConstractor(args["color_difference"])
    tree = constractor.create_tree(args["src"])
    if args["interactive"]:
        draw(tree, False)
    else:
        image = compress_image(tree, 10, args["border"])
        image.save("tree-jpeg/image.png", "PNG")


if __name__ == '__main__':
    main()
