"""Module that provides CLI to user."""

import argparse

from .image_drawer import draw
from .image_saver import compress_image, gif_compression
from .tree_constructor import TreeConstractor


def main():
    """Provide CLI to user."""
    parser = argparse.ArgumentParser(description="Compress image by tree")
    parser.add_argument("src",
                        help="Converted image")
    parser.add_argument("--color_difference", "-cd",
                        default=0.12,
                        type=float,
                        help="Color difference in dole.")
    parser.add_argument("--output", "-o",
                        default="tree-jpeg/result.png",
                        help="File where to save results.")
    parser.add_argument("--border", "-b",
                        default=False,
                        action="store_true",
                        help="Show borders of quadtrees or not.")
    parser.add_argument("--gif", "-g",
                        default=False,
                        action="store_true",
                        help="Save gif with step-by-step compression process.")
    parser.add_argument("--interactive", "-i",
                        default=False,
                        action="store_true",
                        help="Run or not pygame window.")
    args = vars(parser.parse_args())
    constractor = TreeConstractor(args["color_difference"])
    tree = constractor.create_tree(args["src"])
    if args["interactive"]:
        draw(tree, False)
    else:
        image = compress_image(tree, 10, args["border"])
        if args["gif"]:
            gif_compression(tree, borders=args["border"], result_path=args["output"])
        image.save(args["output"], "PNG")


if __name__ == "__main__":
    main()
