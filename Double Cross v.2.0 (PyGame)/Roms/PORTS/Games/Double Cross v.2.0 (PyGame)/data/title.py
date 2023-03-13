"""Module: title.py
Overview: Control flow for the game while in the TITLE state.
Classes:
    Title(tools._State):
        Methods:
            __init__(self)
            event_manager(self,event)
            get_image(self)
            update(self,Surf)"""
import pygame as pg
from . import menu,tools
from . import setup as su

class Title(tools._State):
    """Class for the title screen (the first State)."""
    def __init__(self):
        self.image,self.spin = su.GFXA["title1"],su.GFXA["title2"]
        self.timer = 0.0
        self.blink = False
        self.done = False
        self.next = None
        self.sub  = None
        self.start_time = 0.0
        self.redraw = False

    def event_manager(self,event):
        """Press any key to continue."""
        if not self.sub:
            if event.type == pg.KEYDOWN:
                if event.key != pg.K_F5:
                    self.done = True
                    self.next = "MENU"
        else:
            self.sub.event_manager(event)

    def get_image(self,Surf):
        """Create the screen image."""
        if pg.time.get_ticks()-self.timer >= 200:
            self.blink = not self.blink
            self.timer = pg.time.get_ticks()
        if self.blink:
            Surf.blit(self.spin,(0,0))

    def update(self,Surf):
        """Draw everything in its time in its place."""
        if not self.sub:
            Surf.blit(self.image,(0,0))
            self.get_image(Surf)
        else:
            self.state_submenu(Surf)