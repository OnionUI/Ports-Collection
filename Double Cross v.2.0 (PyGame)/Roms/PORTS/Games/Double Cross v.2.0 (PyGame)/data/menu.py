"""Module: menu.py
Overview:
    Specific menu classes (derived from tools._GenericMenu) are defined in
    this module. The MainMenu class manages control flow in the MENU state.
    The MusicMenu is implemented as a submenu both during the MENU state and
    GAME state. The ExitMenu is a unique menu which can be used during any
    state of the game.
Classes:
    MainMenu(tools._GenericMenu):
        Methods:
            __init__(self,rect,font)
            set_text(self,mycolor=su.COLORS["WHITE"])
            engage(self)
    MusicMenu(tools._GenericMenu):
        Methods:
            __init__(self,rect,font,accessed)
            heading(self)
            set_text(self,mycolor=su.COLORS["WHITE"])
            engage(self)
    ExitMenu(tools._GenericMenu):
        Methods:
            __init__(self,rect,font,surf_copy)
            heading(self)
            engage(self)
            update(self,Surf)
            """
import os
import pygame as pg
from . import tools
from . import setup as su

class MainMenu(tools._GenericMenu):
    """This class is the main game menu."""
    def __init__(self,rect,font):
        tools._GenericMenu.__init__(self,rect,font)
        self.timeout = 15.0 #After 15 seconds with no events return to Title.
        self.options = ("1 Komrade Solo Drop","2 Komrade Death Drop",
                        "Controls","Music","Highscores")
        self.bw_ind = [1] #2 Player mode displays with black and white cursor.
        self.step  = (0,80)  #Distance between menu options.
        self.start = (self.rect.size[0]//2,138) #First option center.
        self.additionals = [(su.GFXA["strip"],(0,0)),(su.GFXA["strip"],(480,0)),
                            (su.GFXA["logo"],(80,5))]
        self.setup()
        self.set_cursor((0,0,360,80),(20,20))
        self.Musicer = MusicMenu(((0,0),su.SCREENSIZE),su.FONTS["WADIM_I"],"MENU")
        self.next = None
        self.redraw = False

    def set_text(self,mycolor=su.COLORS["WHITE"]):
        """Overloaded so that option names alternate red and white."""
        for i,opt in enumerate(self.options):
            msg = self.font.render(opt,1,(su.COLORS["RED"] if i%2 else mycolor))
            msg_rect = msg.get_rect(center=(self.start[0],self.start[1]+self.step[1]*i))
            self.image.blit(msg,msg_rect)

    def engage(self):
        opts = ["GAME","2-PLAYER","MAPPING","MUSIC","SCORING"]
        if opts[self.ind] in ["GAME","MAPPING","SCORING"]:
            self.next = opts[self.ind]
            self.done = True
        elif opts[self.ind] == "MUSIC":
            self.sub = self.Musicer
        else:
            pass #2-Player not implemented.

class MusicMenu(tools._GenericMenu):
    """Class used for the music select screen from the main menu and the pause screen."""
    def __init__(self,rect,font,accessed):
        tools._GenericMenu.__init__(self,rect,font,accessed)
        songs = os.listdir(os.path.join("sound","music"))
        mid = sorted([name[:-4] for name in songs if name[-3:] == "mp3"])
        if self.accessed == "MENU":
            self.options = (["Back"]+mid+["Off"] if mid else ["Back"])
        else:
            self.options = (["Resume"]+mid+["Off"] if mid else ["Resume"])
        self.step  = (0,80)  #distance between menu options
        self.start = (self.rect.size[0]//2,128) #Center of the first option
        if mid:
            self.additionals = [(su.GFXA["strip"],(0,0)),(su.GFXA["strip"],(480,0)),
                                (su.GFXA["donote"],(65,400)),self.heading()]
        self.setup()
        self.set_cursor((0,0,220,80),(20,20))

    def heading(self):
        surf = pg.Surface((102,45)).convert()
        pg.draw.rect(surf,su.COLORS["WHITE"],(0,0,102,45),3)
        if self.accessed == "MENU":
            text = su.FONTS["WADIM"].render("MUSIC",1,su.COLORS["WHITE"])
        else:
            text = su.FONTS["WADIM"].render("PAUSE",1,su.COLORS["WHITE"])
        txt_r = text.get_rect(center=surf.get_rect().center)
        surf.blit(text,txt_r)
        surf_r = surf.get_rect(center=(self.start[0],40))
        return surf,surf_r

    def set_text(self,color=su.COLORS["WHITE"]):
        for i,opt in enumerate(self.options):
            msg = self.font.render(opt,1,(su.COLORS["RED"] if not i else su.COLORS["WHITE"]))
            msg_rect = msg.get_rect(center=(self.start[0],self.start[1]+self.step[1]*i))
            self.image.blit(msg,msg_rect)
            if 0 < i < 4:
                self.image.blit(su.GFXA["note"],(95,90+self.step[1]*i))

    def event_manager(self,event):
        tools._GenericMenu.event_manager(self,event)
        if self.accessed != "MENU":
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                self.done = True

    def engage(self):
        if not self.ind:
            self.done = True
        elif 1 <= self.ind <= 3:
            pg.mixer.music.stop()
            song = self.options[self.ind]+".mp3"
            volumes = [0.8,1,0.7]
            su.play_song(song,volumes[self.ind-1])
        elif self.ind == 4:
            pg.mixer.music.stop()

class ExitMenu(tools._GenericMenu):
    """Exit menu used in all parts of the game."""
    def __init__(self,rect,font,surf_copy):
        tools._GenericMenu.__init__(self,rect,font)
        self.accessed = surf_copy
        self.vert = False
        self.options = ("YES","NO")
        self.ind = 1 #default to 'NO' to be polite
        self.step  = (81,0)  #distance between menu options
        self.start = (64,71) #location of the center of the first option
        self.additionals = [self.heading()]
        self.setup()
        self.set_cursor((0,0,80,50),(10,10))
        self.curs.rect.center = (self.start[0]+self.step[0]*self.ind,
                                 self.start[1]+self.step[1]*self.ind)
        pg.draw.rect(self.image,su.COLORS["BLUE"],(4,4,200,100),10)

    def heading(self):
        surf = su.FONTS["WADIM"].render("EXIT",1,su.COLORS["RED"])
        surf_r = surf.get_rect(center=(self.rect.size[0]//2,30))
        return surf,surf_r

    def engage(self):
        self.done = True if self.ind else "QUIT"

    def update(self,Surf):
        Surf.blit(self.accessed,(0,0))
        tools._GenericMenu.update(self,Surf)
