from LevelLoader import Map
import pygame
from GStats import Stats
import pathlib

class Game():
    def __init__(self):
        self.path = str(pathlib.Path(__file__).parent.absolute())
        
        #filepath = self.path + "/GameStuff/ARRAY.txt"
        filepath = self.path + "/maze.txt"

        self.GS = Stats()
        self.Map = Map(filepath,"-1")
        #self.Map.makeblank(40,30)
        self.GS.x,self.GS.y = self.Map.dimensions()        

        
        self.prevpressed = False
        self.mode = "Brush"
        self.stored = "-1"

        self.to_change = []
        self.rect_selection = []

        self.screen = pygame.display.set_mode((self.GS.x*self.GS.cellsize, (self.GS.y+1)*self.GS.cellsize))

        

        floortile_1 = pygame.image.load(self.path +  "/GameStuff/tiles/floor/floor_1.png")
        floortile_2 = pygame.image.load(self.path +  "/GameStuff/tiles/floor/floor_2.png")
        floortile_3 = pygame.image.load(self.path +  "/GameStuff/tiles/floor/floor_3.png")
        floortile_4 = pygame.image.load(self.path +  "/GameStuff/tiles/floor/floor_4.png")


        walltile_1 = pygame.image.load(self.path +  "/GameStuff/tiles/wall/wall_1.png")
        walltile_2 = pygame.image.load(self.path +  "/GameStuff/tiles/wall/wall_2.png")
        walltile_3 = pygame.image.load(self.path +  "/GameStuff/tiles/wall/wall_3.png")

        self.pallete = {"-1":floortile_1,"-2":floortile_2,"-3":floortile_3,"-4":floortile_4, "@1":walltile_1,"@2":walltile_2,"@3":walltile_3,}

        tools = {1:"Brush",2:"R_Sel",self.GS.x:"Save"}
        self.cols = {3:"@1",4:"@2",5:"@3",6:"-1",7:"-2",8:"-3",9:"-4",}

        pygame.init()

        for x in range(1,self.GS.x+1): #bottom bit: tool menu
            if x in tools.keys():
                self.print_txt(tools[x],x,self.GS.y+1)
            elif x in self.cols.keys():
                cs = self.GS.cellsize
                drawpos = ((x-1)*cs, (self.GS.y)*cs, cs, cs)
                self.screen.blit(pygame.transform.scale(self.pallete[self.cols[x]],(64,64)),drawpos)
        
        for x in range(1,self.GS.x+1): 
            for y in range(1,self.GS.y+1):
                self.blit_tile(x,y)


    def blit_tile(self,x,y):
        tile = self.Map[x,y]
        cs = self.GS.cellsize
        drawpos = ((x-1)*cs, (y-1)*cs, cs, cs)
        #pygame.draw.rect(self.screen,self.pallete[tile],drawpos)
        #self.print_txt(tile,x,y)

        self.screen.blit(pygame.transform.scale(self.pallete[tile],(64,64)),drawpos)


    def blitmap(self):
        for x,y in self.to_change:
            self.blit_tile(x,y)
        self.to_change = []
        
        pygame.display.flip()

    def CheckEvents(self):
        for event in pygame.event.get(): #check events, keys pointless but we need the checks so why not
            dirdict = {275:1,276:3,273:0,274:2}
            if event.type == pygame.KEYDOWN:
                if event.key in dirdict.keys():
                    self.player_dir = dirdict[event.key]
        
        pressed1, pressed2, pressed3 = pygame.mouse.get_pressed()
        pos = pygame.mouse.get_pos()
        coord = self.get_coords(pos)
        if pressed2: #middleclick for colour
            if coord[1] <= self.GS.y:
                self.stored = self.Map[coord]
        if pressed1:
            if coord[1] == (self.GS.y+1) and not self.prevpressed:
                if coord[0]==2:
                    self.mode = "Rect_select"
                else:
                    self.rect_selection = []
                    if coord[0]==1:
                        self.mode = "Paintbrush"
                    elif coord[0]==self.GS.x:
                        print("SAVING FILE")
                        self.Map.save()
                    elif coord[0] in self.cols.keys():
                        self.stored = self.cols[coord[0]]
                        print(self.stored)
                    
                
            else:
                if coord[1] <= self.GS.y:
                    if self.mode == "Paintbrush":
                        self.Map[coord] = self.stored
                        self.to_change.append(coord)
                    elif self.mode == "Rect_select":
                        if len(self.rect_selection) == 0 and not self.prevpressed:
                            self.rect_selection = coord
                            cs = self.GS.cellsize
                            drawpos = ((coord[0]-0.6)*cs, (coord[1]-1)*cs, int(cs/5), int(cs/5)) #little green indicator
                            pygame.draw.rect(self.screen,(0,255,0),drawpos)

                        
  
            self.prevpressed = True
        else:
            if self.prevpressed and self.mode == "Rect_select":
                if coord[1]<=self.GS.y:
                    for x in range(min(coord[0],self.rect_selection[0]),max(coord[0],self.rect_selection[0])+1):
                        for y in range(min(coord[1],self.rect_selection[1]),max(coord[1],self.rect_selection[1])+1):
                            self.Map[x,y] = self.stored
                            self.to_change.append([x,y])
                self.rect_selection = []
            self.prevpressed = False


    

    def get_coords(self,pos): return [pos[0]//self.GS.cellsize+1,pos[1]//self.GS.cellsize+1]

    def print_txt(self,tile,x,y):
        cs = self.GS.cellsize
        font = pygame.font.Font('freesansbold.ttf', 20)
        if tile in self.pallete.keys(): 
            text = font.render(tile, True, (0,0,0),self.pallete[tile])
        else:
            font = pygame.font.Font('freesansbold.ttf', 12)
            text = font.render(tile, True, (255,255,255),(0,0,0))
        textRect = text.get_rect()
        textRect.center = (int((x-0.5)*cs), int((y-0.5)*cs))
        self.screen.blit(text, textRect)

g = Game()

while True:
    g.CheckEvents()
    g.blitmap()

