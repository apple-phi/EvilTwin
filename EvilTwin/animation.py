import pathlib
import itertools
import pygame
import random

from .constants import SPRITES, STAR_FRACTION, TILE_SIZE


class SpriteAnimation:
    """Animations are retrived as an `itertools.cycle` of pygame images."""

    def __init__(self, path):
        self.animations = {}
        for entry in pathlib.Path(path).iterdir():
            self.load_file(entry) if entry.is_file() else self.load_group(entry)

    def load_file(self, file: pathlib.Path):
        surface = pygame.image.load(file)
        self.animations[file.stem] = [surface]

    def load_group(self, directory: pathlib.Path):
        images = [pygame.image.load(entry) for entry in directory.iterdir()]
        self.animations[directory.stem] = images

    def __getitem__(self, key):
        return itertools.cycle(self.animations[key])


class StarAnimation(SpriteAnimation):
    image = pygame.image.load(SPRITES / "star" / "basic.png")

    def __init__(self):
        super().__init__(SPRITES / "star")
        self.animations["rotate-mini"] = [
            pygame.transform.scale(
                i, (TILE_SIZE * STAR_FRACTION, TILE_SIZE * STAR_FRACTION)
            )
            for i in random_rotate(self.animations["rotate"])
        ]


def random_rotate(lst: list):
    x = random.randrange(0, len(lst))
    return lst[:x] + lst[x:]
