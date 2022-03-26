import io

import pygame
import numpy as np
import toml

from .animation import StarAnimation
from .constants import (
    STAR_FRAME_DELAY,
    TILE_SIZE,
    STAR_OFFSET,
    STAR_SPRITE,
    TILES,
    WALLS,
    ITEMS,
    SOUNDS,
)


class Level:
    def __init__(self, path: str):
        with open(path) as f:
            self.data = toml.load(f)
        self.array = np.loadtxt(io.StringIO(self.data["map"]), delimiter=",", dtype=str)
        self.dimensions = self.array.shape[::-1]
        self.stars: list[list[int]] = self.data["stars"]
        self.start: list[int] = self.data["start"]
        self.end: tuple[int] = tuple(self.data["end"])
        #I, Alex, take full responsibility for this crime \/
        self.switch: tuple[int] = tuple(self.data["switch"]) if "switch" in self.data else [-1,-1]
        self.activated = False

        self.items: dict[str, list[list[int]]] = self.data["items"]
        self.image = pygame.Surface(
            (
                self.dimensions[0] * TILE_SIZE,
                self.dimensions[1] * TILE_SIZE,
            )
        )
        self.star_animations = [StarAnimation()["rotate-mini"] for _ in self.stars]
        self.tick = 0
        self._load_all()._update_stars()._render_all()

    def _load_all(self) -> "Level":
        return self._load_tiles()._load_items()

    def _render_all(self) -> "Level":
        return self._render_tiles()._render_items()._render_stars()._render_switch()

    def _load_tiles(self) -> "Level":
        self.tileset = {}
        for tile in self.array.flatten():
            if tile not in self.tileset:
                self.tileset[tile] = pygame.image.load(TILES / f"{tile}.png")
        self.tileset['005'] = pygame.image.load(TILES / "005.png")
        return self

    def _render_tiles(self) -> "Level":
        self.image.blits(
            [
                (self.tileset[tile if tile!='004'or not self.activated else'005'], (x * TILE_SIZE, y * TILE_SIZE))
                for (y, x), tile in np.ndenumerate(self.array)
            ]
        )
        self.image.blits([
            (pygame.image.load(TILES / "entrance.png"), (self.start[0] * TILE_SIZE, self.start[1] * TILE_SIZE)),
            (pygame.image.load(TILES / "exit.png"), (self.end[0] * TILE_SIZE, self.end[1] * TILE_SIZE))
        ])
        return self

    def _load_items(self) -> "Level":
        self.itemset = {}
        for item in self.items:
            if item not in self.itemset:
                self.itemset[item] = pygame.image.load(TILES / f"{item}.png")
        return self

    def _render_items(self) -> "Level":
        self.image.blits(
            [
                (self.itemset[item], (x * TILE_SIZE, y * TILE_SIZE))
                for item, positions in self.items.items()
                for x, y in positions
                if (item != '086' or self.activated) and (item != '004' or not self.activated)
            ]
        )
        return self

    def _render_switch(self) -> "Level":
        if not self.activated:
            self.image.blit(
                pygame.image.load(TILES / "switch_open.png"), (self.switch[0] * TILE_SIZE, self.switch[1] * TILE_SIZE)
            )
        else:
            self.image.blit(
                pygame.image.load(TILES / "switch_closed.png"), (self.switch[0] * TILE_SIZE, self.switch[1] * TILE_SIZE)
            )
        return self

    def _update_stars(self) -> "Level":
        self.star_frames = [next(anim) for anim in self.star_animations]
        return self

    def _render_stars(self) -> "Level":
        self.image.blits(
            [
                (
                    frame,
                    (x * TILE_SIZE + STAR_OFFSET, y * TILE_SIZE + STAR_OFFSET),
                )
                for (x, y), frame in zip(self.stars, self.star_frames)
            ]
        )
        return self

    def collect_star(self, x, y) -> bool:
        if [x, y] in self.stars:
            s=pygame.mixer.Sound(SOUNDS/'fx'/'bonus.mp3')
            s.set_volume(0.15)
            s.play()
            self.stars.remove([x, y])
            self._render_all()
            return True
        return False

    def flip_switch(self, x, y) -> bool:
        if (x, y) == self.switch:
            self.activated = True
            s=pygame.mixer.Sound(SOUNDS/'fx'/'destroyed_stones.mp3')
            s.set_volume(0.15)
            s.play()
            return True
        return False

    @property
    def stars_found(self) -> int:
        return 3 - len(self.stars)

    def show_on(self, screen):
        """Render level tilemap, scaled to the screen size."""
        if self.tick % STAR_FRAME_DELAY == 0:
            self._update_stars()
        self._render_all()
        pygame.transform.scale(self.image, screen.get_size(), screen)
        self.tick += 1
        return self

    def get_screen(self, size, **kwargs) -> pygame.Surface:
        """Helper to set the screen so that each tile is a square of side `size`."""
        return pygame.display.set_mode(
            (self.dimensions[0] * size, self.dimensions[1] * size), **kwargs
        )

    def wall_at(self, x, y):
        return (
            not 0 <= x < self.dimensions[1]
            or not 0 <= y < self.dimensions[1]
            or self.array[x, y] in WALLS+['004']*(not self.activated)
            or any([y, x] in v for k,v in self.items.items() 
            if (k != '086' or self.activated))
        )

    def star_at(self, coords):
        return coords in self.stars
