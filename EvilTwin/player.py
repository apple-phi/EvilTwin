import numpy as np
from tilemap import Tile

class Player:
    def __init__(self, map, coords):
        self.map = map
        self.xy = coords
        self.dest = self.src

        self.is_moving = False
        self.dir = (0, 0)
    
    def path(self, xy):
        """
        Chooses the player's destination in the x and/or y direction based on a vector
        ranging from [-1,-1] to [1,1]
        """
        mov = self.xy

        # While the current tile dest is blank, move along by 1
        # This is a while True which gets broken as soon as a wall is met. 
        while self.map[mov[1] + xy[1], mov[0] + xy[0]] != Tile.WALL:
            mov = (mov[0] + xy[0], mov[1] + xy[1])

        
        self.dest = mov

        # If the end result causes movement, set movement flag to true, set direction. 
        if self.dest != self.xy:
            self.is_moving = True
            self.dir = xy
        
        # Otherwise, set direction to null. 
        else:
            self.dir = (0, 0)
    

    def move(self):
        """
        Actually moves the player along in the current direction of movement. 
        """

        # If currently moving
        if self.is_moving:
            trial_dest = (self.xy[0] + self.dir[0], self.xy[1] + self.dir[1])

            # If have reached a wall, stop moving
            if self.map[trial_dest[1], trial_dest[0]] == Tile.WALL:
                self.dir = (0, 0)
                self.is_moving = False
        
            # Else, move
            else:
                self.xy = trial_dest

    def __repr__(self):
        return f"Player - Current: {self.xy}, Dest: {self.dest}, Dir: {self.dir}, moving: {self.is_moving}"

class Enemy(Player):
    def path(self,xy):
        return super().path(-xy[0],-xy[1])