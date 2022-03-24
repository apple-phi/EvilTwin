import io

import pygame
import numpy as np
import toml

from .constants import TILE_SIZE, STAR_OFFSET, STAR_SPRITE, TILES, WALLS


class Level:
    def __init__(self, path: str):
        with open(path) as f:
            self.data = toml.load(f)
        self.array = np.loadtxt(io.StringIO(self.data["map"]), delimiter=",", dtype=str)
        self.dimensions = self.array.shape[::-1]
        self.stars: list[list[int]] = self.data["stars"]
        self.start: list[int] = self.data["start"]
        self.end: list[int] = self.data["end"]
        self.image = pygame.Surface(
            (
                self.dimensions[0] * TILE_SIZE,
                self.dimensions[1] * TILE_SIZE,
            )
        )
        self._load_tiles()._render_tiles()._render_stars()

    def _load_tiles(self) -> "Level":
        self.tileset = {}
        for _, tile in np.ndenumerate(self.array):
            if tile not in self.tileset:
                with open(TILES / f"{tile}.png") as f:
                    self.tileset[tile] = pygame.image.load(f)
        return self

    def _render_tiles(self) -> "Level":
        self.image.blits(
            [
                (self.tileset[tile], (x * TILE_SIZE, y * TILE_SIZE))
                for (y, x), tile in np.ndenumerate(self.array)
            ]
        )
        return self

    def _render_stars(self) -> "Level":
        self.image.blits(
            [
                (
                    STAR_SPRITE,
                    (y * TILE_SIZE + STAR_OFFSET, x * TILE_SIZE + STAR_OFFSET),
                )
                for x, y in self.stars
            ]
        )

    def check_for_star(self, x, y) -> "Level":
        if [x, y] in self.stars:
            self.stars.remove([x, y])
            self._render_stars()
        return self

    @property
    def stars_found(self) -> int:
        return 3 - len(self.stars)

    def show_on(self, screen):
        """Render level tilemap, scaled to the screen size."""
        pygame.transform.scale(self.image, screen.get_size(), screen)
        return self

    def get_screen(self, size, **kwargs) -> pygame.Surface:
        """Helper to set the screen so that each tile is a square of side `size`."""
        return pygame.display.set_mode(
            (self.dimensions[0] * size, self.dimensions[1] * size), **kwargs
        )

    def wall_at(self, x, y):
        return self.array[y, x] in WALLS

    def star_at(self, coords):
        return coords in self.stars
