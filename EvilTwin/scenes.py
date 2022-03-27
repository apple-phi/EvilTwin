import abc
import math
import itertools

import pygame
from textwrap import dedent


from .levels import Level
from .player import Enemy, Player, MOVES, OPPOSITES
from .constants import LEVELS, ASSETS, TILES, STAR_SPRITE, SOUNDS
from .user import user_data
from .animation import StarAnimation

CURRENT_PAGE = 0
FURTHEST_PAGE = 0


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
        return -2 * self.fraction_elapsed**3 + 3 * self.fraction_elapsed**2

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
            * (4 * self.elapsed * (self.elapsed - self.duration) / self.duration**2)
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

        pygame.mixer.music.load(SOUNDS / "loading.wav")
        pygame.mixer.music.play(-1, 0.0)

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
            pygame.mixer.music.load(SOUNDS / "menu.wav")
            pygame.mixer.music.set_volume(0.15)
            pygame.mixer.music.play(-1, 0.0)
            self.next_scene = SlideUpBetween(self, IntroScreen())


class ChangeButton:
    image = pygame.image.load(TILES / "014.png")

    def __init__(self, x, y, w, h, right):
        self.x = x + w / 16  # slight offset due to shadow
        self.y = y + h / 16
        self.w = w
        self.h = h
        self.right = right
        self.scaled_image = pygame.transform.scale(self.image, (w, h))
        self.font = pygame.font.Font(ASSETS / "Pixeboy-font.ttf", int(h / 2))
        self.text = self.font.render(">" if right else "<", False, (246, 224, 200))

    def clickable_at(self, x, y) -> bool:
        return self.x <= x <= self.x + self.w and self.y <= y <= self.y + self.h

    def show_on(self, screen: pygame.Surface):
        screen.blit(self.scaled_image, (self.x, self.y))
        screen.blit(self.text, (self.x + self.w / 3, self.y + self.h / 3))


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
            star_positions[self.stars :] if user_data.completed(level) else []
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
        self.font = pygame.font.Font(
            ASSETS / "Pixeboy-font.ttf", int(screen_height / 12)
        )

        self.menu = [
            LevelButton(x, y, width, height, level + CURRENT_PAGE * 9)
            for level, (y, x) in enumerate(
                itertools.product(
                    range(int(width / 2), screen_width, int(width * 2)),
                    range(int(height / 2), screen_height, int(height * 2)),
                ),
            )
        ]

        self.changes = [
            ChangeButton(
                screen_width - width / 3, height / 6, width / 6, height / 6, True
            ),
            ChangeButton(width / 6, height / 6, width / 6, height / 6, False),
        ]
        if CURRENT_PAGE == -1:
            self.changes.pop(1)
        elif CURRENT_PAGE == FURTHEST_PAGE:
            self.changes.pop(0)
        if CURRENT_PAGE == FURTHEST_PAGE == 0:
            self.changes = []

    def show_on(self, screen: pygame.Surface):
        screen.fill((24, 33, 93))
        for b in self.menu + self.changes:
            b.show_on(screen)

    def handle_event(self, event: pygame.event.Event):
        global CURRENT_PAGE
        if event.type == pygame.MOUSEBUTTONDOWN and CURRENT_PAGE > -1:
            x, y = pygame.mouse.get_pos()
            for button in self.menu:
                if button.clickable_at(x, y):
                    self.next_scene = FadeToBlackBetween(
                        self, LevelScreen(button.level)
                    )
                    break
            for button in self.changes:
                if button.clickable_at(x, y):
                    if button.right and CURRENT_PAGE < FURTHEST_PAGE:
                        CURRENT_PAGE += 1

                        self.next_scene = FadeToBlackBetween(self, MenuScreen())
                    elif not button.right:
                        CURRENT_PAGE -= 1
                        if CURRENT_PAGE == -1:
                            self.next_scene = MenuScreen()
                        else:
                            self.next_scene = FadeToBlackBetween(self, MenuScreen())
                    break
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            for button in self.changes:
                if button.clickable_at(x, y):
                    if button.right and CURRENT_PAGE < FURTHEST_PAGE:
                        CURRENT_PAGE += 1
                        self.next_scene = FadeToBlackBetween(self, MenuScreen(), 1)
                    elif not button.right and CURRENT_PAGE > -1:
                        CURRENT_PAGE -= 1
                        if CURRENT_PAGE == -1:
                            self.next_scene = FadeToBlackBetween(self, MenuScreen(), 1)
                        else:
                            self.next_scene = FadeToBlackBetween(self, MenuScreen())
                    break

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.mixer.music.stop()
            self.next_scene = FadeToBlackBetween(self, TitleScreen())


