import abc
import math
import itertools

import pygame


from .levels import Level
from .player import Enemy, Player, MOVES, OPPOSITES
from .constants import LEVELS, ASSETS, TILES, STAR_SPRITE
from .user import user_data


class Scene(abc.ABC):
    def __init__(self):
        self.next_scene = None

    @abc.abstractmethod
    def show_on(screen: pygame.Surface):
        ...

    @abc.abstractmethod
    def handle_event(self, event: pygame.event.Event):
        ...


class Transition(Scene):
    def __init__(self, old: Scene, new: Scene, duration=50):
        super().__init__()
        self.old = old
        self.new = new
        self.scenes = old, new
        self.duration = duration
        self.elapsed = 0

    @property
    def fraction_elapsed(self):
        return self.elapsed / self.duration

    @property
    def current_scene(self) -> Scene:
        return self.scenes[self.fraction_elapsed > 0.5]

    def handle_event(self, event):
        self.current_scene.handle_event(event)

    def show_on(self, screen: pygame.Surface):
        self.elapsed += 1
        if self.fraction_elapsed >= 1:
            self.next_scene = self.new


class SlideUpBetween(Transition):
    def __init__(self, old: Scene, new: Scene, duration=50):
        super().__init__(old, new, duration)
        self.image_old = pygame.display.get_surface().copy()
        self.image_new = self.image_old.copy()
        self.image = self.image_new.copy()

    @property
    def fractional_offset(self):
        """Make cubic with turning points at (0, 0) & (d, 1).

        y=-\frac{2}{d^{3}}x^{3}+\frac{3}{d^{2}}x^{2}
        """
        return -2 * self.fraction_elapsed ** 3 + 3 * self.fraction_elapsed ** 2

    def show_on(self, screen: pygame.Surface):
        super().show_on(screen)
        self.old.show_on(self.image_old)
        self.new.show_on(self.image_new)
        self.image.blit(
            self.image_old, (0, -screen.get_height() * self.fractional_offset)
        )
        self.image.blit(
            self.image_new, (0, screen.get_height() * (1 - self.fractional_offset))
        )
        screen.blit(self.image, (0, 0))


class FadeToBlackBetween(Transition):
    def __init__(self, old: Scene, new: Scene, duration=50):
        super().__init__(old, new, duration)
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

    def show_on(self, screen: pygame.Surface):
        super().show_on(screen)
        self.current_scene.show_on(screen)
        self.update_alpha()
        screen.blit(self.veil, (0, 0))


class TitleScreen(Scene):
    title_font = pygame.font.Font(ASSETS / "Pixeboy-font.ttf", 120)
    subtitle_font = pygame.font.Font(ASSETS / "Pixeboy-font.ttf", 40)

    def __init__(self):
        super().__init__()
        self.tick = 0
        self.image = pygame.display.get_surface().copy()
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
            self.next_scene = SlideUpBetween(self, MenuScreen())


class LevelButton:
    image = pygame.image.load(TILES / "014.png")

    def __init__(self, x: float, y: float, w: float, h: float, level: int):
        self.x = x + w / 16  # slight offset due to shadow
        self.y = y + h / 16
        self.w = w
        self.h = h
        self.level = level
        self.scaled_image = pygame.transform.scale(self.image, (w, h))
        self.font = pygame.font.Font(ASSETS / "Pixeboy-font.ttf", int(h / 2))
        self.text = self.font.render(f"{level:0>2}", False, (246, 224, 200))
        self.unlocked = user_data.unlocked(level)
        self.stars = user_data.stars_in(level, 0)
        star_dims = (w / 6, h / 6)
        star_y = y + 1.2 * h - star_dims[1] / 2
        star_centre = x + w / 2 + w / 32 - star_dims[0] / 2
        star_sep = w / 4
        star_positions = [
            (star_centre - star_sep, star_y),
            (star_centre + star_sep, star_y),
            (star_centre, star_y),
        ]
        self.unlocked_stars_positions = star_positions[: self.stars]
        self.unlocked_star_image = pygame.transform.smoothscale(STAR_SPRITE, star_dims)
        self.locked_stars_positions = (
            star_positions[self.stars :] if self.unlocked else []
        )
        self.locked_star_image = self.unlocked_star_image.copy()
        self.locked_star_image.set_alpha(50)
        if not self.unlocked:
            self.text.set_alpha(125)
            self.scaled_image.set_alpha(125)

    def clickable_at(self, x, y) -> bool:
        return (
            self.unlocked
            and self.x <= x <= self.x + self.w
            and self.y <= y <= self.y + self.h
        )

    def show_on(self, screen: pygame.Surface):
        screen.blit(self.scaled_image, (self.x, self.y))
        screen.blit(self.text, (self.x + self.w / 8, self.y + self.h / 2))
        screen.blits(
            [
                (self.unlocked_star_image, coord)
                for coord in self.unlocked_stars_positions
            ]
        )
        screen.blits(
            [(self.locked_star_image, coord) for coord in self.locked_stars_positions]
        )


class MenuScreen(Scene):
    def __init__(self):
        super().__init__()
        screen_width, screen_height = pygame.display.get_surface().get_size()
        width, height = screen_width / 6, screen_height / 6
        self.menu = [
            LevelButton(x, y, width, height, level)
            for level, (y, x) in enumerate(
                itertools.product(
                    range(int(width / 2), screen_width, int(width * 2)),
                    range(int(height / 2), screen_height, int(height * 2)),
                ),
            )
        ]

    def show_on(self, screen: pygame.Surface):
        screen.fill((24, 33, 93))
        for b in self.menu:
            b.show_on(screen)

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            for button in self.menu:
                if button.clickable_at(x, y):
                    self.next_scene = FadeToBlackBetween(
                        self, LevelScreen(button.level)
                    )
                    break
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.next_scene = FadeToBlackBetween(self, TitleScreen())


class LevelScreen(Scene):
    def __init__(self, number: int):
        super().__init__()
        self.number = number
        self.path = LEVELS / f"{number}.toml"
        self.level = Level(self.path)
        self.player = Player(self.level)
        self.enemy = Enemy(self.level)
        self.winner = None

    def show_on(self, screen: pygame.Surface):
        self.level.show_on(screen)
        if self.winner is None:
            self.player.move()
            self.enemy.move()
            self.check_result()
        self.enemy.animate_on(screen, idle_every=5)
        self.player.animate_on(screen, idle_every=5)

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.next_scene = FadeToBlackBetween(self, MenuScreen())
            elif (
                event.key in MOVES
                and not self.player.is_moving
                and not self.enemy.is_moving
                and self.winner is None
            ):
                self.player.state = MOVES[event.key]
                if self.player.can_move():
                    self.enemy.state = OPPOSITES[self.player.state]

    def check_result(self):
        if self.player.xy == self.level.end:
            self.win()
        if (
            self.enemy.stars > 0
            or self.enemy.xy == self.level
            or manhattan_dist(*self.player.xy, *self.enemy.xy) < 1
        ):
            self.lose()

    def win(self):
        self.enemy.state = "hit"
        self.player.state = "idle"
        self.winner = self.player
        user_data.complete(self.number, stars=self.player.stars)
        self.next_scene = FadeToBlackBetween(self, MenuScreen())

    def lose(self):
        self.player.state = "hit"
        self.winner = self.enemy
        self.next_scene = FadeToBlackBetween(self, LevelScreen(self.number))


def manhattan_dist(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)
