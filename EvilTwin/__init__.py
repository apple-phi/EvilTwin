import pathlib
import sys
from random import randint
from typing import Callable
from .constants import *

import pygame

from .constants import LEVELS, TILE_SIZE
from .levels import Level
from .player import Player

LOADING, IN_MENU, IN_LEVEL = 0, 1, 2
MOVES = {
    pygame.K_w: "up",
    pygame.K_a: "left",
    pygame.K_s: "down",
    pygame.K_d: "right",
}

class Button:
    def __init__(self, x: int, y: int, w: int, h: int, command: Callable):
        self.x,self.y,self.w,self.h,self.command = x,y,w,h,command
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        col = [0, 0, 0]
        col[randint(0,2)] = 255
        self.image.fill(col)


    @staticmethod
    def run(buttons: list["Button"], x, y):
        for b in buttons:
            if b.x <= x <= b.x + b.w and b.y <= y <= b.y + b.h:
                b.command()
    def display(self,screen : pygame.Surface):
        screen.blit(
            pygame.transform.scale(self.image, (self.w, self.h)),
            (self.x, self.y),
        )



class Game:
    def __init__(self):
        screen = pygame.display.set_mode((640, 480), pygame.SCALED)
        pygame.display.set_caption("Game Name")
        pygame.display.set_icon(STAR_SPRITE)
        self.level = Level(LEVELS / "1.toml")
        self.state = IN_MENU
        self.level.show_on(screen)
        clock = pygame.time.Clock()

        self.player = Player(self.level)

        self.menu = [
            Button(
                x,
                50,
                TILE_SIZE,
                TILE_SIZE,
                lambda n=n: self.enter_level(f"{n}.toml")
            )
            for n,x in enumerate(range(0, 1000, TILE_SIZE * 2),1)
        ]

        while True:
            self.check_events()
            if self.state == IN_MENU:
                for b in self.menu:
                    b.display(screen)
            elif self.state == IN_LEVEL:
                self.level.show_on(screen)
                self.player.move()
                self.player.animate_on(screen, idle_every=5)

                if self.player.finished:
                    self.state = IN_MENU

            pygame.display.flip()
            clock.tick(30)

    def parse_event(self, key):
        if self.state == IN_LEVEL:
            if key == pygame.K_ESCAPE:
                self.state = IN_MENU
            elif key in MOVES and not self.player.is_moving:
                    self.player.state = MOVES[key]

    def check_events(self):
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                case pygame.KEYDOWN:
                    self.parse_event(event.key)
                case pygame.MOUSEBUTTONDOWN:
                    if self.state == IN_MENU:
                        Button.run(self.menu,*pygame.mouse.get_pos())
    
    def enter_level(self,level):
        self.state = IN_LEVEL
        self.level = Level(LEVELS / level)
        self.player = Player(self.level)
