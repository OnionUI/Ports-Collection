"""Module: blocks.py
Overview: Contains the class used to represent our blocks.
Classes:
    Block:
        Methods:
            __init__(self,ind,rot,vert,color)
            make_image(self)
            shift(self,direction)
            gravity(self)
            rotate(self)
            add2grid(self)
            update_grid(self)
Global Constants:
    BLOCKS"""

import pygame as pg
from . import setup as su

#These are the blocks represented by binary (written in dec to save space)
BLOCKS = (((0,0,0,15),(4,4,4,4 ),(0,0,0,15),(2,2,2,2 )),  #Stick
          ((0,0,6,6 ),(0,0,6,6 ),(0,0,6,6 ),(0,0,6,6 )),  #Block
          ((0,0,2,14),(0,4,4,6 ),(0,0,7,4 ),(0,6,2,2 )),  #True L-Block
    	  ((0,0,7,1 ),(0,2,2,6 ),(0,0,4,7 ),(0,6,4,4 )),  #Reverse L-Block
          ((0,0,6,12),(0,4,6,2 ),(0,0,3,6 ),(0,4,6,2 )),  #Z-Block
          ((0,0,12,6),(0,2,6,4 ),(0,0,6,3 ),(0,2,6,4 )),  #Z-Block
          ((0,0,2,7 ),(0,4,6,4 ),(0,0,7,2 ),(0,2,6,2 )))  #T-Block

class Block:
    """Class representing individual blocks."""
    def __init__(self,ind,rot,vert,color):
        self.vert = vert #True if a vertical drop, False if horizontal
        self.grid = None #Corresponding vertical or horizontal grid
        self.rot = rot #Rotation index
        self.ind = ind #Block type index
        self.type = BLOCKS[ind][rot] #Specific block including rotation
        self.color = color
        self.depth = 0   #How many cells "down" the current pit are we.
        self.lateral = 4 #Location with relation to the walls of the pit.
        self.rect  = pg.Rect(280,-60,80,80)
        self.done = False
        self.pix_per_frame = 2 #Changed to 4 during fast-drop.
        self.make_image()

    def make_image(self):
        """Create our block image by converting to binary and iterating over
           The block; blitting as dictated."""
        temp = pg.Surface((80,80)).convert_alpha()
        temp.fill((0,0,0,0))
        for i,x in enumerate(self.type):
            for j,y in enumerate(bin(x)[2:].zfill(4)):
                if y == '1':
                    #Flip indices for horizontal phase blocks
                    a,b = (i,j) if self.vert else (j,i)
                    temp.fill(self.color,(b*20,a*20,20,20))
                    temp.blit(su.GFXA["shade"],(b*20,a*20))
        self.image = temp

    def shift(self,direction):
        """Called when player presses a key for lateral motion within current pit."""
        binary_block = [int(i*2**(8-self.lateral-direction)) for i in self.type]
        if not any(a&b for a,b in zip(binary_block,self.grid[self.depth:])):
            self.lateral += direction
            self.rect.x += direction*20

    def gravity(self):
        """Serves as our "gravity" function within the current pit. Function is called
        by placing USEREVENTS on the event queue using pygame.time.set_timer. When the
        player holds the fast-drop key the time between function calls is decreased."""
        if self.rect.y%20==0:
            binary_block = [int(i*2**(8-self.lateral)) for i in self.type]
            if any(a&b for a,b in zip(binary_block,self.grid[self.depth+1:])):
                su.SFX["thud"].play()
                self.done = True
                self.add2grid()
                return 0
            else:
                self.depth += 1
        self.rect.y += self.pix_per_frame #Possible values include (1,2,4,5)
        return 1

    def rotate(self):
        """Rotates the object if clear.  Currently no wall kick implemented."""
        pg.key.set_repeat() #Turn repeat off while rotating.
        binary_block = [int(i*2**(8-self.lateral)) for i in BLOCKS[self.ind][(self.rot+1)%4]]
        if not any(a&b for a,b in zip(binary_block,self.grid[self.depth:])):
            su.SFX["blipshort1"].play()
            self.rot = (self.rot+1)%4
            self.type = BLOCKS[self.ind][self.rot]
            self.make_image()

    def add2grid(self):
        """Adds the object to its grid."""
        binary_block = [int(i*2**(8-self.lateral)) for i in self.type]
        for blockdepth,newcells in enumerate(binary_block):
            self.grid[self.depth+blockdepth] |= newcells

    def update_grid(self):
        """Finds any complete rows and deletes them from grid accordingly."""
        row2del = []
        for i,row in enumerate(self.grid):###
            if i < 4:
                self.grid[i] = 2049 #Clear the top 4 rows.###
            elif i != 24 and row == 4095:
                self.grid.pop(i) #Pop completed rows
                self.grid.insert(0,2049) #Insert an empty row at the top.
                row2del.append(i)
        return row2del