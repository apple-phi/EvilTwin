import pathlib
import sys
import pygame
from .tilemap import TileMap, Tile, Level
from .player import Player

ASSETS = pathlib.Path(__file__).parent / "assets"





class Game:
    def __init__(self):
        screen = pygame.display.set_mode((640, 480), pygame.SCALED)
        lvl = Level(screen, ASSETS / "level.txt")

        lvl.show()
        clock = pygame.time.Clock()

        self.pl = Player(lvl, (0, 0))
        while True:
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    case pygame.KEYDOWN:
                        self.parse_event(event.key)


            screen.fill((0, 0, 0))
            lvl.show()
            self.pl.move()
            screen.blit(self.pl.image, (self.pl.xy[0] * Tile.width, self.pl.xy[1] * Tile.height))

            pygame.display.flip()
            clock.tick(30)
    
    def parse_event(self, key):
        if key == pygame.K_s:
            self.pl.path((0, 1))
