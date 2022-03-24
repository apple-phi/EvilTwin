import pathlib
import pygame

ASSETS = pathlib.Path(__file__).parent / "assets"
LEVELS = ASSETS / "levels"
TILES = ASSETS / "tiles"
SPRITES = ASSETS / "sprites"

TILE_SIZE = 16
STAR_FRACTION = 0.5
STAR_SPRITE = pygame.transform.scale(
    pygame.image.load(SPRITES / "star.png"),
    (TILE_SIZE * STAR_FRACTION, TILE_SIZE * STAR_FRACTION),
)
STAR_OFFSET = (0.5 - STAR_FRACTION / 2 - 1 / 16) * TILE_SIZE


WALLS = """
000
001
002
003
006
007
008
009
010
011
013
014
015
016
017
018
026
029
030
031
039
040
041
042
043
044
052
053
054
056
057
058
059
066
067
068
069
071
072
073
074
078
083
091
100
101
102
103
""".split()
