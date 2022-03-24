from enum import Enum

import numpy as np
import pygame

from .levels import Level
from .constants import SPRITES
from .animation import SpriteAnimation

VECTORS = {
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

OPPOSITES = {
    "up": "down",
    "down": "up",
    "left": "right",
    "right": "left",
}


class BaseCharacter:
    def __init__(self, level: Level, speed=1 / 4):
        self.level = level
        self.speed = speed
        self.is_moving = False
        self.stars = 0

        self.state = "idle"  # idle | left | right | up | down | rotate
        self.tick = 0

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._state = value
        self.dir = VECTORS.get(value, (0, 0))
        self.is_moving = value != "idle"
        print(self.__class__.__name__,self._state,self.dir,self.is_moving)

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
        if self.xy[0].is_integer() and self.xy[1].is_integer():
            self.dest = [self.xy[0] + self.dir[0], self.xy[1] + self.dir[1]]

            # If have reached a wall, stop moving
            if self.level.wall_at(int(self.dest[1]), int(self.dest[0])):
                self.state = "idle"  # self.state is a @property so it should auto-change self.dir and self.is_moving

        if self.is_moving:
            self.xy = (
                self.xy[0] + self.speed * self.dir[0],
                self.xy[1] + self.speed * self.dir[1],
            )

        self.stars += self.level.collect_star(*self.xy)

    def can_move(self):
        """Check if character can move in current direction,
        assuming it is currently fully on a square."""
        return not self.level.wall_at(
            int(self.xy[1] + self.dir[1]), int(self.xy[0] + self.dir[0])
        )


class Player(BaseCharacter):
    def __init__(self, level: Level):
        super().__init__(level)
        self.xy = tuple(map(float, level.start))
        self.animation = SpriteAnimation(SPRITES / "player")
        self.finished = False

    def __repr__(self):
        return f"Player - Current: {self.xy}, Dir: {self.dir}, moving: {self.is_moving}"


class Enemy(BaseCharacter):
    def __init__(self, level: Level):
        super().__init__(level)
        self.xy = tuple(map(float, level.end))
        self.animation = SpriteAnimation(SPRITES / "enemy")
