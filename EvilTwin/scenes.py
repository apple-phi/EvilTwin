import abc
import math
from random import randint

import pygame


from .levels import Level
from .player import Enemy, Player, MOVES, OPPOSITES
from .constants import LEVELS, TILE_SIZE, ASSETS


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


class FadeToBlackBetween(Scene):
    def __init__(self, old: Scene, new: Scene, duration=50):
        super().__init__()
        self.old = old
        self.new = new
        self.scenes = old, new
        self.duration = duration
        self.elapsed = 0
        self.veil = pygame.display.get_surface().copy()
        self.veil.fill((0, 0, 0))

    def update_alpha(self) -> float:
        """Make quartic through (0, 0) -> (d/2, 1) -> (d, 0)

        y=\left(\frac{4x\left(x-d\right)}{d^{2}}\right)^{2}
        """
        return self.veil.set_alpha(
            255
            * (4 * self.elapsed * (self.elapsed - self.duration) / self.duration ** 2)
            ** 2
        )

    @property
    def current_scene(self) -> Scene:
        return self.scenes[self.elapsed > self.duration / 2]

    def show_on(self, screen: pygame.Surface):
        self.current_scene.show_on(screen)
        self.update_alpha()
        screen.blit(self.veil, (0, 0))
        self.elapsed += 1
        if self.elapsed >= self.duration:
            self.next_scene = self.new

    def handle_event(self, event):
        self.current_scene.handle_event(event)


class TitleScreen(Scene):
    title_font = pygame.font.Font(ASSETS / "Pixeboy-font.ttf", 120)
    subtitle_font = pygame.font.Font(ASSETS / "Pixeboy-font.ttf", 40)

    def __init__(self):
        super().__init__()
        self.tick = 0
        self.image = pygame.display.get_surface()
        top_half = pygame.surface.Surface(
            (self.image.get_width(), self.image.get_height() / 2)
        )
        bottom_half = top_half.copy()
        top_half.fill((225, 124, 183))
        top_half.blit(self.title_font.render("Mirror", False, (24, 33, 93)), (104, 290))
        bottom_half.fill((24, 33, 93))
        bottom_half.blit(
            self.title_font.render("Mirror", False, (225, 124, 183)), (104, 290)
        )
        self.image.blit(bottom_half, (0, 0))
        self.image = pygame.transform.rotate(self.image, 180)
        self.image.blit(top_half, (0, 0))
        self.subtitle = self.subtitle_font.render(
            "Click anywhere to start", False, (246, 224, 200)
        )

    def show_on(self, screen: pygame.Surface):
        screen.blit(self.image, (0, 0))
        self.subtitle.set_alpha(round(255 * math.cos(self.tick / 30) ** 2))
        self.tick += 1
        screen.blit(
            self.subtitle,
            (150, 550),
        )

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONUP:
            self.next_scene = FadeToBlackBetween(self, MenuScreen())


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
        self.next_scene = FadeToBlackBetween(
            self, LevelScreen(LEVELS / (f"{number}.toml"))
        )


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
        self.check_result()

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.next_scene = FadeToBlackBetween(self, MenuScreen())
            elif (
                event.key in MOVES
                and not self.player.is_moving
                and not self.enemy.is_moving
            ):
                self.player.state = MOVES[event.key]
                if self.player.can_move():
                    self.enemy.state = OPPOSITES[self.player.state]

    def check_result(self):
        print(self.player.xy, self.level.end)
        if len(self.level.stars) == 0 and self.player.xy == self.level.end:
            self.win()
        if (
            self.enemy.stars > 0
            or self.enemy.xy == self.level
            or manhattan_dist(*self.player.xy, *self.enemy.xy) < 1
        ):
            self.lose()

    def win(self):
        self.enemy.state = "hit"
        self.next_scene = FadeToBlackBetween(self, MenuScreen())

    def lose(self):
        self.player.state = "hit"
        self.next_scene = FadeToBlackBetween(self, MenuScreen())


def manhattan_dist(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)
