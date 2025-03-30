import pygame
from threading import Thread
from random import randint
import io

from row import Row
from canvas import Canvas



def thread_pygame(canvas: Canvas):
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()
    pygame.display.set_caption("")
    running = True

    screen.fill((0, 0, 0))
    
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Render
        canvas.increment()
        frame = canvas.get_frame()

        #screen.fill((0, 0, 0))

        for y, row in enumerate(frame):
            for x, pixel in enumerate(row):
                pygame.draw.rect(screen, pixel, (x * 5, y * 5, 5, 5))


        # Update display
        pygame.display.flip()
        #clock.tick(300)


def thread_reader(canvas: Canvas, mode:str = "random", *args):

    if mode == "random":
        for _ in range(200):

            # Do not fill buffer too much
            #if canvas.get_buf_len() > 10 * canvas.get_frame_n_pixels():
            #    continue

            row = Row(canvas.width)
            row.write([ (randint(0,255), randint(0,255), randint(0,255)) for _ in range(canvas.width)])
            canvas.buf_add_row(row)
    
    elif mode == "playlist":
        canv_n_pixels = canvas.get_frame_n_pixels()

        playlist = args[0]

        fileobjs: list[io.BufferedReader] = []
        playlist_index = -1
        file_done = True
        file_pos = 0

        playing = True

        while playing:

            # Read new file whenever only 10 frames are loaded ahead
            if canvas.get_buf_len() > 10 * canv_n_pixels:
                continue
            
            if file_done:
                playlist_index += 1
                if playlist_index >= len(playlist):
                    # End of playlist
                    playing = False
                    break

                fileobjs.append( open(playlist[playlist_index], "rb") )
                
                file = fileobjs[-1]
                file_pos = file.tell()

                file_done = False


            # Read file
            file.seek(file_pos)
            try:
                data = file.read(canv_n_pixels * 20 * 3)
                if not data:  # End of file reached
                    file_done = True
                    continue
                file_pos = file.tell()
            except EOFError:
                # Read until the end of the file
                file.seek(file_pos)
                data = file.read()
                file_done = True

            
            data = bytearray(data)
            
            # Truncate data to be multiple of 3
            if not len(data) % 3 == 0:
                while len(data) % 3 != 0:
                    data.append(0)


            pixels: list[(int,int,int)] = []

            for i in range(0, len(data), 3):
                r = data[i]
                g = data[i + 1]
                b = data[i + 2]
                
                pixels.append((r, g, b))
            

            while True:
                try:
                    row = Row(canvas.width)
                    row.write(pixels[:canvas.width])
                    canvas.buf_add_row(row)
                    pixels = pixels[canvas.width:]
                except IndexError:
                    row = Row(canvas.width)
                    extra_pixels = canvas.width - len(pixels)
                    row.write(pixels + [(0,0,0) for _ in range(extra_pixels)])
                    canvas.buf_add_row(row)
                    continue
        
        print("End of playlist")
        for fileobj in fileobjs:
            fileobj.close()



        
        

if __name__ == "__main__":

    canvas = Canvas(100,100)

    # Start pygame thread
    pygame_thread = Thread(target=thread_pygame, args=[canvas])
    pygame_thread.start()

    # Start reader thread
    reader_thread = Thread(target=thread_reader, args=[canvas, "playlist", ["demo.png", "demo2.txt", "crash"]], daemon=True)
    reader_thread.start()



