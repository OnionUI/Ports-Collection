"""Module: main.py
Overview: Primary control flow for entire game.
Classes:
    Control:
        Methods:
            __init__(self)
            get_controls(self)
            control_events(self)
            lowest_image(self,Menu)
            reset(self)
            update(self,Surf)
            main(self)"""
import os,sys  #used for os.environ and sys.exit
import pickle
import pygame as pg

from . import title,menu,keymap,highscore,game
from . import setup as su

class Control:
    """The flow of the entire game is governed from this class."""
    def __init__(self):
        self.fps = 200
        self.showfps = False #Is the fps visible in the window title bar?
        self.myclock = pg.time.Clock() #A clock to restrict the framerate.

        #Load control presets if any, else set to default controls
        self.filename = os.path.join("data","playcontrols.dat")
        self.game_controls = self.get_controls()

        #Classes that Control will use as States.
        self.Titler = title.Title()
        self.Menuer = menu.MainMenu(((0,0),su.SCREENSIZE),su.FONTS["WADIM_I"])
        self.Mapper = keymap.KeyMapping(self.game_controls)
        self.Scorer = highscore.DisplayHigh()
        self.Higher = highscore.NewHigh()
        self.Gamer  = game.Game(self.game_controls)
        self.Exit = None

        #Previous State-classes arranged in a dictionary.
        self.state_dict = {"TITLE"  : self.Titler,
                           "MENU"   : self.Menuer,
                           "MAPPING": self.Mapper,
                           "SCORING": self.Scorer,
                           "TOP"    : self.Higher,
                           "GAME"   : self.Gamer}

        #Start game in the TITLE State.
        self.State = self.state_dict["TITLE"]

        pg.key.set_repeat()
        pg.time.set_timer(pg.USEREVENT,50)

    def get_controls(self):
        """If custom controls have been saved, retrieve them."""
        try:
            with open(self.filename,'rb') as myfile:
                data = pickle.load(myfile)
        except (IOError,ValueError):
            data = su.PLAYER1_DEFAULT,su.PLAYER2_DEFAULT
        return data

    def control_events(self):
        """Primary event loop. Events are passed to States as needed."""
        if self.State != "QUIT":
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_F5:
                        self.showfps = not self.showfps
                    elif event.key == pg.K_ESCAPE:
                        if not self.Exit:
                            if self.State != self.state_dict["MAPPING"]:
                                image = self.lowest_image(self.State)
                            else:
                                image = self.State.image
                            self.Exit = menu.ExitMenu((155,154,209,109),su.FONTS["WADIM"],image)
                            self.State.redraw = True
                            pg.key.set_repeat()
                        else:
                            self.Exit.done = True
                #Pass the event to the applicable state or to the exit prompt.
                if not self.Exit:
                    self.State.event_manager(event)
                else:
                    self.Exit.event_manager(event)

                if event.type == pg.QUIT:
                    self.State = "QUIT"

    def lowest_image(self,Menu):
        """Get the image of the deepest sub-menu (best for full-screen sized menus)."""
        if not Menu.sub:
            return Menu.image
        else:
            return self.lowest_image(Menu.sub)

    def reset(self):
        """Reset the game so that it loops and go to Menu state."""
        if self.Gamer.lose:
            self.__init__() #Recreate everything.
            self.State = self.state_dict["MENU"]
            self.State.start_time = pg.time.get_ticks()

    def update(self,Surf):
        """Updates the current State; checks if it is done; and updates the
        State accordingly based on the current states 'next' variable."""
        if not self.Exit:
            self.State.update(Surf)
        else:
            self.Exit.update(Surf)
            if self.Exit.done:
                if self.Exit.done == "QUIT":
                    self.State.done = "QUIT"
                else:
                    self.Exit = None
                    self.State.start_time = pg.time.get_ticks()
        if self.State.done:
            if self.State.done == "QUIT":
                self.State = "QUIT"
            else:
                self.State.state_cleanup()
                next_state = self.State.next
                self.State = self.state_dict[next_state]
                self.State.start_time = pg.time.get_ticks()
                if next_state == "TOP":
                    self.State.score = self.Gamer.score
                    self.State.level = self.Gamer.level
                elif next_state == "MENU":
                    self.reset()
                elif next_state == "GAME":
                    self.State.controls = self.get_controls()

    def main(self):
        """Control flow for everything"""
        while 1:
            self.control_events()
            if self.State == "QUIT":
                break
            else:
                self.update(su.SURFACE)
            #Display the framerate in the window title if showfps is True.
            if self.showfps:
                frames = self.myclock.get_fps()
                pg.display.set_caption("{} - FPS: {:.2f}".format(su.CAPTION,frames))
            elif pg.display.get_caption()[0] != su.CAPTION:
                pg.display.set_caption(su.CAPTION)
            self.myclock.tick(self.fps)

            su.monitor.blit(pg.transform.scale(su.SURFACE, (640,480)), (0,0))
            pg.display.flip()
        pg.quit();sys.exit()
