import sys

import pygame

pygame.init()
pygame.mixer.music.set_volume(.15)

from .constants import *
from .scenes import TitleScreen


class Game:
    pygame.mouse.set_visible(False)
    def __init__(self):
        self.screen = pygame.display.set_mode((700, 700), pygame.SCALED)

        self.curs = pygame.transform.flip(pygame.transform.scale(pygame.image.load(TILES / "cursor.png").convert_alpha(), (16, 16)), True, False)
        w, h = self.curs.get_size()
        for x in range(w):
            for y in range(h):
                self.curs.set_at((x, y), pygame.Color(150, 0, 255, self.curs.get_at((x, y))[3]))
        pygame.display.set_caption("Mirror Mirror")
        pygame.display.set_icon(STAR_SPRITE)
        self.scene = TitleScreen()

    def run(self):
        clock = pygame.time.Clock()
        while True:
            self.handle_events()
            if self.scene.next_scene is not None:
                self.scene = self.scene.next_scene
            self.scene.show_on(self.screen)
            self.screen.blit(self.curs, pygame.mouse.get_pos())
            pygame.display.flip()
            clock.tick(40)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            self.scene.handle_event(event)
