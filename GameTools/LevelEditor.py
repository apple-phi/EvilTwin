import itertools
from LevelLoader import Map

import pygame
import pathlib

import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / "EvilTwin"))
# dont worry about it, it just works
TILES, WALLS, ITEMS = "", ..., []
exec("from constants import TILES,WALLS,ITEMS")  # so linter doesnt cry
TILENUM = 104


class Game:
    def __init__(self):
        self.path = pathlib.Path(__file__).parent
        self.cellsize = 64

        filepath = (self.path.parent / "EvilTwin/assets/levels/1.toml").absolute()
        self.load_map(filepath)

        self.prevpressed = False
        self.mode = "Paintbrush"
        self.stored = WALLS[0]

        self.to_change = []
        self.rect_selection = []

        self.screen = pygame.display.set_mode(
            (self.actual_width * self.cellsize, (self.y + 9) * self.cellsize)
        )

        self.pallete = {
            f"{n:03d}": pygame.image.load(TILES / f"{n:03d}.png")
            for n in range(TILENUM)
        }
        self.tools = {
            1: "Brush",
            2: "R_Sel",
            3: "Remove Items",
            4: "Player",
            5: "Enemy",
            6: "Star",
            7: "Switch",
            8: "Play",
            self.actual_width - 1: "Load_from",
            self.actual_width: "Save_to",
        }
        self.cols = {(n % 13 + 1, n // 13 + 1): f"{n:03d}" for n in range(TILENUM)}
        pygame.init()

        self.blit_all()

    def blit_tile(self, x, y):
        tile = self.Map[x, y]
        cs = self.cellsize
        drawpos = ((x - 1) * cs, (y - 1) * cs, cs, cs)
        # pygame.draw.rect(self.screen,self.pallete[tile],drawpos)
        # self.print_txt(tile,x,y)
        self.screen.blit(pygame.transform.scale(self.pallete[tile], (64, 64)), drawpos)

        for k, v in self.Map.items.items():
            if [x, y] in v:
                self.screen.blit(
                    pygame.transform.scale(self.pallete[k], (64, 64)), drawpos
                )

    def blitmap(self):
        for x, y in self.to_change:
            self.blit_tile(x, y)
        self.to_change = []
        image = pygame.Surface((10, 10))
        image.fill([255, 255, 0])
        for x, y in self.Map.stars:
            self.screen.blit(
                image,
                (self.cellsize * (x - 1), self.cellsize * (y - 1)),
            )

        image = pygame.Surface((10, 10))
        for col, obj in zip(([255,0,0],[0,255,0],[0,0,255]),(self.Map.enemy,self.Map.player,self.Map.switch)):
            image.fill(col)
            if obj:
                self.screen.blit(
                    image,
                    (
                        self.cellsize * (obj[0] - 1),
                        self.cellsize * (obj[1] - 1),
                    ),
                )

        pygame.display.flip()

    def CheckEvents(self):
        pygame.event.get()
        pressed1, pressed2, _ = pygame.mouse.get_pressed()
        pos = pygame.mouse.get_pos()
        coord = self.get_coords(pos)
        if pressed2 and coord[1] <= self.y and coord[0] <= self.x:
            self.stored = self.Map[coord]
            if self.mode not in ("Paintbrush", "Rect_select"):
                self.mode = "Paintbrush"
        if pressed1:
            self.handle_pressed(coord)
        else:
            if self.prevpressed and self.mode == "R_Sel":
                if coord[1] <= self.y and coord[0] <= self.x:
                    for x, y in itertools.product(
                        range(
                            min(coord[0], self.rect_selection[0]),
                            max(coord[0], self.rect_selection[0]) + 1,
                        ),
                        range(
                            min(coord[1], self.rect_selection[1]),
                            max(coord[1], self.rect_selection[1]) + 1,
                        ),
                    ):
                        self.Map[x, y] = self.stored
                        self.to_change.append([x, y])
                self.rect_selection = []
            self.prevpressed = False

    def get_coords(self, pos):
        return [pos[0] // self.cellsize + 1, pos[1] // self.cellsize + 1]

    def print_txt(self, tile, x, y):
        cs = self.cellsize
        font = pygame.font.Font("freesansbold.ttf", 20)
        if tile in self.pallete.keys():
            text = font.render(tile, True, (0, 0, 0), self.pallete[tile])
        else:
            font = pygame.font.Font("freesansbold.ttf", 12)
            text = font.render(tile, True, (255, 255, 255), (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (int((x - 0.5) * cs), int((y - 0.5) * cs))
        self.screen.blit(text, textRect)

    def load_map(self, filepath):
        self.Map = Map(filepath, ITEMS, WALLS[0])
        # self.Map.makeblank(50,10)
        self.x, self.y = self.Map.dimensions()
        self.actual_width = max(self.x, 13)
        self.screen = pygame.display.set_mode(
            (self.actual_width * self.cellsize, (self.y + 9) * self.cellsize)
        )

    def blit_all(self):
        for x, y in itertools.product(range(1, self.actual_width + 1), range(1, 9)):
            cs = self.cellsize
            drawpos = ((x - 1) * cs, (self.y - 1 + y) * cs, cs, cs)
            self.screen.blit(
                pygame.transform.scale(self.pallete[self.cols[(x, y)]], (64, 64)),
                drawpos,
            )

        for x in range(1, self.actual_width + 1):  # bottom bit: tool menu
            if x in self.tools:
                self.print_txt(self.tools[x], x, self.y + 9)
        for x, y in itertools.product(range(1, self.x + 1), range(1, self.y + 1)):
            self.blit_tile(x, y)

    def handle_pressed(self, coord):
        if coord[1] == (self.y + 9) and not self.prevpressed:
            self.handle_toolbar(coord)

        elif self.y < coord[1] < self.y + 9:
            coord = coord[0], coord[1] - self.y
            if coord in self.cols:
                self.stored = self.cols[coord]
                if self.mode not in ("Paintbrush", "Rect_select"):
                    self.mode = "Paintbrush"

        elif coord[1] <= self.y and coord[0] <= self.x:
            self.handle_draw(coord)

        self.prevpressed = True

    def handle_toolbar(self, coord):
        self.rect_selection = []
        if coord[0] in self.tools:
            if coord[0] == 8:
                import subprocess

                subprocess.Popen(["py", "-m", "EvilTwin"])
            elif coord[0] == self.actual_width - 1:
                self.load_map(
                    (
                        self.path.parent
                        / f"EvilTwin/assets/levels/{input('ENTER FILE NAME: ')}.toml"
                    ).absolute()
                )
                self.blit_all()
            elif coord[0] == self.actual_width:
                print("SAVING FILE")
                self.Map.save()
            else:
                self.mode = self.tools[coord[0]]

    def handle_draw(self, coord):
        if self.mode == "Paintbrush":
            self.Map[coord] = self.stored
            self.to_change.append(coord)
        elif self.mode == "Items":
            self.remove_items(coord)
        elif self.mode in "Player Enemy Switch".split():
            if p := getattr(self.Map, self.mode.lower()):
                self.to_change.append(p)
            setattr(self.Map, self.mode.lower(), list(coord))
        elif self.mode == "Star":
            if list(coord) not in self.Map.stars:
                self.Map.stars.append(list(coord))

        elif self.mode == "R_Sel":
            if not self.rect_selection and not self.prevpressed:
                self.rect_selection = coord
                drawpos = (
                    (coord[0] - 0.6) * self.cellsize,
                    (coord[1] - 1) * self.cellsize,
                    int(self.cellsize / 5),
                    int(self.cellsize / 5),
                )
                pygame.draw.rect(self.screen, (0, 255, 0), drawpos)

    def remove_items(self, coord):
        coord = list(coord)
        for v in self.Map.items.values():
            if coord in v:
                v.remove(coord)
        if coord in self.Map.stars:
            self.Map.stars.remove(coord)
        if coord == self.Map.player:
            self.Map.player = None
        if coord == self.Map.enemy:
            self.Map.enemy = None
        if coord == self.Map.switch:
            self.Map.switch = None
        self.to_change.append(coord)


g = Game()

while True:
    g.CheckEvents()
    g.blitmap()
