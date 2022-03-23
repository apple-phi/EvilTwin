import pathlib
import sys
import pygame

from .levels import Level
from .constants import TILE_SIZE, LEVELS
from .player import Player


class Game:
    def __init__(self):
        screen = pygame.display.set_mode((640, 480), pygame.SCALED)
        level = Level(LEVELS / "test.toml")

        level.show_on(screen)
        clock = pygame.time.Clock()

        self.pl = Player(level, (0, 0))
        while True:
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    case pygame.KEYDOWN:
                        self.parse_event(event.key)


            screen.fill((0, 0, 0))
            level.show_on(screen)
            self.pl.move()
            self.pl.show_on(screen)

            pygame.display.flip()
            clock.tick(30)
    
    def parse_event(self, key):
        if key == pygame.K_s:
            self.pl.path((0, 1))
