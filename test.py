import sys
import pygame as pg

clock = pg.time.Clock()

WIDTH = 500
HEIGHT = 500

BLACK = (0, 0, 0, 255)
WHITE = (255, 255, 255, 100)
RED = (255, 0, 0, 100)
GREEN = (0, 255, 0, 100)
BLUE = (0, 0, 255, 100)
EMPTY = pg.Color(0, 0, 0, 0)


class Renderer:
    def __init__(self):
        pg.init()
        self.RES = self.WIDTH, self.HEIGHT = 1200, 600
        self.H_WIDTH, self.H_HEIGHT = self.WIDTH // 2, self.HEIGHT // 2
        self.FPS = 60

        self.screen = pg.display.set_mode(self.RES)
        self.surface = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)

        self.clock = pg.time.Clock()
        self.event_handlers = []

    def draw(self):
        self.screen.fill(pg.Color('darkslategray'))
        self.surface.fill(EMPTY)

        # draw the things
        pg.draw.circle(self.surface, WHITE, (100, 100), 10)

        self.screen.blit(self.surface, (0, 0))
        pg.display.flip()

    def attach_event_handler(self, handler):
        self.event_handlers.append(handler)

    def handle_events(self):
        for event in pg.event.get():
            for handler in self.event_handlers:
                handler(event)

    def run(self):
        while True:
            self.draw()
            self.handle_events()
            pg.display.set_caption(str(int(self.clock.get_fps())))
            self.clock.tick(self.FPS)


def handle_quit(event):
    if event.type == pg.QUIT:
        exit()


def main():
    renderer = Renderer()
    renderer.attach_event_handler(handle_quit)
    renderer.run()


if __name__ == '__main__':
    main()

# pg.init()
#
# screen = pg.display.set_mode((WIDTH, HEIGHT))
#
#
# while True:
#     time_elapsed_ms = clock.tick(100)
#
#     for event in pg.event.get():
#         if event.type == pg.QUIT:
#             sys.exit()
#
#     # reset screen
#     screen.fill(BLACK)
#
#     # draw things here
#
#     # refresh screen
#     pg.display.update()
