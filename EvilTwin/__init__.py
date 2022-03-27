import sys

import pygame

pygame.init()
pygame.mixer.music.set_volume(0.15)

from .constants import *
from .scenes import TitleScreen

pygame.mouse.set_cursor(
    pygame.cursors.Cursor(
        (0, 0),
        pygame.image.load(ASSETS / "cursor.png"),
    )
)


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((700, 700), pygame.SCALED)
        pygame.display.set_caption("Mirror Mirror")
        pygame.display.set_icon(pygame.image.load(ASSETS / "cute_star.png"))
        self.scene = TitleScreen()

    def run(self):
        clock = pygame.time.Clock()
        while True:
            self.handle_events()
            if self.scene.next_scene is not None:
                self.scene = self.scene.next_scene
            self.scene.show_on(self.screen)
            pygame.display.flip()
            clock.tick(40)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            self.scene.handle_event(event)
