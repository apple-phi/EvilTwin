import sys

import pygame

pygame.init()
pygame.mixer.music.set_volume(0.15)

from .constants import *
from .scenes import TitleScreen


CURSOR = pygame.transform.smoothscale(
    pygame.image.load(ASSETS / "cursor.png"), (40, 40)
)
pygame.mouse.set_visible(False)


class Game:
    pygame.mouse.set_visible(False)

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
            self.screen.blit(CURSOR, pygame.mouse.get_pos())
            pygame.display.flip()
            clock.tick(40)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            self.scene.handle_event(event)
