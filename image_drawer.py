
import pygame

from .quadtree import Quadtree, Area, Pixel


class WinImage(object):
    """docstring for WinImage"""

    def __init__(self, tree: Quadtree, display=(640, 640)):
        pygame.init()
        self.tree = tree
        self.ratio = (display[0] - tree.bounds.end.x + 1) / tree.bounds.end.x
        self.screen = pygame.display.set_mode(display)
        self.clock = pygame.time.Clock()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

    def update(self):
        self.screen.fill((0, 0, 0))
        for node in self.tree:
            if node.is_divided():
                center_x = (node.bounds.start.x + node.bounds.end.x) * (self.ratio + 1) / 2 - 1
                center_y = (node.bounds.start.y + node.bounds.end.y) * (self.ratio + 1) / 2 - 1
                pygame.draw.line(self.screen, (255, 255, 255),  (center_x, node.bounds.start.y * self.ratio), (center_x, node.bounds.end.x * self.ratio))
                pygame.draw.line(self.screen, (255, 255, 255),  (node.bounds.start.x * self.ratio, center_y), (node.bounds.end.x * self.ratio, center_y))
            elif not node.is_empty():
                pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect((node.pixel.x * (self.ratio + 1), node.pixel.y * (self.ratio + 1)), (self.ratio, self.ratio)))
        pygame.display.update()

    def exec(self):
        self.update()
        while not False:
            self.check_events()
            # self.update()


def draw(tree: Quadtree):
    app = WinImage(tree)
    app.exec()


def main():
    tree = Quadtree(Area((0, 0), (16, 16)))
    tree.insert(Pixel(0, 0))
    tree.insert(Pixel(0, 7))
    tree.insert(Pixel(8, 8))
    draw(tree)


if __name__ == '__main__':
    main()
