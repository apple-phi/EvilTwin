from LevelLoader import Map
import pygame
import pathlib
from collections import defaultdict

#from dataclasses import dataclass
#from typing import List
#@dataclass
#class Node:
#    x: int
#    y: int
#    connections: List[int]


filepath_1 = pathlib.Path(__file__).parent.absolute()/"maze.txt"

MAP = Map(filepath_1)
print(MAP)
nodes = defaultdict(list)
start_node = ()
end_node = ()

def find_furthest(y,x,direction):
    dy, dx = {0:(-1,0), 1:(0,1), 2:(1,0), 3:(0,-1)}[direction] # u r d l
    while MAP.array[y][x] == '-1':
        y+=dy
        x+=dx
    return y-dy,x-dx

for row_i, row in enumerate(MAP.array):
    for col_i, col in enumerate(row):
        if row_i == 0:
            if col ==  '-1':
                start_node = (row_i, col_i)
        elif row_i == len(MAP.array)-1:
            if col ==  '-1':
                end_node = (row_i, col_i)
        elif col == '-1':
            for dy,dx in ((-1,0), (0,1), (1,0), (0,-1)):
                #opt = find_furthest(row_i, col_i, direction)
                if MAP.array[row_i+dy][col_i+dx] == '-1':
                    nodes[(row_i, col_i)].append((row_i+dy,col_i+dx))
                    nodes[(row_i+dy,col_i+dx)].append((row_i, col_i))

print(nodes)

