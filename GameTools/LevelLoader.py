import textwrap
class Map:
    def __init__(self,filepath,default='-'):
        self.default = default
        self.filepath = filepath
        self.array = self.load()
    def save(self):
        with open(self.filepath,"w") as f:
            f.write(textwrap.dedent("""\
            name = "Level 1"
            stars = [[2, 3], [2, 1], [3, 2]]
            start = [1, 1]
            end = [3, 3]
            map = '''
            """))
            f.write("\n".join([",".join(self.array[i]) for i in range(len(self.array))]))
            f.write("\n'''")
    def load(self):
        try:
            with open(self.filepath,"r") as f:
                return [j.strip().split(",") for j in f.readlines()[5:-1]]
        except FileNotFoundError:
            print("generating new file")
            return self.makeblank(50,10)
    def __getitem__(self,xy):
        (x,y) = xy
        return self.array[y-1][x-1]
    
    def __setitem__(self,xy,val):
        (x,y) = xy
        self.array[y-1][x-1] = val
    
    def __delitem__(self,xy):
        (x,y) = xy
        self.array[y-1][x-1] = self.default
    
    def __str__(self):
        return str(self.array)
    
    def makeblank(self,x,y):
        self.array = [[self.default for _ in range(x)] for _ in range(y)]
        return self.array

    def dimensions(self):
        return [len(self.array[0]),len(self.array)]

