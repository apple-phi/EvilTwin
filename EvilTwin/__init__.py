import pathlib
import pygame
from .tilemap import TileMap

ASSETS = pathlib.Path(__file__).parent / "assets"


class Level:
    def __init__(self, screen: pygame.Surface, path: str):
        self.screen = screen
        self.map: TileMap = TileMap(path).render()

    def show(self):
        """Render level tilemap, scaled to the screen size."""
        pygame.transform.scale(self.map.image, self.screen.get_size(), self.screen)
        return self


class Game:
    def __init__(self):
        screen = pygame.display.set_mode((640, 480), pygame.SCALED)
        Level(screen, ASSETS / "level.txt").show()
        clock = pygame.time.Clock()
        while True:
            clock.tick(30)
            pygame.display.flip()
