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


class TileSet:
    ...


class TileMap:
    def __init__(self, path: str, tileset: TileSet, rect=None):
        self.array = parse_into_arr(path)
        self.dimensions = self.array.shape[::-1]
        self.image = pygame.Surface(self.dimensions)
        self.tileset = tileset
        self.rect = pygame.Rect(rect) if rect is not None else self.image.get_rect()

    def __getitem__(self, coords):
        x, y = coords
        return self.map[y, x]

    def render(self):
        for (i, j), value in np.ndenumerate(self.array):
            self.image.blit(
                self.tileset[value], (i * self.tileset.size, j * self.tileset.size)
            )

    def __repr__(self):
        return repr(self.array)
