class Map:
    def __init__(self,filepath,default='-'):
        self.default = default
        self.filepath = filepath
        self.array = self.load()
    def save(self):
        with open(self.filepath,"w") as f:
            f.write("\n".join([" ".join(self.array[i]) for i in range(len(self.array))]))
    def load(self):
        try:
            with open(self.filepath,"r") as f:
                return [j.strip().split(" ") for j in f.readlines()]
        except FileNotFoundError:
            print("generating new file")
            return self.makeblank(10,10)
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

