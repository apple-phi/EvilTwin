import abc
from random import randint

import pygame


from .levels import Level
from .player import Enemy, Player, MOVES, OPPOSITES
from .constants import LEVELS, TILE_SIZE


class Button:
    def __init__(self, x: int, y: int, w: int, h: int, command):
        self.x, self.y, self.w, self.h, self.command = x, y, w, h, command
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        col = [0, 0, 0]
        col[randint(0, 2)] = 255
        self.image.fill(col)

    @staticmethod
    def run(buttons: list["Button"], x, y):
        for b in buttons:
            if b.x <= x <= b.x + b.w and b.y <= y <= b.y + b.h:
                b.command()

    def display(self, screen: pygame.Surface):
        screen.blit(
            pygame.transform.scale(self.image, (self.w, self.h)),
            (self.x, self.y),
        )


class Scene(abc.ABC):
    def __init__(self):
        self.next_scene = None

    @abc.abstractmethod
    def show_on(screen: pygame.Surface):
        ...

    @abc.abstractmethod
    def handle_event(self, event: pygame.event.Event):
        ...


class MenuScreen(Scene):
    def __init__(self):
        super().__init__()
        self.menu = [
            Button(x, 50, TILE_SIZE, TILE_SIZE, lambda n=n: self.enter_level(n))
            for n, x in enumerate(range(0, 1000, TILE_SIZE * 2), 1)
        ]

    def show_on(self, screen: pygame.Surface):
        for b in self.menu:
            b.display(screen)

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            Button.run(self.menu, *pygame.mouse.get_pos())

    def enter_level(self, number: str):
        self.next_scene = LevelScreen(LEVELS / (f"{number}.toml"))


class LevelScreen(Scene):
    def __init__(self, path: str):
        super().__init__()
        self.level = Level(path)
        self.player = Player(self.level)
        self.enemy = Enemy(self.level)

    def show_on(self, screen: pygame.Surface):
        self.level.show_on(screen)
        self.player.move()
        self.enemy.move()
        self.player.animate_on(screen, idle_every=5)
        self.enemy.animate_on(screen, idle_every=5)
        if self.player.finished:
            self.next_scene = MenuScreen()

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.next_scene = MenuScreen()
            elif (
                event.key in MOVES
                and not self.player.is_moving
                and not self.enemy.is_moving
            ):
                self.player.state = MOVES[event.key]
                if self.player.can_move():
                    self.enemy.state = OPPOSITES[self.player.state]
