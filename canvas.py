from row import Row
from queue import Queue

class Canvas:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

        self.row_buffer: Queue[Row] = Queue()

        self.frame: list[list[(int,int,int)]]
        self.frame = [ [(0,0,0) for _ in range(width)] for _ in range(height) ]
    
    def buf_add_row(self, row: Row):
        self.row_buffer.put_nowait(row)
    
    def increment(self):
        # Pop first row
        self.frame.pop(0)

        # Add new row from buf to the end of the frame
        try:
            self.frame.append(self.row_buffer.get_nowait().pixels)
        except Exception as e:
            # If no row in buffer, append black row
            print(f"Canvas: {e}")
            self.frame.append([(0,0,0) for _ in range(self.width)])
        #self.frame.append(self.row_buffer.get().pixels)

    
    def get_frame(self) -> list[list[(int,int,int)]]:
        '''Return the frame. Unset rows will be black.'''
        
        # If height too small
        if len(self.frame) < self.height:
            while len(self.frame) < self.height:
                self.frame.append([(0,0,0) for _ in range(self.width)])
        
        return self.frame

    def get_buf_len(self) -> int:
        return self.row_buffer.qsize()
    
    def get_frame_n_pixels(self) -> int:
        return self.width * self.height