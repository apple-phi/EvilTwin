from enum import Enum

import numpy as np
import pygame

from .levels import Level
from .constants import SPRITES
from .animation import SpriteAnimation

VECTORS = {
    "idle": (0, 0),
    "left": (-1, 0),
    "right": (1, 0),
    "up": (0, -1),
    "down": (0, 1),
}

MOVES = {
    pygame.K_w: "up",
    pygame.K_a: "left",
    pygame.K_s: "down",
    pygame.K_d: "right",
}


class BaseCharacter:
    def __init__(self, level: Level):
        self.level = level
        self.is_moving = False
        self.dir = (0, 0)
        self.stars = 0

        self._state = "idle"  # idle | left | right | up | down | rotate
        self.tick = 0

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._state = value
        self.dir = VECTORS[value]
        self.is_moving = value != "idle"

    def animate(self, idle_every=1):
        if self.tick == 0 or self.state != "idle":
            self.image = next(self.animation[self.state])
        self.tick = (self.tick + 1) % idle_every

    def show_on(self, screen: pygame.Surface):
        screen_width, screen_height = screen.get_size()
        n_tiles_x, n_tiles_y = self.level.dimensions
        width, height = screen_width // n_tiles_x, screen_height // n_tiles_y
        screen.blit(
            pygame.transform.scale(self.image, (width, height)),
            (self.xy[0] * width, self.xy[1] * height),
        )

    def animate_on(self, screen: pygame.Surface, idle_every=1):
        self.animate(idle_every)
        self.show_on(screen)

    def move(self):
        """
        Actually moves the player along in the current direction of movement.
        """

        # If currently moving
        if self.is_moving:
            trial_dest = [self.xy[0] + self.dir[0], self.xy[1] + self.dir[1]]

            # If have reached a wall, stop moving
            if self.level.wall_at(trial_dest[1], trial_dest[0]):
                self.state = "idle"
                self.is_moving = False

            # Else, move
            else:
                self.xy = trial_dest

        self.stars += self.level.collect_star(*self.xy)


class Player(BaseCharacter):
    def __init__(self, level: Level):
        super().__init__(level)
        self.xy = level.start
        self.animation = SpriteAnimation(SPRITES / "player")
        self.finished = False

    def move(self):
        super().move()
        if len(self.level.stars) == 0 and self.xy == self.level.end:
            self.finished = True

    def __repr__(self):
        return f"Player - Current: {self.xy}, Dir: {self.dir}, moving: {self.is_moving}"


class Enemy(BaseCharacter):
    def __init__(self, level: Level):
        super().__init__(level)
        self.xy = level.end
        self._dir = (0, 0)
        self.animatation = SpriteAnimation(SPRITES / "enemy")

    @property
    def dir(self):
        return self._dir

    @dir.setter
    def dir(self, value):
        """Set the direction to be the opposite of the player"""
        self._dir = (-value[0], -value[1])

    def move(self):
        super().move()
