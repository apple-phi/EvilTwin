import pathlib
class Stats():
    def __init__(self):
        import pygame
        self.x,self.y = 5,5
        self.cellsize = 64

        self.path = str(pathlib.Path(__file__).parent.absolute())

        floortile_1 = pygame.image.load(self.path +  "/GameStuff/tiles/floor/floor_1.png")
        floortile_2 = pygame.image.load(self.path +  "/GameStuff/tiles/floor/floor_2.png")
        floortile_3 = pygame.image.load(self.path +  "/GameStuff/tiles/floor/floor_3.png")
        floortile_4 = pygame.image.load(self.path +  "/GameStuff/tiles/floor/floor_4.png")
        walltile_1 = pygame.image.load(self.path +  "/GameStuff/tiles/wall/wall_1.png")
        walltile_2 = pygame.image.load(self.path +  "/GameStuff/tiles/wall/wall_2.png")
        walltile_3 = pygame.image.load(self.path +  "/GameStuff/tiles/wall/wall_3.png")
        
        knight_run_1 = pygame.image.load(self.path +  "/GameStuff/heroes/knight/knight_run_anim_f0.png")
        knight_run_2 = pygame.image.load(self.path +  "/GameStuff/heroes/knight/knight_run_anim_f1.png")
        knight_run_3 = pygame.image.load(self.path +  "/GameStuff/heroes/knight/knight_run_anim_f2.png")
        knight_run_4 = pygame.image.load(self.path +  "/GameStuff/heroes/knight/knight_run_anim_f3.png")
        knight_run_5 = pygame.image.load(self.path +  "/GameStuff/heroes/knight/knight_run_anim_f4.png")
        knight_run_6 = pygame.image.load(self.path +  "/GameStuff/heroes/knight/knight_run_anim_f5.png")

        knight_idle_1 = pygame.image.load(self.path +  "/GameStuff/heroes/knight/knight_idle_anim_f0.png")
        knight_idle_2 = pygame.image.load(self.path +  "/GameStuff/heroes/knight/knight_idle_anim_f1.png")
        knight_idle_3 = pygame.image.load(self.path +  "/GameStuff/heroes/knight/knight_idle_anim_f2.png")
        knight_idle_4 = pygame.image.load(self.path +  "/GameStuff/heroes/knight/knight_idle_anim_f3.png")
        knight_idle_5 = pygame.image.load(self.path +  "/GameStuff/heroes/knight/knight_idle_anim_f4.png")
        knight_idle_6 = pygame.image.load(self.path +  "/GameStuff/heroes/knight/knight_idle_anim_f5.png")
        
        self.knight_run = [knight_run_1,knight_run_2,knight_run_3,knight_run_4,knight_run_5,knight_run_6,]
        self.knight_idle = [knight_idle_1,knight_idle_2,knight_idle_3,knight_idle_4,knight_idle_5,knight_idle_6,] #TEMP
        self.pallete = {"-1":floortile_1,"-2":floortile_2,"-3":floortile_3,"-4":floortile_4, "@1":walltile_1,"@2":walltile_2,"@3":walltile_3,}