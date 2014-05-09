import os, sys
import pygame
from pygame.locals import *

if not pygame.font: print 'Warning, fonts disabled'

# Constants
ROWS = 4

main_dir = os.path.split(os.path.abspath(__file__))[0]

def load_image(file):
    "loads an image, prepares it for play"
    file = os.path.join(main_dir, 'data', file)
    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s'%(file, pygame.get_error()))
    return surface.convert()

def load_images(*files):
    imgs = []
    for file in files:
        imgs.append(load_image(file))
    return imgs

class Board:
    def __init__(self):
        'Create a new empty Board'
        self.grid = []
        for x in range(0, ROWS):
            self.grid.append([0] * ROWS)
    
    def print_board(self):
        'Print the board to the console'
        for row in self.grid:
            print "\t".join((map(str,row)))
    
    def add_tile(self):
        'Add a tile to a random location on the board'
        #Find empty tiles
        self.grid[1] = [2,2,2,2]
        self.print_board()
        empties = []
        for row in range(0, ROWS):
            empties.append([i for i, x in enumerate(self.grid[row]) if x == 0])
        print empties
        new_tile_row = len(empties)


def main():
    pygame.init()
    screen = pygame.display.set_mode((400, 400))
    pygame.display.set_caption('2048')
    
    # Background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((255,255,255))
    
    screen.blit(background, (0,0))
    pygame.display.flip()
    
    tiles = Board();
    
    tiles.add_tile()
    #tiles.print_board()
    
    while 1:
        
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == MOUSEBUTTONDOWN:
                baa_sound.play()
                x, y = pygame.mouse.get_pos()
                chip.reset(x, y)
        
        
        screen.blit(background, (0,0))
        pygame.display.flip()

if __name__ == '__main__': main()