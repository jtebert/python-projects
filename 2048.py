import os, sys
import pygame
from pygame.locals import *
import random

if not pygame.font:
    raise ValueError('Fonts disabled. Need fonts to play this game.')

# Constants
ROWS = 4 # Number of rows in the grid
SZ = 50  # Drawing size (pixels) of the board
num_val = 5
change_color = [0. + x*(255.-0.)/num_val for x in range(num_val)]
blues = map(lambda c: (c, c, 255), change_color)
greens = map(lambda c: (c, 255, c), change_color)
reds = map(lambda c: (255, c, c), change_color)
colors = blues + greens + reds
vals = [2**(x+1) for x in range(num_val*3)]
COLOR_DICT = dict(zip(vals, colors))
ARROWS = [K_LEFT, K_RIGHT, K_UP, K_DOWN]

main_dir = os.path.split(os.path.abspath(__file__))[0]

def load_image(file):
    '''loads an image, prepares it for play'''
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

class Board(object):
    def __init__(self):
        '''Create a new empty Board'''
        self.grid = Board.empty_grid()
    
    @staticmethod        
    def empty_grid():
        '''Create an empty grid'''
        grid = []
        for x in range(ROWS):
            grid.append([0] * ROWS)
        return grid
    
    def print_board(self):
        'Print the board to the console'
        for row in self.grid:
            print "\t".join((map(str,row)))
    
    def add_tile(self):
        '''Add a tile to a random location on the board'''
        empties = self.free_cells()
        # TODO: How to handle if board is full
        new_tile_loc = random.choice(empties)
        rand_vals = [2]*3 + [4]
        new_tile_val = random.choice(rand_vals)
        self.grid[new_tile_loc[0]][new_tile_loc[1]] = new_tile_val
        
    def free_cells(self):
        '''Return a list of tuples of the empty spaces on the board'''
        empties = []
        for row in range(ROWS):
            empty_cols = [i for i, x in enumerate(self.grid[row]) if x == 0]
            empties.extend(map(lambda c: (row, c), empty_cols))
        return empties
        
    def is_full(self):
        '''Return whether or not every cell on the board is filled'''
        return len(self.free_cells()) == 0
        
    def draw_tiles(self, bg):
        '''Draw all of the tiles/values in the grid'''
        for row in range(ROWS):
            for col in range(ROWS):
                self.draw_tile(row, col, bg)
                
    def rotate(self):
        '''Rotate the grid (swap rows and columns)'''
        new_grid = Board.empty_grid()
        for row_ind in range(ROWS):
            for col_ind in range(ROWS):
                new_grid[col_ind][row_ind] = self.grid[row_ind][col_ind]
        self.grid = new_grid
    
    def draw_tile(self, row, col, bg):
        '''Draw the tile with the given coordinates onto the background'''
        # Create the image of the tile
        val = self.grid[row][col]
        if val:
            tile = pygame.Surface((SZ, SZ))
            tile.fill(COLOR_DICT[val])
            font = pygame.font.Font(None, 36)
            text = font.render(str(val), 1, (0,0,0))
            textpos = text.get_rect()
            textpos.center = tile.get_rect().center
            tile.blit(text, textpos)
            pygame.draw.rect(tile, (255,255,255), tile.get_rect(), 2)
            # Place tile at the correct coordinates
            bg.blit(tile, (col*SZ, row*SZ))
            
    def shift_right(self):
        '''Shift the tiles to the right and do any merging'''
        old_tiles = self.grid
        self.grid = map(lambda r: r[::-1], self.grid)
        self.shift_left()
        self.grid = map(lambda r: r[::-1], self.grid)
        return old_tiles
        
    def shift_down(self):
        '''Shift the tiles down and do any merging'''
        old_tiles = self.grid
        self.rotate()
        self.shift_right()
        self.rotate()
        return old_tiles
        
    def shift_up(self):
        '''Shift the tiles up and do any merging'''
        old_tiles = self.grid
        self.rotate()
        self.shift_left()
        self.rotate()
        return old_tiles
            
    def shift_left(self):
        '''Shift the tiles to the left and do any merging'''
        old_tiles = self.grid
        new_grid = []
        for row in self.grid:
            # shift everything to the right
            row = self.shift_row_left(row)
            # merge once (looking from right side)
            row = self.merge_row_left(row)
            # shift right again
            row = self.shift_row_left(row)
            new_grid.append(row)
        self.grid = new_grid
        return old_tiles
    
    def shift_row_left(self, row):
        '''Shift a row to the left (all zeros end up on the right)'''
        # Find indices of zeros
        els = filter(lambda e: e != 0, row)
        new_row = els + [0]*(ROWS - len(els))
        return new_row
        
    def merge_row_left(self, row):
        '''Merge the first two matching elements on the left'''
        merged = False
        for col_ind in range(ROWS-1):
            if merged == False and row[col_ind] == row[col_ind + 1] and row[col_ind] != 0:
                merged = True
                row[col_ind] = row[col_ind] + row[col_ind + 1]
                row[col_ind + 1] = 0
        return row
    
    def highest_tile(self):
        '''Return the value of the highest tile in the board'''
        return max(max(self.grid))

def main():
    pygame.init()
    screen = pygame.display.set_mode((SZ*ROWS, SZ*ROWS))
    pygame.display.set_caption('2048')
    
    # Background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((255,255,255))
    
    screen.blit(background, (0,0))
    pygame.display.flip()
    
    tiles = Board();
    
    tiles.add_tile()
    tiles.add_tile()
    
    game_over = False
    game_won = False
    
    while not game_over:
        
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == MOUSEBUTTONDOWN:
                tiles.add_tile()
            elif event.type == KEYDOWN:
                if event.key == K_LEFT:
                    old_tiles = tiles.shift_left()
                if event.key == K_RIGHT:
                    old_tiles = tiles.shift_right()
                if event.key == K_DOWN:
                    old_tiles = tiles.shift_down()
                if event.key == K_UP:
                    old_tiles = tiles.shift_up()
                # Check for changes to game state
                if old_tiles != tiles.grid and event.key in ARROWS:
                    tiles.add_tile()
                if tiles.is_full() and old_tiles == tiles.grid:
                    game_over = True
        if tiles.highest_tile >= 2048:
            game_won = True
        
        screen.blit(background, (0,0))
        tiles.draw_tiles(screen)
        pygame.display.flip()

if __name__ == '__main__': main()
