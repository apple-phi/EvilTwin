




"""DON"T USE. This is legacy code. Please use `levels.py` instead."""





from enum import IntEnum
import io
import pathlib

import numpy as np
import pygame

ASSETS = pathlib.Path(__file__).parent / "assets"
TEST_TILE_PATH = ASSETS / "tile.png"


class classproperty:
    def __init__(self, f):
        self.f = f

    def __get__(self, instance, owner):
        return self.f(owner)


class Tile(IntEnum):
    def __new__(cls, value, path):
        obj = int.__new__(cls, value)
        obj._value_ = value
        obj.image = pygame.image.load(path) if path else None
        return obj

    EMPTY = 0, None
    FLOOR = 1, TEST_TILE_PATH
    WALL = 2, TEST_TILE_PATH
    STAR = 3, TEST_TILE_PATH
    START = 4, TEST_TILE_PATH
    END = 5, TEST_TILE_PATH

    @classproperty
    def width(cls) -> int:
        return cls.FLOOR.image.get_width()

    @classproperty
    def height(cls) -> int:
        return cls.FLOOR.image.get_height()


def parse_into_arr(path):
    with open(path) as f:
        return np.genfromtxt(
            io.StringIO(" ".join(f.read()).replace("\n ", "\n")), dtype=int
        )


class TileMap:
    def __init__(self, path: str, rect=None):
        self.array = parse_into_arr(path)
        self.dimensions = self.array.shape[::-1]
        self.image = pygame.Surface(
            (
                self.dimensions[0] * Tile.width,
                self.dimensions[1] * Tile.height,
            )
        )
        self.rect = pygame.Rect(rect) if rect is not None else self.image.get_rect()

    def __getitem__(self, coords):
        x, y = coords
        return self.array[y, x]

    def render(self):
        self.image.blits(
            [
                (Tile(value).image, (x * Tile.width, y * Tile.height))
                for (y, x), value in np.ndenumerate(self.array)
                if Tile(value).image is not None
            ]
        )
        return self

    def __repr__(self):
        return repr(self.array)

class Level:
    def __init__(self, screen: pygame.Surface, path: str):
        self.screen = screen
        self.map: TileMap = TileMap(path).render()

    def show(self):
        """Render level tilemap, scaled to the screen size."""
        pygame.transform.scale(self.map.image, self.screen.get_size(), self.screen)
        return self
    
    def __getitem__(self, key):
        return self.map[key]