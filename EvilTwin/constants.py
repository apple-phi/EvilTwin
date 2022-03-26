import pathlib
import pygame

ASSETS = pathlib.Path(__file__).parent / "assets"
SOUNDS = pathlib.Path(__file__).parent / "Space Music Pack"
LEVELS = ASSETS / "levels"
TILES = ASSETS / "tiles"
SPRITES = ASSETS / "sprites"

TILE_SIZE = 16
STAR_FRACTION = 0.6
STAR_SPRITE = pygame.image.load(SPRITES / "star" / "basic.png")

STAR_OFFSET = (0.5 - STAR_FRACTION / 2 - 1 / 16) * TILE_SIZE
STAR_FRAME_DELAY = 5

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
065
066
067
068
069
070
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

ITEMS = [
    f"0{int(x)-1}"
    for x in """\
13
24 25 26
37 38 39
50
61 62 63 64 65
78
80 81 87
""".split()
]

WALLS += ITEMS