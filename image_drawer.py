"""Unnecessary module for GUI."""

import pygame

from .quadtree import Quadtree


class WinImage(object):
    """Main pygame window."""

    def __init__(self, tree: Quadtree, display=(1080, 1080)):
        pygame.init()
        self.tree = tree
        self.ratio = (display[0] - tree.area.end.x + 1) / tree.area.end.x
        self.grid_color = (255, 255, 255)
        self.background = self.grid_color
        self.screen = pygame.display.set_mode(display)
        self.clock = pygame.time.Clock()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.jpeg_image()
                elif event.key == pygame.K_s:
                    pygame.image.save(
                        self.screen,
                        f"tree_{self.tree.depth()}.jpg",
                    )
                elif event.key == pygame.K_e:
                    pygame.quit()
                    exit(0)

    def update(self):
        self.screen.fill(self.background)
        for node in self.tree:
            if node.is_divided():
                center_x = (node.area.start.x + node.area.end.x) * (self.ratio + 1) / 2 - 1
                center_y = (node.area.start.y + node.area.end.y) * (self.ratio + 1) / 2 - 1
                pygame.draw.line(
                    self.screen,
                    self.grid_color,
                    (center_x, node.area.start.y * (self.ratio + 1) - 1),
                    (center_x, node.area.end.y * (self.ratio + 1) - 1),
                )
                pygame.draw.line(
                    self.screen,
                    self.grid_color,
                    (node.area.start.x * (self.ratio + 1) - 1, center_y),
                    (node.area.end.x * (self.ratio + 1) - 1, center_y),
                )
            else:
                pygame.draw.rect(
                    self.screen,
                    node.area.color,
                    pygame.Rect(
                        node.area.start.x * (self.ratio + 1),
                        node.area.start.y * (self.ratio + 1),
                        (node.area.end.x - node.area.start.x) * (self.ratio + 1) - 1,
                        (node.area.end.y - node.area.start.y) * (self.ratio + 1) - 1,
                    ),
                )
        pygame.display.update()

    def jpeg_image(self):
        new_depth = self.tree.depth() - 1 if self.tree.depth() > 1 else 1
        print(f"Current depth: {self.tree.depth()}")
        print(f"New depth: {new_depth}")
        for node in self.tree:
            if node.depth() == 2:
                node.unite()
        self.tree.collapse()
        self.update()

    def exec(self):
        self.update()
        while not False:
            self.check_events()
            # self.update()


def draw(tree: Quadtree):
    app = WinImage(tree)
    app.exec()
