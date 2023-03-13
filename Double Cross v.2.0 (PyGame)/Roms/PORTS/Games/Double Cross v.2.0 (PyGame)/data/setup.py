"""Module: setup.py
Overview:
    Display initialization, global constants, and graphic/sound/font loading.
Functions:
    _get_graphics(directory,alpha=False)
    _get_sounds(directory)
    _play_first_song()
Globals:
    SCREENSIZE
    CAPTION
    SURFACE (not technically a constant as it is the display surface)
    PLAYER1_DEFAULT
    PLAYER2_DEFAULT
    FONTS
    COLORS
    GFXA
    SFX"""
try:
    #This is here so that this application gets its own icon in the taskbar
    #when being run on Windows 7, rather than stacked as another python application.
    import ctypes as _ctypes
    _myappid = 'double_cross'
    _ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(_myappid)
except (ImportError,AttributeError):
    pass

import os
import pygame as pg

os.environ['SDL_VIDEO_CENTERED'] = '1'
pg.mixer.pre_init(44100, -16, 2, 8192)
pg.mixer.init()

#Global constants.
SCREENSIZE = (520,520) #Global screen size(520,520)
CAPTION    = "Double Cross"

pg.init()
#set_icon and set_caption before set_mode.
_icon = pg.image.load(os.path.join("graphics","dc_icon.png"))
pg.display.set_icon(_icon)
pg.display.set_caption(CAPTION)
monitor = pg.display.set_mode((640,480))
SURFACE = pg.Surface(SCREENSIZE)

#Dictionary of used fonts.
FONTS = {}
FONTS["WADIM"]   = pg.font.Font(os.path.join('fonts','wadim_giant.ttf'),40)
FONTS["WADIM_S"] = pg.font.Font(os.path.join('fonts','wadim_giant.ttf'),35)
FONTS["WADIM_I"] = pg.font.Font(os.path.join('fonts','wadimi.ttf'),35)
FONTS["WADIM_IBIG"] = pg.font.Font(os.path.join('fonts','wadimi.ttf'),45)
FONTS["ARIAL"]   = pg.font.Font(os.path.join('fonts','arial.ttf'),16)
FONTS["IMPACT"]  = pg.font.Font(os.path.join('fonts','impact.ttf'),35)

#Player one control defaults
PLAYER1_DEFAULT = ((pg.K_LEFT,pg.K_RIGHT,pg.K_UP,pg.K_DOWN),
                   (pg.K_DOWN,pg.K_UP,pg.K_LEFT,pg.K_RIGHT))

#Player two control defaults
PLAYER2_DEFAULT = ((pg.K_LEFT,pg.K_RIGHT,pg.K_UP,pg.K_DOWN),
                   (pg.K_s,pg.K_w,pg.K_a,pg.K_d))

#Dict of commonly used colors
COLORS = {}
COLORS["RED"]   = (255,0,0)
COLORS["WHITE"] = (255,255,255)
COLORS["BLUE"]  = (0,0,255)
COLORS["BLACK"] = (0,0,0)
COLORS["YELLOW"] = (255,255,0)

def _get_graphics(directory,alpha=False):
    """Returns a dictionary of all the image files in a directory.
    Dictionary keys are image names minus their file extensions."""
    dirlist = os.listdir(directory)
    graphic = {}
    for graf in dirlist:
        if graf[-3:] in ("png","jpg"):
            if not alpha:
                graphic[graf[:-4]] = pg.image.load(os.path.join(directory,graf)).convert()
                graphic[graf[:-4]].set_colorkey((255,0,255))
            else:
                graphic[graf[:-4]] = pg.image.load(os.path.join(directory,graf)).convert_alpha()
    return graphic

def _get_sounds(directory):
    """Returns a dictionary of all the sound effect files in a directory.
    Dictionary keys are names minus their file extensions."""
    dirlist = os.listdir(directory)
    sound = {}
    for fx in dirlist:
        if fx[-3:] == "wav":
            sound[fx[:-4]] = pg.mixer.Sound(os.path.join(directory,fx))
    return sound

def play_song(song,vol):
    """If song not found our program won't crash in a fiery blaze."""
    if song in os.listdir(os.path.join('sound','music')):
        pg.mixer.music.load(os.path.join('sound','music',song))
        pg.mixer.music.set_volume(vol)
        pg.mixer.music.play(-1)

GFXA = _get_graphics("graphics",True) #Dictionary of graphics
SFX  = _get_sounds(os.path.join("sound","effects")) #Dictionary of sound effects

#Play the first song. Music select module will control the others.
play_song('Korobelniki.mp3',0.7)