class LevelScreen(Scene):
    font = pygame.font.Font(ASSETS / "Pixeboy-font.ttf", 40)
    text1 = font.render("Collect the stars", False, (246, 224, 200))
    text2 = font.render("&", False, (246, 224, 200))
    text3 = font.render("reach the end", False, (246, 224, 200))

    def __init__(self, number: int):
        super().__init__()
        self.number = number
        self.path = LEVELS / f"{number}.toml"
        self.level = Level(self.path)
        self.player = Player(self.level)
        self.enemy = Enemy(self.level)
        self.winner = None
        self.esc = pygame.transform.scale(
            pygame.image.load(TILES / "esc.png").convert_alpha(), (48, 48)
        )

        pygame.mixer.music.load(SOUNDS / "battle.wav")
        pygame.mixer.music.set_volume(0.05)
        pygame.mixer.music.play(-1, 0.0)

    def show_on(self, screen: pygame.Surface):
        self.level.show_on(screen)
        if self.number == 0:
            screen.blit(self.text1, (165, 205))
            screen.blit(self.text2, (300, 235))
            screen.blit(self.text3, (200, 265))
        self.enemy.move()
        if self.winner is None:
            self.player.move()
            self.check_result()
        self.enemy.animate_on(screen, idle_every=5)
        self.player.animate_on(screen, idle_every=5)
        screen.blit(self.esc, (12, 12))

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.next_scene = FadeToBlackBetween(self, MenuScreen())
            elif event.key == pygame.K_r:
                self.next_scene = FadeToBlackBetween(self, LevelScreen(self.number))
            elif (
                event.key in MOVES
                and not self.player.is_moving
                and not self.enemy.is_moving
                and self.winner is None
            ):
                self.player.state = MOVES[event.key]
                if self.player.can_move() and self.number != "Final":
                    s = pygame.mixer.Sound(SOUNDS / "fx" / "monster_1.mp3")
                    s.set_volume(0.15)
                    s.play()
                    self.enemy.state = OPPOSITES[self.player.state]

    def check_result(self):
        if self.player.xy == self.level.end:
            s = pygame.mixer.Sound(SOUNDS / "fx" / "fantasy.mp3")
            s.set_volume(0.15)
            s.play()
            self.win()
        if manhattan_dist(*self.player.xy, *self.enemy.xy) < 1:
            s = pygame.mixer.Sound(SOUNDS / "fx" / "start-level.wav")
            s.set_volume(0.1)
            s.play()
            self.lose()

    def win(self):
        self.enemy.state = "hit"
        self.player.state = "idle"
        self.winner = self.player
        pygame.mixer.music.stop()
        user_data.complete(self.number, stars=self.player.stars)

        if self.number != 8:
            self.next_scene = FadeToBlackBetween(self, MenuScreen())
            return
        self.next_scene = FinalScene()

    def lose(self):
        self.player.state = "hit"
        self.winner = self.enemy
        pygame.mixer.music.stop()
        self.next_scene = LoseAnimation(
            self, FadeToBlackBetween(self, LevelScreen(self.number))
        )


