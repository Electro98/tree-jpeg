"""Module that provides CLI to user."""

from .tree_constructor import TreeConstractor
from .image_drawer import draw


def main():
    constractor = TreeConstractor()
    tree = constractor.create_tree("practice_21\\images\\unknown.png")
    draw(tree)


if __name__ == '__main__':
    main()
