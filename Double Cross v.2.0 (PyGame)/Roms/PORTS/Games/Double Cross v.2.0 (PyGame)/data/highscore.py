"""Module: highscore.py
Overview:
    Module containing classes/functions for inputting and displaying highscores.
    NewHigh is the class used during the state TOP, and DisplayHigh is the class
    used during the state SCORING. Selector creates and animates our letter
    selecting cursor during the TOP state.
Global Constants:
    ALLDICT
    REVDICT
Functions:
    alphaprinter(string,alphagrid)
    make_dicts()
Classes:
    NewHigh(tools._State):
        Methods:
            __init__(self)
            check_score(self)
            save_score(self)
            make_image(self)
            blink_cursor(self,Surf)
            print_name(self,Surf)
            event_manager(self,event)
            engage(self)
            update(self,Surf)
    Selector:
        Methods:
            __init__(self)
            update(self,coord,direc,Surf)
    DisplayHigh(tools._State):
        Methods:
            __init__(self)
            prep(self)
            blinkit(self,Surf)
            event_manager(self,event)
            update(self,Surf)
            state_add_cleanup(self)"""
import pickle,os
import pygame as pg
from . import tools,reset
from . import setup as su

def make_dicts():
    """Create dictionaries for use with the alphaprinter."""
    grid = [(x,y) for y in range(6) for x in range(7)]
    characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890."+-'
    all_d = {(a,b):characters[i] for i,(a,b) in enumerate(grid[:40])}
    rev_d = {characters[i]:(a,b) for i,(a,b) in enumerate(grid[:40])}
    return all_d,rev_d

def alphaprinter(string,alphagrid):
    """Given a string and an alphagrid, return an image with the text."""
    highscore = pg.Surface((500,50)).convert_alpha()
    highscore.fill((0,0,0,0))
    for i,char in enumerate(string.upper()):
        if char != " ":
            a,b = REVDICT[char]
            highscore.blit(alphagrid,(50*i,0),(a*50,b*50,50,50))
    return highscore

#These dictionaries are coordinates on the grid paired with the character there.
ALLDICT,REVDICT = make_dicts()

class NewHigh(tools._State):
    def __init__(self):
        self.score,self.level = 0,0
        self.bg = su.GFXA["scorebg"]
        self.image = None
        self.sub = None
        self.done = False
        self.ready = False
        self.next = "SCORING"

        self.filename = os.path.join("data","highs.dat")
        self.data = None
        self.insert_here = None
        self.play_name = ""
        self.image = self.make_image()

        self.coord = [0,0]
        self.direc = None
        self.blink = False
        self.timer = 0.0
        self.Select = Selector()

    def check_score(self):
        try:
            with open(self.filename,'rb') as myfile:
                self.data = pickle.load(myfile)
        except (IOError,ValueError):
            self.data = reset.reset_scores(self.filename)
        for i,datum in enumerate(self.data):
            if self.score > datum[1]:
                self.insert_here = i
                break
            elif self.score == datum[1] and self.level > datum[2]:
                self.insert_here = i
                break
        self.ready = True

    def save_score(self):
        self.data.insert(self.insert_here,(self.play_name,self.score,self.level))
        self.data.pop()
        with open(self.filename,'wb') as myfile:
            pickle.dump(self.data,myfile)
        self.done = True

    def make_image(self):
        temp = pg.Surface((520,520)).convert_alpha()
        temp.blit(self.bg,(0,0))
        temp.blit(su.GFXA["alphagrid"],(85,160))
        temp.blit(su.FONTS["WADIM"].render("Very good Komrade",1,(255,0,0)),(120,10))
        temp.blit(su.FONTS["WADIM_S"].render("Submit your name for our records",1,(255,0,0)),(30,45))
        pg.draw.rect(temp,(255,255,255),(50,85,420,60),3)
        return temp

    def blink_cursor(self,Surf):
        if pg.time.get_ticks()-self.timer > 1000/7:
            self.blink = not self.blink
            self.timer = pg.time.get_ticks()
        if self.blink and len(self.play_name)<8:
            Surf.fill(su.COLORS["YELLOW"],(60+50*len(self.play_name),135,50,3))

    def print_name(self,Surf):
        name_img = alphaprinter(self.play_name,su.GFXA["alphagrid"])
        Surf.blit(name_img,(60,85))

    def event_manager(self,event):
        """Events for menus here. If a sub menu is active the event is passed
        down to that menu instead."""
        if not self.sub:
            if event.type == pg.KEYDOWN:
                if not self.direc:
                    if event.key == pg.K_DOWN:
                        self.coord[1],self.direc = (self.coord[1]+1)%6,"DOWN"
                    elif event.key == pg.K_UP:
                        self.coord[1],self.direc = (self.coord[1]-1)%6,"UP"
                    elif event.key == pg.K_RIGHT:
                        self.coord[0],self.direc = (self.coord[0]+1)%7,"RIGHT"
                    elif event.key == pg.K_LEFT:
                        self.coord[0],self.direc = (self.coord[0]-1)%7,"LEFT"
                if event.key in (pg.K_KP_ENTER,pg.K_RETURN):
                    self.engage()
        else:
            self.sub.event_manager(event)

    def engage(self):
        if tuple(self.coord) not in ((5,5),(6,5)): #Add letter to name.
            if len(self.play_name) < 8:
                self.play_name += ALLDICT[tuple(self.coord)]
        elif tuple(self.coord) == (5,5): #Backspace. Delete letter from name.
            if self.play_name:
                self.play_name = self.play_name[:-1]
        else:
            if self.play_name: #Confirm name. End button.
                self.save_score()

    def update(self,Surf):
        """Draw everything in its time in its place."""
        if not self.ready:
            self.check_score()
        if self.insert_here != None:
            if not self.sub:
                Surf.blit(self.image,(0,0))
                self.Select.update(self.coord,self.direc,Surf)
                self.blink_cursor(Surf)
                self.print_name(Surf)
                if not self.Select.anim:
                    self.direc = None
            else:
                self.state_submenu(Surf)
        else:
            self.done = True

