from enum import IntEnum
import io
import pathlib

import numpy as np
import pygame

ASSETS = pathlib.Path(__file__).parent / "assets"
TEST_TILE_PATH = ASSETS / "tile.png"


class Tile(IntEnum):
    def __new__(cls, value, path):
        obj = int.__new__(cls, value)
        obj._value_ = value
        obj.image = pygame.image.load(path)
        return obj

    EMPTY = 0, TEST_TILE_PATH
    FLOOR = 1, TEST_TILE_PATH
    WALL = 2, TEST_TILE_PATH
    STAR = 3, TEST_TILE_PATH
    START = 4, TEST_TILE_PATH
    END = 5, TEST_TILE_PATH


def parse_into_arr(path):
    with open(path) as f:
        return np.genfromtxt(
            io.StringIO(" ".join(f.read()).replace("\n ", "\n")), dtype=int
        )


class TileMap:
    def __init__(self, path: str, tile_size=32, rect=None):
        self.array = parse_into_arr(path)
        self.dimensions = self.array.shape[::-1]
        self.image = pygame.Surface(
            (
                self.dimensions[0] * tile_size,
                self.dimensions[1] * tile_size,
            )
        )
        self.tile_size = tile_size
        self.rect = pygame.Rect(rect) if rect is not None else self.image.get_rect()

    def __getitem__(self, coords):
        x, y = coords
        return self.map[y, x]

    def render(self):
        self.image.blits(
            [
                (Tile(value).image, (x * self.tile_size, y * self.tile_size))
                for (y, x), value in np.ndenumerate(self.array)
            ]
        )

    def __repr__(self):
        return repr(self.array)
