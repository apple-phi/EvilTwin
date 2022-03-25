import textwrap, toml
class Map:
    def __init__(self,filepath,ITEM_STR=(),default='-'):
        self.default = default
        self.filepath = filepath
        self.ITEM_STR = ITEM_STR
        self.array, self.items = self.load()

    def save(self):
        with open(self.filepath,"w") as f:
            f.write(textwrap.dedent(f"""\
            name = "Level 1"
            stars = {[[i-1,j-1] for i,j in self.stars]}
            start = {[self.player[0]-1,self.player[1]-1]}
            end = {[self.enemy[0]-1,self.enemy[1]-1]}
            map = '''
            """))
            f.write("\n".join([",".join(self.array[i]) for i in range(len(self.array))]))
            f.write("\n'''\n[items]\n"+"\n".join(f"{k} = {[[i-1,j-1] for i,j in v]}" for k,v in self.items.items()))
    def load(self):
        try:
            with open(self.filepath,"r") as f:
                data = toml.load(f)
                for k,v in data["items"].items():
                    data["items"][k] = [[i+1,j+1] for i,j in v]
                self.player = [data["start"][0]+1,data["start"][1]+1]
                self.enemy = [data["end"][0]+1,data["end"][1]+1]
                self.stars = [[i-1,j-1] for i,j in data["stars"]]
                return [j.strip().split(",") for j in data['map'].split()], data['items']
        except FileNotFoundError:
            print("generating new file")
            self.stars = []
            self.player, self.enemy = None, None
            return self.makeblank(10,10), {}
    def __getitem__(self,xy):
        (x,y) = xy
        return self.array[y-1][x-1]
    
    def __setitem__(self,xy,val):
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