class Selector:
    def __init__(self):
        self.image = su.GFXA["flipper_h"].subsurface((0,0,100,100))
        self.h_flips = [su.GFXA["flipper_h"].subsurface(( i*100,0,100,100)) for i in (1,2)]
        self.rect = pg.Rect(60,135,100,100)
        self.flip = None
        self.anim = False
        self.timer = 0.0
        self.frame = 0
    def update(self,coord,direc,Surf):
        next_rect = (60+coord[0]*50,135+coord[1]*50)
        if not self.anim and self.rect.topleft != next_rect:
            su.SFX["chimed"].play()
            self.anim = True
            self.timer = pg.time.get_ticks()
        if self.anim:
            if pg.time.get_ticks()-self.timer > 1000/10:
                self.frame+=1
                self.timer = pg.time.get_ticks()
            try:
                dirs={"RIGHT":self.h_flips[self.frame],
                      "LEFT":pg.transform.flip(self.h_flips[self.frame],1,0),
                      "DOWN":pg.transform.rotate(self.h_flips[self.frame],-90),
                      "UP"  :pg.transform.rotate(self.h_flips[self.frame],90)}
                if self.frame:
                    self.rect.topleft = next_rect
                Surf.blit(dirs[direc],self.rect)
            except IndexError:
                self.anim = False
                self.frame = 0
        if not self.anim:
            Surf.blit(self.image,self.rect)

class DisplayHigh(tools._State):
    """Displays the highscores and controls user events during that state."""
    def __init__(self):
        self.filename = os.path.join("data","highs.dat")
        self.bg = su.GFXA["scorebg"]
        self.message = su.GFXA["nekey"]
        self.msg_rect = self.message.get_rect(center=(260,502))
        self.ready = False
        self.image = None
        self.sub = None
        self.done = False
        self.next = "MENU"

        self.blink = False
        self.blink_timer = 0.0

    def prep(self):
        if not self.ready:
            try:
                with open(self.filename,'rb') as myfile:
                    self.ready = pickle.load(myfile)
            except (IOError,ValueError):
                self.ready = reset.reset_scores(self.filename)
            temp = pg.Surface(su.SCREENSIZE).convert()
            temp.blit(self.bg,(0,0))
            fields = '{:26}{}'.format('Score:','Level:')
            for i,(name,score,level) in enumerate(self.ready):
                colors = (su.COLORS["RED"],su.COLORS["WHITE"]) if i%2 else (su.COLORS["WHITE"],su.COLORS["RED"])
                info = '{:30}{}'.format(str(score).zfill(8), str(level).zfill(2))
                temp.blit(alphaprinter("{}.{}".format(i+1,name),su.GFXA["alphagrid"]),(20,i*100))
                temp.blit(su.FONTS["WADIM_IBIG"].render(fields,1,colors[0]),(50,50+i*100))
                temp.blit(su.FONTS["IMPACT"].render(info,1,colors[1]),(180,49+i*100))
            self.image = temp

    def blinkit(self,Surf):
        if pg.time.get_ticks()-self.blink_timer >= 250:
            self.blink = not self.blink
            self.blink_timer = pg.time.get_ticks()
        if self.blink:
            Surf.blit(self.message,self.msg_rect)

    def event_manager(self,event):
        """Press any key to continue."""
        if not self.sub:
            if event.type == pg.KEYDOWN:
                if event.key != pg.K_F5:
                    self.done = True
        else:
            self.sub.event_manager(event)

    def update(self,Surf):
        """Draw everything in its time in its place."""
        if not self.sub:
            self.prep()
            Surf.blit(self.image,(0,0))
            self.blinkit(Surf)
        else:
            self.state_submenu(Surf)

    def state_add_cleanup(self):
        self.ready = False