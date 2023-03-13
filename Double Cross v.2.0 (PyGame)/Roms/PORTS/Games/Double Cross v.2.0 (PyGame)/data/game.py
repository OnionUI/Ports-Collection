"""Module: game.py
Overview:
    Game logic and control flow for the game while in the GAME state.
    The class Game manages the core of the game. The class _Draw_Mixin
    contains the draw functions that class Game uses; pulled out for better
    organization.
Classes:
    _Draw_Mixin:
        Methods:
            draw_setup(self,Surf)
            draw_playfield(self,Surf)
            draw_next(self,Surf)
            draw_prefield(self,Surf)
            draw_bluelines(self,Surf)
            draw_current(self,Surf)
            draw_delete_rows(self,Surf)
            draw_stats(self,Surf)
    Game(tools._State,_Draw_Mixin):
        Methods:
            __init__(self,controls)
            event_manager(self,event)
            drop_it(self)
            stop_drop(self)
            go2music_menu(self)
            update(self,Surf)
            playing(self,Surf)
            get_next(self,Surf)
            get_new_grids(self)
            transpose(self,grid)
            adjust_score(self,Surf)
            get_colors(self,rgb)"""
import random
import pygame as pg
from . import blocks,menu,loser,tools
from . import setup as su

class _Draw_Mixin:
    """Draw functions for Game class.  Pulled out for organization's sake.
       Inherited by Game; do not create instances of this class."""
    def draw_setup(self,Surf):
        pg.key.set_repeat(50,50)
        Surf.blit(self.bg,(0,0))
        self.draw_next(Surf)
        self.draw_playfield(Surf)
        self.draw_stats(Surf)
        self.last_screen = Surf.copy()
        self.image = self.last_screen.copy()
    def draw_playfield(self,Surf):
        """Generates the playing field."""
        Surf.fill(su.COLORS["YELLOW"],(219,19,202,402))
        Surf.fill(su.COLORS["BLACK"],(220,20,200,400))
        Surf.fill(su.COLORS["YELLOW"],(19,219,201,202))
        Surf.fill(su.COLORS["BLACK"],(20,220,400,200))
        self.draw_bluelines(Surf)
    def draw_next(self,Surf):
        """Update the preview fields."""
        self.draw_prefield(Surf)
        Surf.blit(self.NextBlocks[1].image,(136,40,80,80))
        Surf.blit(self.NextBlocks[0].image,(40,136,80,80))
    def draw_prefield(self,Surf):
        """Resets preview boxes."""
        Surf.fill(su.COLORS["YELLOW"],(135,39,82,82))
        Surf.fill(su.COLORS["BLACK"],(136,40,80,80))
        Surf.fill(su.COLORS["YELLOW"],(39,135,82,82))
        Surf.fill(su.COLORS["BLACK"],(40,136,80,80))
    def draw_bluelines(self,Surf):
        """Draws the blue grid lines in the shared grid."""
        for i in range(10):
            Surf.fill(su.COLORS["BLUE"],(220,219+i*20,200,1))
            Surf.fill(su.COLORS["BLUE"],(219+i*20,220,1,200))
        if self.vert:
            Surf.fill(su.COLORS["RED"],(220,219,200,1))
        else:
            Surf.fill(su.COLORS["RED"],(219,220,1,200))
    def draw_current(self,Surf):
        """Draws the currently falling block."""
        if self.Current:
            if self.vert:
                loc   = self.Current.rect.topleft
                erase = pg.Rect((self.Current.rect.x-20,self.Current.rect.y-5,120,85))
            else:
                loc = self.Current.rect.topleft[::-1]
                erase = pg.Rect((self.Current.rect.y-5,self.Current.rect.x-20,85,120))
            Surf.blit(self.last_screen,erase,erase)
            Surf.blit(self.Current.image,loc)
        self.draw_next(Surf)
    def draw_delete_rows(self,Surf):
        """If there are pending deletions, this function will update the changes.
        This function is a little messy, but functional (I think)."""
        if not self.del_temp:
            self.del_temp = Surf.copy()
        if  pg.time.get_ticks() - self.del_timer > 1000/7:
            self.del_ind += 1
            self.del_timer = pg.time.get_ticks()
        loc = (200,400),(220,20),(0,20),(200,20)
        if not self.vert:
            loc = tuple(i[::-1] for i in loc)
        temp = pg.Surface(loc[0]).convert()
        temp.blit(self.del_temp,(0,0),(loc[1],loc[0]))
        for pend in self.pending:
            if self.vert:
                if self.del_ind in (0,1):
                    temp.blit(self.del_frames[self.del_ind],(0,20*(pend-4)))
                elif self.del_ind == 2:
                    temp.fill((0),(0,20*(pend-4),200,20))
            else:
                if self.del_ind in (0,1):
                    temp.blit(pg.transform.rotate(self.del_frames[self.del_ind],90),(20*(pend-4),0))
                elif self.del_ind == 2:
                    temp.fill((0),(20*(pend-4),0,20,200))
            if self.del_ind == 3:
                get = (200,20*(pend-4)) if self.vert else (20*(pend-4),200)
                temp.blit(self.del_temp,loc[2],(loc[1],get))
                temp.fill((0),((0,0),loc[3]))
                su.SFX["line"].play()
                self.del_temp.blit(temp,loc[1])
        if self.del_ind != 3:
            Surf.blit(temp,loc[1])
        else:
            self.del_ind = 0
            Surf.blit(self.del_temp,(0,0))
            self.adjust_score(Surf)
            self.pending = []
            self.del_temp = None
        self.draw_bluelines(Surf)
    def draw_stats(self,Surf):
        Surf.fill(su.COLORS["YELLOW"],(9,439,502,47)); Surf.fill(su.COLORS["BLACK"],(10,440,500,45))
        stats = "SCORE: {:<16}Level: {:3}".format(str(self.score).zfill(8),self.level)
        Surf.blit(su.FONTS["WADIM"].render(stats,1,su.COLORS["WHITE"]),(22,443))

