import pygame

class Row:
    def __init__(self, width: int):
        self.width = width
        self.pixels: list[(int,int,int)] = [ (0,0,0) for _ in range(width)]
    
    def write(self, data: list[(int,int,int)]):
        self.pixels = data



class Canvas:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

        self.row_buffer: list[Row] = []

        self.frame: list[list[(int,int,int)]]
        self.frame = [ [(0,0,0) for _ in range(width)] for _ in range(height) ]
    
    def buf_add_row(self, row: Row):
        self.row_buffer.append(row)
    
    def increment(self):
        # Pop first row
        self.frame.pop(0)

        # Add new row to the end of the frame
        self.frame.append(self.row_buffer.pop(0).pixels)
    
    def get_frame(self) -> list[list[(int,int,int)]]:
        '''Return the frame. Unset rows will be black.'''

        # Height ok
        if len(self.frame) >= self.height:
            return self.frame
        
        # Height too small
        else:
            while len(self.frame) < self.height:
                self.frame.append([(0,0,0) for _ in range(self.width)])
            return self.frame
        
        
        

if __name__ == "__main__":
    canvas = Canvas(16,10)

    from random import randint
    for i in range(10):
        row = Row(canvas.width)
        row.write([ (randint(0,255), randint(0,255), randint(0,255)) for _ in range(canvas.width)])
        canvas.buf_add_row(row)

    for i in range(10):
        canvas.increment()
        print(canvas.get_frame())







    

class Reader:
    def __init__(self, canvas: Canvas):
        self.canvas = canvas

        self.playlist: list[str] = []

    def add_playlist(self, playlist:list[str]):
        self.playlist.extend(playlist)

    