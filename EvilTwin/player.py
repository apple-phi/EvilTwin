import numpy as np
import pygame

from .levels import TILE_SIZE, Level


class Player:
    def __init__(self, level: Level, is_enemy=False):
        self.level = level
        self.xy = level.start
        self.is_enemy = is_enemy
        self.dest = self.xy

        self.is_moving = False
        self.dir = (0, 0)

        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill((255, 0, 0))

    def show_on(self, screen: pygame.Surface):
        screen_width, screen_height = screen.get_size()
        n_tiles_x, n_tiles_y = self.level.dimensions
        width, height = screen_width // n_tiles_x, screen_height // n_tiles_y
        screen.blit(
            pygame.transform.scale(self.image, (width, height)),
            (self.xy[0] * width, self.xy[1] * height),
        )

    def path(self, xy):
        """
        Chooses the player's destination in the x and/or y direction based on a vector
        ranging from [-1,-1] to [1,1]
        """

        mov = self.xy

        # While the current tile dest is blank, move along by 1
        # This is a while True which gets broken as soon as a wall is met.
        while (
            mov[0] + xy[0] < self.level.dimensions[0]
            and mov[1] + xy[1] < self.level.dimensions[1]
            and not self.level.wall_at(mov[0] + xy[0], mov[1] + xy[1])
        ):
            mov = (mov[0] + xy[0], mov[1] + xy[1])

        self.dest = mov

        # If the end result causes movement, set movement flag to true, set direction.
        if self.dest != self.xy:
            self.is_moving = True
            self.dir = xy

        # Otherwise, set direction to null.
        else:
            self.dir = (0, 0)

        print(self.dest)

    def move(self):
        """
        Actually moves the player along in the current direction of movement.
        """

        # If currently moving
        if self.is_moving:
            trial_dest = (self.xy[0] + self.dir[0], self.xy[1] + self.dir[1])

            # If have reached a wall, stop moving
            if self.level.wall_at(trial_dest[1], trial_dest[0]):
                self.dir = (0, 0)
                self.is_moving = False

            # Else, move
            else:
                self.xy = trial_dest

    def __repr__(self):
        return f"Player - Current: {self.xy}, Dest: {self.dest}, Dir: {self.dir}, moving: {self.is_moving}"


class Enemy(Player):
    def move(self, xy):
        return super().move(-xy[0], -xy[1])
