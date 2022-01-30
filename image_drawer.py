
import pygame

from PIL import Image

from .quadtree import Quadtree, Area, Pixel


class WinImage(object):
    """docstring for WinImage"""

    def __init__(self, tree: Quadtree, display=(1080, 1080)):
        pygame.init()
        self.tree = tree
        self.ratio = (display[0] - tree.area.end.x + 1) / tree.area.end.x
        self.grid_color = (177, 177, 177)
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
                    pygame.image.save(self.screen, f"tree_{self.tree.depth()}.jpg")
                elif event.key == pygame.K_e:
                    pygame.quit()
                    exit(0)

    def update(self):
        self.screen.fill((0, 0, 0))
        for node in self.tree:
            if node.is_divided():
                center_x = (node.area.start.x + node.area.end.x) * (self.ratio + 1) / 2 - 1
                center_y = (node.area.start.y + node.area.end.y) * (self.ratio + 1) / 2 - 1
                pygame.draw.circle(self.screen, (255, 0, 0), (center_x, center_y), 2, 3)
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


def main():
    with Image.open("practice_21\\images\\test2.jpeg") as input_img:
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
