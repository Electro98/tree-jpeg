"""Module that provides CLI to user."""

import argparse

from .tree_constructor import TreeConstractor
from .image_drawer import draw


def main():
    parser = argparse.ArgumentParser(description='Compress image by tree')
    parser.add_argument('src',
                        help='Converted image')
    parser.add_argument('--color_difference', '-cd', default=0.12, type=float,
                        help='Color difference in dole.')
    parser.add_argument('--interactive', '-i', action="store_true",
                        help='Run or not pygame window.')
    args = vars(parser.parse_args())
    constractor = TreeConstractor(args["color_difference"])
    tree = constractor.create_tree(args["src"])
    draw(tree, False)


if __name__ == '__main__':
    main()
