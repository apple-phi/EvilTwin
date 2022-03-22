import itertools
from LevelLoader import Map
import pygame
from GStats import Stats
import pathlib

filepath_1 = pathlib.Path(__file__).parent.absolute()/"GameStuff/ARRAY.txt"


class Game():
    def __init__(self):
        self.GS = Stats()  # import some of the important stuff like the images
        # transfer names for ease of use
        self.knight_run, self.knight_idle, self.pallete = self.GS.knight_run, self.GS.knight_idle, self.GS.pallete

        # Map arguments are the file and default state of a tile if we delete it. Map supports replace, delete and create but the methods dont change the size of the map
        self.Map_1 = Map(filepath_1, "-1")
        self.GS.x, self.GS.y = self.Map_1.dimensions()

        self.player_dir = -1
        self.look_dir = 1
        self.player_pos = [1, 1]
        # states used in drawing the correct frame for player
        self.running, self.idle = 0, 0

        self.clock = pygame.time.Clock()  # needed for time tick after
        self.screen = pygame.display.set_mode(
            (self.GS.x*self.GS.cellsize, (self.GS.y+1)*self.GS.cellsize))

        for x, y in itertools.product(range(1, self.GS.x+1), range(1, self.GS.y+1)):
            self.blit_tile(x, y)
        pygame.display.flip()

    def blit_tile(self, x, y):
        """
        Draws a tile on the screen

        Args:
            x (int): The x coordinate of the tile to be drawn, coords start from 1 not 0.
            y (int): The y coordinate of the tile to be drawn, coords start from 1 not 0.
        """

        tile = self.Map_1[x, y]
        cs = self.GS.cellsize
        drawpos = ((x-1)*cs, (y-1)*cs, cs, cs)
        # all images scaled to the tile size
        self.screen.blit(pygame.transform.scale(
            self.pallete[tile], (self.GS.cellsize, self.GS.cellsize)), drawpos)

    def blit_player(self):
        """Draws the player at its current coords"""
        cs = self.GS.cellsize
        # adjust drawing position with 1,1 coords system
        drawpos = ((self.player_pos[0]-1)*cs, (self.player_pos[1]-1)*cs)
        if self.running:
            img = self.knight_run[(self.running-1) % len(self.knight_run)]
        else:
            img = self.knight_idle[(self.idle-1) % len(self.knight_idle)]
        # flips sideways if we are moving left
        img = pygame.transform.flip(img, self.look_dir, False)
        self.screen.blit(pygame.transform.scale(
            img, (self.GS.cellsize, self.GS.cellsize)), drawpos)

    def CheckEvents(self):
        """Checks all user input, and updates the screen"""
        for event in pygame.event.get():
            # the big numbers are python codes for the arrow keys, linked to the direction they result in (N,E,S,W as 0,1,2,3)
            dirdict = {pygame.K_UP: 0, pygame.K_RIGHT: 1,
                       pygame.K_DOWN: 2, pygame.K_LEFT: 3}
            if event.type == pygame.KEYDOWN:
                if event.key in dirdict:
                    self.player_dir = dirdict[event.key]
                    if dirdict[event.key] in [1, 3]:
                        # gets the knight boi looking around properly by means of flip
                        self.look_dir = dirdict[event.key] == 3
                    if not self.running:  # start the running frames, stop the idle ones
                        self.running, self.idle = 1, 0
            elif event.type == pygame.KEYUP:
                if event.key in dirdict and dirdict[event.key] == self.player_dir:
                    self.player_dir, self.running, self.idle = \
                        -1, 0, 1  # dir set to special -1 so we dont move
        if self.running:
            self.running += 1
        elif self.idle:
            self.idle += 1

        pygame.display.flip()

    def MovePlayer(self):
        """Deals with legal player movement"""
        self.blit_tile(
            *self.player_pos)  # cover image of previous knight by redrawing the tile
        if self.player_dir != -1:
            movedict = {0: [0, -1], 1: [1, 0], 2: [0, 1], 3: [-1, 0]}
            next_pos = [self.player_pos[i]+movedict[self.player_dir][i]
                        for i in range(2)]  # next player position hypothetically
            next_pos = [min(max(next_pos[0], 1), self.GS.x), min(
                max(next_pos[1], 1), self.GS.y)]  # clamp value in the bounds
            if "@" not in self.Map_1[next_pos]:  # @ signifies a solid block
                self.player_pos = next_pos
        self.blit_player()


g = Game()
while True:  # gameloop
    g.CheckEvents()
    g.MovePlayer()
    g.clock.tick(10)
