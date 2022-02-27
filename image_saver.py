
import numpy as np
from PIL import Image

from .quadtree import Quadtree
from .timer import timeit


def to_max_depth(tree: Quadtree, max_depth: int):
    """Compress tree until max_depth is reached."""
    if tree.depth() <= max_depth:
        return tree
    diff_depth = tree.depth() - max_depth + 1
    for node in tree:
        if node.depth() == diff_depth:
            node.unite()
    tree.collapse()


def tree_to_clear_matrix(tree: Quadtree) -> np.ndarray:
    """Create image from tree."""
    size = tree.area.end
    result = np.ndarray((*size, 3), dtype=np.uint8)
    for node in tree:
        if node.is_divided():
            continue
        x0, y0 = node.area.start
        x1, y1 = node.area.end
        result[y0:y1, x0:x1] = node.area.color
    return result


def tree_to_bordered_matrix(tree: Quadtree) -> np.ndarray:
    """Create image with borders from tree."""
    size = tree.area.end.x * 2 - 1
    result = np.ndarray((size, size, 3), dtype=np.uint8)
    for node in tree:
        x0, y0 = node.area.start
        x1, y1 = node.area.end
        if node.is_divided():
            # result[y0 * 2:y1 * 2 - 1, x0 + x1 - 1] = (255, 255, 255)
            # result[y0 + y1 - 1, x0 * 2:x1 * 2 - 1] = (255, 255, 255)
            continue
        result[y0 * 2:y1 * 2 - 1, x0 * 2:x1 * 2 - 1] = node.area.color
    return result


def tree_to_strange_matrix(tree: Quadtree) -> np.ndarray:
    """Create strange image from tree."""
    size = tree.area.end.x * 2 - 1
    result = np.ndarray((size, size, 3), dtype=np.uint8)
    for node in tree:
        x0, y0 = node.area.start
        x1, y1 = node.area.end
        if node.is_divided():
            result[y0 * 2:y0 + y1, (x0 + x1) // 2 + x0] = (0, 0, 0)
            result[(y0 + y1) // 2 + y0, x0 * 2:x0 + x1] = (0, 0, 0)
            continue
        result[y0 * 2:y1 + y0, x0 * 2:x1 + x0] = node.area.color
    return result


def compress_image(tree: Quadtree, max_depth: int, borders: bool) -> Image:
    """Compress tree to max depth and construct image."""
    to_max_depth(tree, max_depth)
    if not borders:
        image_data = tree_to_clear_matrix(tree)
    else:
        image_data = tree_to_bordered_matrix(tree)
    return Image.fromarray(image_data, "RGB")


@timeit
def gif_compression(
    tree: Quadtree,
    min_depth: int = 4,
    borders: bool = False,
    result_path: str = "result",
):
    """Create GIF with tree compression."""
    start_depth = tree.depth()
    if start_depth <= min_depth:
        raise AttributeError("current_depth less than min_depth")
    image_data_from_tree = tree_to_clear_matrix if not borders else tree_to_bordered_matrix
    frames = [Image.fromarray(image_data_from_tree(tree), "RGB")]
    for i in reversed(range(min_depth, start_depth)):
        to_max_depth(tree, i)
        frames.append(Image.fromarray(image_data_from_tree(tree), "RGB"))
    frames[0].save(
        f'{result_path}_comp.gif',
        'GIF', append_images=frames[1:],
        save_all=True,
        duration=(start_depth - min_depth) * 200,
        loop=0,
        optimize=True)
