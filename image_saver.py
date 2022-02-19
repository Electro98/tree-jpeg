
import numpy as np

from .quadtree import Quadtree
from PIL import Image, ImageDraw


def to_max_depth(tree: Quadtree, max_depth: int):
    if tree.depth() <= max_depth:
        return tree
    diff_depth = tree.depth() - max_depth + 1
    for node in tree:
        if node.depth() == diff_depth:
            node.unite()
    tree.collapse()


def tree_to_clear_matrix(tree: Quadtree) -> np.ndarray:
    size = tree.area.end
    result = np.ndarray((*size, 3), dtype=np.uint8)
    for node in tree:
        if node.is_divided():
            continue
        x0, y0 = node.area.start
        x1, y1 = node.area.end
        result[y0:y1, x0:x1] = node.area.color
    return result

def tree_to_dirty_matrix(tree: Quadtree) -> np.ndarray:
    size = tree.area.end.x * 2 - 1
    result = np.ndarray((size, size, 3), dtype=np.uint8)
    for node in tree:
        x0, y0 = node.area.start
        x1, y1 = node.area.end
        if node.is_divided():
            result[y0 * 2:y1 * 2 - 1, x0 + x1 - 1] = (255, 255, 255)
            result[y0 + y1 - 1, x0 * 2:x1 * 2 - 1] = (255, 255, 255)
            continue
        result[y0 * 2:y1 * 2 - 1, x0 * 2:x1 * 2 - 1] = node.area.color
    return result


def tree_to_strange_matrix(tree: Quadtree) -> np.ndarray:
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
    to_max_depth(tree, max_depth)
    if not borders:
        image_data = tree_to_clear_matrix(tree)
    else:
        image_data = tree_to_dirty_matrix(tree)
    return Image.fromarray(image_data, "RGB")