class Game(tools._State,_Draw_Mixin):
    def __init__(self,controls):
        self.done = False
        self.next = "TOP"
        self.sub = None
        self.Musicer = menu.MusicMenu(((0,0),su.SCREENSIZE),su.FONTS["WADIM_I"],"PAUSE")
        self.start = False
        self.lose  = False
        self.Lost  = loser.Lose() #Class for lose animation.
        self.controls = controls

        self.bg = su.GFXA["base"]
        self.vert = False
        self.score = 0; self.level = 1; self.linecount = 0
        self.speed = 50 #Speed implemented using pygame.time.set_timer
        self.fast_drop = False

        self.rgb = -1
        self.color = self.get_colors()
        self.pending = [] #Rows pending deletion.
        self.redraw = True
        self.del_ind = -1
        self.del_timer = 0.0
        self.del_frames = [su.GFXA["cell_deletion1"],su.GFXA["cell_deletion2"]]
        self.del_temp = None

        #Empty grid. Displayed as such for visual purposes.
        empty_grid = ([int('0b100000000001',2)]*24 #An empty row.   [dec 2049]
                     +[int('0b111111111111',2)])   #The bottom row. [dec 4095]
        self.grids = [empty_grid[:],empty_grid[:]] #One for horz, one for vert.

        self.last_screen = None
        v_ind,h_ind = random.randint(0,6),random.randint(0,6)
        self.NextBlocks = [blocks.Block(h_ind,random.randint(0,3),False,self.color[h_ind]),
                           blocks.Block(v_ind,random.randint(0,3), True,self.color[v_ind])]
        self.Current = None

    def event_manager(self,event):
        """Press any key to continue."""
        if not self.sub:
            i = not self.vert
            if event.type == pg.USEREVENT and self.start:
                if self.Current and not self.Current.gravity():
                    self.Current.done = True
            if event.type == pg.KEYDOWN:
                if event.key != pg.K_F5:
                    if not self.Lost.nekey:
                        if not self.start:
                            self.start = True
                        if self.Current:
                            if event.key == self.controls[0][i][0]:
                                self.Current.shift(-1+2*i)
                            elif event.key == self.controls[0][i][1]:
                                self.Current.shift(1-2*i)
                            elif event.key == self.controls[0][i][2]:
                                self.Current.rotate()
                            elif event.key == self.controls[0][i][3]:
                                self.drop_it()
                            elif event.key == pg.K_SPACE: #Pause with P
                                self.go2music_menu()
                    else:
                        self.done = True
                        pg.key.set_repeat(200,100)
            elif event.type == pg.KEYUP:
                if event.key == self.controls[0][i][3]:
                    self.stop_drop()
                elif event.key == self.controls[0][i][2]:
                    pg.key.set_repeat(50,50)
        else:
            self.sub.event_manager(event)

    def drop_it(self):  #Enable fast drop
        if not self.fast_drop:
            if self.Current:
                if not self.Current.rect.y%4:
                    self.Current.pix_per_frame = 4
                    self.fast_drop = True
                pg.time.set_timer(pg.USEREVENT,10)
    def stop_drop(self): #Disable fast drop
        self.fast_drop = False
        if self.Current:
            self.Current.pix_per_frame = 2
        pg.time.set_timer(pg.USEREVENT,self.speed)
    def go2music_menu(self): #Change to music menu
        self.sub = self.Musicer
        self.redraw = True
        pg.key.set_repeat()

    def update(self,Surf):
        """Draw everything in its time in its place."""
        if not self.sub:
            if not self.start and self.redraw:
                self.draw_setup(Surf)
                self.redraw = False
            elif self.redraw: #Erase exit menu
                Surf.blit(self.image,(0,0))
                self.redraw = False
                pg.key.set_repeat(50,50)
            if self.start and not self.lose:
                self.playing(Surf)
            elif self.lose:
                self.Lost.update(self.vert,Surf)
                self.image = Surf.copy()
        else:
            self.state_submenu(Surf)

    def playing(self,Surf):
        """Controls updates once blocks have started falling."""
        self.get_next(Surf)
        self.draw_current(Surf)
        Surf.blit(self.last_screen,(220,0),(220,0,200,20))
        Surf.blit(self.last_screen,(0,220),(0,220,20,200))
        self.image = Surf.copy()
        if self.Current and self.Current.done:
            if not self.Current.depth:
                self.lose = True
                self.Current = None
                su.SFX["explosion"].play()
                return 0
            self.pending = self.Current.update_grid()
            self.Current = None

    def get_next(self,Surf):
        """As soon as a block begins to drop, create the next block."""
        if not self.Current:
            if self.pending:
                self.draw_delete_rows(Surf)
            else:
                self.draw_bluelines(Surf)
                self.last_screen = Surf.copy()
                self.get_new_grids()
                self.vert = not self.vert
                self.Current = self.NextBlocks[self.vert]
                self.Current.grid = self.grids[self.vert]
                ind,rot = random.randint(0,6),random.randint(0,3)
                self.NextBlocks[self.vert] = blocks.Block(ind,rot,self.vert,self.color[ind])
                self.draw_next(Surf)
                self.fast_drop = False
                pg.time.set_timer(pg.USEREVENT,self.speed)
                pg.key.set_repeat(50,50)

    def get_new_grids(self):
        """Updates a grid with changes corresponding to the other grid."""
        a = not self.vert
        self.grids[a] = self.grids[a][:14]+self.transpose(self.grids[not a])
    def transpose(self,grid):
        """Accepts a 25 line grid and returns the transpose of the bottom 11 lines."""
        grid2bin = [bin(r)[2:] for r in grid[13:]] #Convert each row to binary.
        trans = ["".join(digit) for digit in zip(*grid2bin)][1:] #Transpose.
        for i,ele in enumerate(trans): #Build side wall.
            trans[i]=ele.replace(ele[0],"0b1",1)
        return [int(ele,2) for ele in trans] #Convert back to dec and return.

    def adjust_score(self,Surf):
        """Called whenever a line deletion occurs to update score and level."""
        self.score += 100*len(self.pending)**2
        self.linecount += len(self.pending)
        if self.linecount >= 10:
            self.level += 1; self.linecount = 0
            self.speed = max(self.speed-5,1)
            su.SFX["lev"].play()
            self.color = self.get_colors()
        self.draw_stats(Surf)

    def get_colors(self):
        """Generates a list that contains seven random colors for each type of block.
           Function is recalled every time a player levels up."""
        inds = [0,1,2]
        opts = [(0,255),(0,255),(0,255)]
        if self.rgb != -1:
            inds.pop(self.rgb)
        self.rgb = random.choice(inds)
        opts[self.rgb] = (200,255)
        return [[random.randint(*opts[i]) for i in range(3)] for x in range(7)]
