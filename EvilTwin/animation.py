import pathlib
import itertools
import pygame


class SpriteAnimation:
    """Single images are stores as pygame images;
    Animations are stored as an `itertools.cycle` of pygame images."""

    def __init__(self, path):
        self.animations = {}
        for entry in pathlib.Path(path).iterdir():
            self.load_file(entry) if entry.is_file() else self.load_group(entry)

    def load_file(self, file: pathlib.Path):
        self.animations[file.stem] = pygame.image.load(file)

    def load_group(self, directory: pathlib.Path):
        images = [pygame.image.load(entry) for entry in directory.iterdir()]
        self.animations[directory.stem] = itertools.cycle(images)

    def __getitem__(self, key):
        return self.animations[key]
