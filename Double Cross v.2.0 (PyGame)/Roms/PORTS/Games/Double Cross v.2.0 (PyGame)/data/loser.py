"""Module: loser.py
Overview: Handles the animation that occurs right after a player loses.
Classes:
    Lose:
        Methods:
            __init__(self)
            lose_curtain(self,Surf)
            wall_gen(self,Surf)
            flash_text(self,Surf)
            update(self,phase,Surf)"""
import pygame as pg
from . import setup as su

class Lose:
    def __init__(self):
        self.curtain = pg.Surface((400,40)).convert_alpha()
        self.curtain.fill((0,0,0,0))
        self.brick = su.GFXA["brick"]
        self.image = pg.Surface((400,400)).convert_alpha()
        self.image.fill((0,0,0,0))
        self.fall = 0 #How far has the curtain fallen?
        self.timer = 0.0
        self.flash = True
        self.done = False
        self.nekey = False
        for i in range(20):
            self.curtain.blit(su.GFXA["curt"],(i*20,0))
        self.lose_wall = None

    def lose_curtain(self,Surf):
        if pg.time.get_ticks()-self.timer > 1000/50:
            self.image.blit(self.curtain,(0,self.fall-20))
            self.fall += 2
            if self.fall == 380:
                self.done = True
                self.nekey = True
            Surf.blit(self.image,(220,20),(200,0,200,400))
            Surf.blit(self.image,(20,220),(0,200,200,200))
            self.timer = pg.time.get_ticks()

    def wall_gen(self,Surf):
        """This function exploits yield generators in order to write this
           function using for loops. Other options include explicitly keeping
           track of indexes using class attributes and just using if statements;
           or completely cutting the function off from the main event loop while
           this function executes. Neither option appealed to me so I went with
           this method."""
        for w in range(11):
            for h in range(20,0,-1):
                while not pg.time.get_ticks()-self.timer > 1000/50:
                    yield "Waiting"
                r = not h%2
                if w<5:
                    if h>10:
                        continue
                    self.image.blit(self.brick,(20*r+w*40-20,180+h*20))
                else:
                    self.image.blit(self.brick,(20*r+w*40-20,h*20-20))
                Surf.blit(self.image,(220,20),(200,0,200,400))
                Surf.blit(self.image,(20,220),(0,200,200,200))
                self.timer = pg.time.get_ticks()
                yield "Next brick"

    def flash_text(self,Surf):
        if pg.time.get_ticks()-self.timer >= 200:
            self.flash = not self.flash
            self.timer = pg.time.get_ticks()
        if self.flash:
            Surf.blit(su.GFXA["nekey"],(99,351))
        else:
            Surf.blit(self.image,(220,20),(200,0,200,400))
            Surf.blit(self.image,(20,220),(0,200,200,200))
        Surf.blit(su.GFXA["komrade"],(-3,265))

    def update(self,phase,Surf):
        if self.done:
            self.flash_text(Surf)
        elif phase: #A lose from the vertical grid.
            self.lose_curtain(Surf)
        else: #A loss from the horizontal grid.
            if not self.lose_wall:
                self.lose_wall = self.wall_gen(Surf)
            try:
                next(self.lose_wall)
            except StopIteration:
                self.done = True
                self.nekey = True