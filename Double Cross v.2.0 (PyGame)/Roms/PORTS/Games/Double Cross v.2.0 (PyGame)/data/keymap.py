"""Module: keymap.py
Overview:
    Control flow for key customization during the MAPPING state.
Classes:
    KeyMapping(tools._State):
        Methods:
            __init__(self,controls)
            set_cursor(self,y=0)
            event_manager(self,event)
            mod_keys(self,event)
            save_keys(self)
            blinkit(self,Surf)
            paint_keys(self)
            update(self,Surf)
            state_subcleanup(self)
            state_add_cleanup(self)
    KeyMenu(tools._GenericMenu):
        heading(self)
        engage(self)"""
import pickle,os
import pygame as pg
from . import tools
from . import setup as su

class KeyMapping(tools._State):
    def __init__(self,controls):
        self.play_ctrl = controls
        self.filename = os.path.join("data","playcontrols.dat")

        self.ind  = [0,0]
        self.done = False
        self.start_time = 0.0

        self.blink = False
        self.blink_timer = 0.0
        self.image = su.GFXA["controls"].copy()
        self.message = su.GFXA["nekey"]
        self.msg_rect = self.message.get_rect(center=(260,260))

        self.mod_which = 1 #Modify 1-Player controls or 2-Player controls
        self.Menu = KeyMenu((146,109,228,309),su.FONTS["WADIM"])
        self.sub = self.Menu
        self.state = None
        self.next = "MENU"

        self.start = (80,55)
        self.step  = (120,120)
        self.set_cursor()
        self.new_keys = ([],[])
        self.redraw = False

    def set_cursor(self,y=0):
        c_rect = pg.Rect((0,0,100,50))
        c_rect.center = self.start[0],self.start[1]+y
        self.curs = tools.Cursor(c_rect,(5,5),15)

    def event_manager(self,event):
        if self.state:
            if self.state == "VIEW":
                if event.type == pg.KEYDOWN and event.key != pg.K_F5:
                    self.done = True
            elif self.state in ("SET1","SET2"):
                self.mod_keys(event)
        elif self.sub:
            self.state = self.sub.event_manager(event)
            if self.state == "SET1":
                self.set_cursor()
            elif self.state == "SET2":
                self.set_cursor(270)

    def mod_keys(self,event):
        if event.type == pg.KEYDOWN and event.key not in (pg.K_F5,pg.K_ESCAPE):
            if event.key not in self.new_keys[self.ind[1]]:
                self.new_keys[self.ind[1]].append(event.key)
                if self.ind[0] < 3:
                    self.ind[0] += 1
                elif self.ind[1] < 1:
                    self.ind = [0,1]
                else:
                    self.ind = [0,0]
                    self.save_keys()
                    self.state = "VIEW"
                self.curs.rect.topleft = (self.curs.start[0]+self.step[0]*self.ind[0],
                                          self.curs.start[1]+self.step[1]*self.ind[1])

    def save_keys(self):
        if self.state == "SET1":
            keys = (self.new_keys,self.play_ctrl[1])
        elif self.state == "SET2":
            keys = (self.play_ctrl[0],self.new_keys)
        elif self.state == "RESET":
            keys = (su.PLAYER1_DEFAULT,su.PLAYER2_DEFAULT)
        self.play_ctrl = keys
        with open(self.filename,'wb') as myfile:
            pickle.dump(keys,myfile)
        self.new_keys = ([],[])

    def blinkit(self,Surf):
        if pg.time.get_ticks()-self.blink_timer >= 250:
            self.blink = not self.blink
            self.blink_timer = pg.time.get_ticks()
        if self.blink:
            Surf.blit(self.message,self.msg_rect)

    def paint_keys(self):
        for i in range(2):
            for j in range(4):
                for k,ctrl in enumerate(self.play_ctrl):
                    self.image.fill(su.COLORS["WHITE"],(51+j*120,91+i*120+270*k,58,16))
                    key = ctrl[i][j]
                    if (not k and self.state == "SET1") or (k and self.state == "SET2"):
                        try:
                            key = self.new_keys[i][j]
                        except IndexError:
                            pass
                    msg = su.FONTS["ARIAL"].render(pg.key.name(key).upper(),1,su.COLORS["BLACK"])
                    if msg.get_rect().width > 54:
                        msg = pg.transform.smoothscale(msg,(54,19))
                    msg_rect = msg.get_rect(center=(80+j*120,99+i*120+k*270))
                    self.image.blit(msg,msg_rect)

    def update(self,Surf):
        self.paint_keys()
        Surf.blit(self.image,(0,0))
        if self.state:
            if self.state == "VIEW":
                self.blinkit(Surf)
            elif self.state in ("SET1","SET2"):
                self.curs.update(Surf)
            elif self.state == "RESET":
                self.save_keys()
                self.state = "VIEW"
        elif self.sub:
            self.state_submenu(Surf)

    def state_subcleanup(self):
        self.done = True
        self.start_time = pg.time.get_ticks()

    def state_add_cleanup(self):
        self.state = None
        self.sub = self.Menu

class KeyMenu(tools._GenericMenu):
    def __init__(self,rect,font):
        tools._GenericMenu.__init__(self,rect,font)
        self.options = ("Back","Default","Custom 1P","Custom 2P","View")
        self.step  = (0,50)
        self.start = (self.rect.size[0]//2,70)
        self.additionals = [self.heading()]
        self.setup()
        self.set_cursor((0,0,180,50),(10,10))
        pg.draw.rect(self.image,su.COLORS["BLUE"],(4,4,219,300),10)

    def heading(self):
        surf = su.FONTS["WADIM"].render("Controls",1,su.COLORS["RED"])
        surf_r = surf.get_rect(center=(self.rect.size[0]//2,30))
        return surf,surf_r

    def engage(self):
        opts = [None,"RESET","SET1","SET2","VIEW"]
        if not self.ind:
            self.done = True
        que = opts[self.ind]
        self.ind = 0
        return que