import textwrap, toml
class Map:
    def __init__(self,filepath,ITEM_STR=(),default='-'):
        self.default = default
        self.filepath = filepath
        self.ITEM_STR = ITEM_STR
        self.array, self.items = self.load()

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
            print(self.items)
            f.write("\n'''\n[items]\n"+"\n".join(f"{k} = {v}" for k,v in self.items.items()))
    def load(self):
        try:
            with open(self.filepath,"r") as f:
                data = toml.load(f)
                return [j.strip().split(",") for j in data['map'].split()], data['items']
        except FileNotFoundError:
            print("generating new file")
            return self.makeblank(10,10), {}
    def __getitem__(self,xy):
        (x,y) = xy
        return self.array[y-1][x-1]
    
    def __setitem__(self,xy,val):
        print(self.items,self.ITEM_STR,val)
        (x,y) = xy
        if val in self.ITEM_STR:
            q = self.items.setdefault(val, [])
            if [x,y] not in q:
                q.append([x,y])
        else:
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