class FinalScene(LevelScreen):
    font = pygame.font.Font(ASSETS / "Pixeboy-font.ttf", 40)

    def __init__(self):
        super().__init__("Final")

        self.radius = 200
        self.frame_count = 0
        self.stars = [StarAnimation()["rotate"] for _ in range(27)]
        self.current_frames = [None] * 27

        self.found = sum(
            (
                [True] * user_data.stars_in(level, 0)
                + [False] * (3 - user_data.stars_in(level, 0))
                for level in range(9)
            ),
            [],
        )

    def show_on(self, screen: pygame.Surface):
        if self.frame_count < 150:
            super().show_on(screen)
            self.draw_stars(
                screen, 150 + 150 * math.cos(2 * math.pi * self.frame_count / 300)
            )

        elif self.frame_count < 225:
            FinalScene.handle_event = (
                lambda self, event: setattr(
                    self, "next_scene", FadeToBlackBetween(self, MenuScreen())
                )
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
                else None
            )
            # yes

            if all(self.found):
                self.draw_stars(
                    screen,
                    1500 * math.sin(2 * math.pi * (self.frame_count - 150) / 400),
                )
            else:
                text1 = self.font.render(
                    f"If only we had the other {self.found.count(False)} stars!",
                    False,
                    (246, 224, 200),
                )
                r = text1.get_rect()
                r.center = (350, 500)
                screen.blit(text1, r)

        elif all(self.found):
            image = pygame.Surface((700, 700))
            image.fill((246, 224, 200))
            col=(self.frame_count-225)*4+50
            if col<=255:
                image.set_alpha(col)
                screen.blit(image, (0, 0))
            else:
                self.next_scene = TitleScreen()
        else:
            self.next_scene = FadeToBlackBetween(self, MenuScreen())

        self.frame_count += 1

    def draw_stars(self, screen, radius):
        positions = [
            (
                350 - 8 + math.cos(math.pi * 2 / 27 * n) * radius,
                350 - 8 + math.sin(math.pi * 2 / 27 * n) * radius,
            )
            for n in range(-14, 14)
        ]
        if not self.frame_count % 3:
            self.current_frames = [*map(next, self.stars)]
        screen.blits(
            zip(
                [
                    (
                        (self.current_frames[i]).set_alpha(
                            255 if self.found[i] else 50
                        ),
                        self.current_frames[i],
                    )[1]
                    for i in range(27)
                ],
                positions,
            )
        )

class LoseAnimation(Transition):
    def show_on(self, screen: pygame.Surface):
        super().show_on(screen)
        if self.fraction_elapsed > 0.3:
            self.old.player.state = "dead"
        self.old.show_on(screen)


def manhattan_dist(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


class IntroScreen(Scene):
    x, y = (30, 48)
    duration = 600
    text = """Dear Commander Leto,

I hope this reaches you in time. We
have uncovered the source of the
rising galactic unrest - a version
of yourself from another dimension
is attempting to steal all of the
stars in our galaxy! We believe she
is harvesting their energy to save
her own dying universe.

Your mission is to stop her and
save all of the stars, but beware,
she will mirror your every move.

Yours truly,
The Prince of the Snailfish
"""
    parts = text.replace("\n\n", "\n<x>\n").split("<x>")

    def __init__(self):
        super().__init__()
        self.font = pygame.font.SysFont("monospace", 30)

        def render(text):
            return [
                self.font.render(line, True, (246, 224, 200))
                for line in text.splitlines()
            ]

        self.rendered_parts = list(
            itertools.accumulate([render(part) for part in self.parts])
        )
        image = pygame.display.get_surface().copy()
        image.fill((24, 33, 93))
        self.images = []
        for rendered_part in self.rendered_parts:
            im = image.copy()
            im.blits(
                [
                    (line, (self.x, self.y + i * 35))
                    for i, line in enumerate(rendered_part)
                ]
            )
            self.images.append(im)
        self.im_iter = iter(self.images)
        self.curr_im = next(self.im_iter)
        self.elapsed = 0

    def show_on(self, screen: pygame.Surface):
        screen.blit(self.curr_im, (0, 0))
        self.elapsed += 1

    def handle_event(self, event):
        if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN) or self.elapsed > 150:
            self.elapsed = 0
            try:
                self.curr_im = next(self.im_iter)
            except StopIteration:
                self.next_scene = SlideUpBetween(self, MenuScreen())


class FadeOver(Transition):
    """Might not work :)"""

    def __init__(self, old, new, duration=50):
        self.image = pygame.display.get_surface().copy()
        super().__init__(old, new, duration=duration)

    def show_on(self, screen: pygame.Surface):

        super().show_on(screen)
        self.old.show_on(screen)
        self.new.show_on(self.image)
        self.image.set_alpha(255 * (1 - self.fraction_elapsed))
        screen.blit(self.image, (0, 0))
