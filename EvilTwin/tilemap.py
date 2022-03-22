import itertools
from enum import Enum
import io

import numpy as np
import pygame


class Tile(Enum):
    EMPTY = 0
    FLOOR = 1
    WALL = 2
    STAR = 3
    START = 4
    END = 5


def parse_into_arr(path):
    with open(path) as f:
        return np.genfromtxt(
            io.StringIO(" ".join(f.read()).replace("\n ", "\n")), dtype=int
        )


# TileSet Test
class TileSet:
    ...


class TileMap:
    def __init__(self, path: str, tileset: TileSet, rect=None):
        self.array = parse_into_arr(path)
        self.dimensions = self.array.shape[::-1]
        
        self.tileset = tileset

        self.image = pygame.Surface((
            self.dimensions[0] * self.tileset.size, 
            self.dimensions[1] * self.tileset.size
            ))

        self.rect = pygame.Rect(rect) if rect is not None else self.image.get_rect()

    def __getitem__(self, coords):
        x, y = coords
        return self.map[y, x]

    def render(self):
        for (y, x), value in np.ndenumerate(self.array):
            self.image.blit(
                self.tileset[value], (x * self.tileset.size, y * self.tileset.size)
            )

    def __repr__(self):
        return repr(self.array)
