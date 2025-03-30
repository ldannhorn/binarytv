class Row:
    def __init__(self, width: int):
        self.width = width
        self.pixels: list[(int,int,int)] = [ (0,0,0) for _ in range(width)]
    
    def write(self, data: list[(int,int,int)]):
        self.pixels = data