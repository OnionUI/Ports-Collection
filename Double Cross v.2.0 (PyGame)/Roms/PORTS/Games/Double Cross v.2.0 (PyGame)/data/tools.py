"""Module: tools.py
Overview:
    Contains prototype classes to be inherited by other more specific classes.
    The Cursor class used in many different menus is also found here.
Classes:
    _State:
        Methods:
            state_submenu(self,Surf)
            state_subcleanup(self)
            state_cleanup(self)
            state_add_cleanup(self)
    _GenericMenu(_State):
        Methods:
            __init__(self,rect,font,accessed=False)
            setup(self)
            set_cursor(self,rect,size,speed=15)
            set_text(self,mycolor=su.COLORS["WHITE"])
            engage(self)
            heading(self)
            event_manager(self,event)
            update(self,Surf)
            state_subcleanup(self)
    Cursor:
        Methods:
            __init__(self,rect,size,speed)
            update(self,Surf)
            rand_color(self)"""
import pygame as pg
from random import randint
from . import setup as su

class _State:
    """All classes used at states must inherit from this Class.
       Where specifics are needed functions state_subcleanup and
       state_add_cleanup can be overloaded. Do not make instances
       of this class."""
    def state_submenu(self,Surf):
        self.sub.update(Surf)
        if self.sub.done:
            if self.sub.done == "QUIT":
                self.done = "QUIT"
                self.sub  = None
            else:
                self.sub.done = False
                self.sub = None
                self.state_subcleanup()
    def state_subcleanup(self):
        """Overload in specific state if additional submenu cleanup is needed."""
        pass
    def state_cleanup(self):
        """Cleanup if control moves to another State."""
        self.done = False
        self.state_add_cleanup()
    def state_add_cleanup(self):
        """Overload in specific state if additional cleanup needed."""
        pass

class _GenericMenu(_State):
    """This is an absract class to be inherited by other menus.  It supplies
    the basic functionality and initializations most often needed.  set_crusor
    and engage must be added to the specific inheriting class.
    Args: rect is the rectangle representing the menu.
    font is the font that the menu options will be rendered in.
    accessed defaults to False but can be used to pass miscelaneous information
    about the caller of the menu (or submenu)."""
    def __init__(self,rect,font,accessed=False):
        #Variables initialized from arguments.
        self.rect = pg.Rect(rect) #Topleft is where it will appear on the main screen.
        self.font = font
        self.accessed = accessed #Used to let a sub menu know info it needs.

        #Variables all menus need as starting values.
        self.ind  = 0         #option index
        self.bw_ind = []
        self.sub  = None      #is there a sub menu active?
        self.done = False     #are we finished here? (False/True/"QUIT")
        self.start_time = 0.0 #when did this menu last become active?
        self.image = pg.Surface(self.rect.size).convert()

        #Variables that differ between different types of menus.
        self.timeout  = False #False or the amount of seconds till timeout.
        self.vert     = True  #Vertical or horizontal menu?
        self.additionals = [] #Other things to draw.
        self.options     = [] #List of menu options.
        self.step  = (0,0)  #Distance between menu options.
        self.start = (0,0) #location of the center of the first option.

    def setup(self):
        """Draw the base menu and set up the cursor."""
        self.image.fill(0)
        for add in self.additionals:
            self.image.blit(*add)
        self.set_text()

    def set_cursor(self,rect,size,speed=15):
        """Set up the cursor.  Indiviudal types of menus must provide this function."""
        c_rect = pg.Rect(rect)
        c_rect.center = self.start
        self.curs = Cursor(c_rect,size,speed)

    def set_text(self,mycolor=su.COLORS["WHITE"]):
        """Render the options on the menu.  Often must be overloaded in individual menus."""
        for i,opt in enumerate(self.options):
            msg = self.font.render(opt,1,mycolor)
            msg_rect = msg.get_rect(center=(self.start[0]+self.step[0]*i,self.start[1]+self.step[1]*i))
            self.image.blit(msg,msg_rect)

    def engage(self):
        """Functionality for selecting menu options.
        Indiviudal types of menus must provide this function."""
        print("And now do something...")

    def heading(self):
        """If a heading is required this can be overloaded and called in self.additionals."""
        print("A heading?")

    def event_manager(self,event):
        """Events for menus here. If a sub menu is active the event is passed
        down to that menu instead."""
        que = None
        if not self.sub:
            if event.type == pg.KEYDOWN:
                if (self.vert and event.key == pg.K_DOWN) or (not self.vert and event.key == pg.K_RIGHT):
                    self.ind = (self.ind+1)%len(self.options)
                    su.SFX["blipshort1"].play()
                elif (self.vert and event.key == pg.K_UP) or (not self.vert and event.key == pg.K_LEFT):
                    self.ind = (self.ind-1)%len(self.options)
                    su.SFX["blipshort1"].play()
                elif event.key in (pg.K_KP_ENTER,pg.K_RETURN):
                    que = self.engage()
                self.curs.rect.topleft = (self.curs.start[0]+self.step[0]*self.ind,
                                          self.curs.start[1]+self.step[1]*self.ind)
                if self.timeout:
                    self.start_time = pg.time.get_ticks()
        else:
            self.sub.event_manager(event)
        return que

    def update(self,Surf):
        """Update the menu.  If a sub-menu is active update that instead."""
        if not self.sub:
            copy_img = self.image.copy()
            if self.ind in self.bw_ind:
                self.curs.update(copy_img,True)
            else:
                self.curs.update(copy_img)
            Surf.blit(copy_img,self.rect)
            if self.timeout and pg.time.get_ticks() - self.start_time > 1000*self.timeout:
                #currently only main menu times out (move later maybe)
                self.done = True
                self.next = "TITLE"
        else:
            self.state_submenu(Surf)

    def state_subcleanup(self):
        self.start_time = pg.time.get_ticks()

class Cursor:
    """Class for creating cursors in menus.
    Args: rect is a Rect with location relative to the menu and size of the cursor (x,y,xS,yS).
    size is the individual size of a border cell (x,y)
    speed is the rate at which border cells change color in frames/second."""
    def __init__(self,rect,size,speed):
        self.rect = pg.Rect(rect)
        self.size = size
        self.speed = speed
        self.start = self.rect.topleft
        self.timer = 0.0
        self.image = pg.Surface(self.rect.size).convert_alpha()

    def update(self,Surf,bw=False):
        """Check timer and update colors if required; then blit to given surface."""
        if pg.time.get_ticks() - self.timer > 1000.0/self.speed:
            self.image.fill((0,0,0,0))
            for sq_r in range(self.rect.width//self.size[0]):
                for num_r in (0,self.rect.height-self.size[1]):
                    self.image.fill(self.rand_color(bw),((sq_r*self.size[0],num_r),self.size))
                    shader = pg.transform.scale(su.GFXA["shade"],self.size)
                    self.image.blit(shader,(sq_r*self.size[0],num_r))
            for sq_c in range(self.rect.height//self.size[1]):
                for num_c in (0,self.rect.width-self.size[0]):
                    self.image.fill(self.rand_color(bw),((num_c,sq_c*self.size[1]),self.size))
                    shader = pg.transform.scale(su.GFXA["shade"],self.size)
                    self.image.blit(shader,(num_c,sq_c*self.size[1]))
            self.timer = pg.time.get_ticks()
        Surf.blit(self.image,self.rect)

    def rand_color(self,blackwhite):
        """Generate a random color."""
        if blackwhite:
            col = randint(0,255)
            return (col,)*3
        return [randint(0,255) for i in range(3)]

