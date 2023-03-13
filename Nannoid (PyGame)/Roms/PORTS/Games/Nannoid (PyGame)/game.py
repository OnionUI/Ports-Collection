import pygame
from pygame.locals import *
import random
import os

pygame.display.init()
pygame.font.init()
#pygame.display.set_icon(pygame.image.load("images/js5_icon.gif"))
pygame.display.set_caption("Nannoid");
pygame.display.set_icon(pygame.image.load("icon.png"))
pygame.mixer.pre_init(44100, -16, 2, 8192)
pygame.mixer.init()

sfx = {}
#for fname in ['bang','bew','blip','bloop','ding','explode','foghorn','hardmetal','hey','laser','metal','snap','tick','tink','win','woop','yipee']:
for fname in ['bloop','bang','bew','blip','foghorn','hardmetal','hey','laser','metal','snap','tick','tink','woop','yipee']:
	#print fname
	sfx[fname] = pygame.mixer.Sound('sfx/%s.wav'%fname)

SW,SH = 640,480
screen = pygame.display.set_mode((SW,SH),SWSURFACE)#|FULLSCREEN)
TW,TH = 32,16
W,H = SW/TW,SH/TH

#pygame.mouse.set_visible(0)

fnt = "yellow.ttf"
fontsmall = pygame.font.Font(fnt,45)
fontmedium = pygame.font.Font(fnt,65)
fontlarge = pygame.font.Font(fnt,135)

colorscore = (0,230,250)
colorpause = (0,230,250)

colortitle = (0,230,250)
colortext = (0,184,193)
colorbright = (178,251,255)


from level import level
lvl = level()
lvl.screen = screen
lvl.score = 0
lvl.scur = 0
lvl.cur = 1
lvl.sissy = 0

def run(state):
	while state != None:
		state = state()

def state_quit():
	return None

#play_levels = [0,21,9,6,5,16,2,23,4,17,13,8,1,11,18,20,15,14,10,19,7,22,12,3]
play_levels = [0,39,21,13,5,17,6,7,29,11,1,38,30,15,2,23,4,14,9,19,18,22,3,34]

def state_play():
	grab(1)
	#pygame.mixer.music.stop()
	lvl.bkgr_fname = 'images/title.jpg'
	lvl.tiles_fname = 'etiles.png'
	lvl.init_graphics()
	lvl.quit = 0
	lvl.lives = 3
	lvl.score = 0
	lvl.scorev = 0
	lvl.dead = 0
	#lvl.cur = 0
	lvl.blocks = 0
	lvl.deaths = 0
	lvl.hits = 0
	lvl.frames = 0

	if lvl.sissy: lvl.lives = 5

	lvl.level_fname = "levels/%d.lvl" % play_levels[lvl.cur]
	n = lvl.cur-1
	lvl.bkgr_fname = "images/bkgr%d.jpg" % ((n/3)%3+1)
	lvl.bkgr = pygame.image.load(lvl.bkgr_fname).convert()
	lvl.junks_cur = (n%3)
	lvl.load()
	lvl.init()
	lvl.start()
	
	while 1:
		lvl.frames += 1
		if lvl.blocks == 0:
			if lvl.cur:
				sfx['yipee'].play()
				pause("Good Job!")
				
			lvl.cur += 1
			if lvl.cur > 23:
				pause("You Won!")
				return state_hs

			"""
			if lvl.scur:
				lvl.cur = lvl.scur
			else:
				lvl.cur += 1
			"""

			lvl.level_fname = "levels/%d.lvl" % play_levels[lvl.cur]
			n = lvl.cur-1
			lvl.bkgr_fname = "images/bkgr%d.jpg" % ((n/3)%3+1)
			lvl.bkgr = pygame.image.load(lvl.bkgr_fname).convert()
			lvl.junks_cur = (n%3)
			lvl.load()
			lvl.init()
			lvl.start()
		lvl.loop()
		#pygame.display.flip()
		if lvl.dead:
			lvl.deaths += 1
			if lvl.lives:
				lvl.start()
			else:
				sfx['foghorn'].play()
				pause("Game Over")
				return state_hs
		if lvl.quit == 1:
			return state_hs



hs_entries = 5
hs_default = [(100,'Cuzco'),(100,'Phil'),(100,'Nan'),(100,'Tim'),(100,'Jet')]
hs_fnames = ["hs_normal.sav","hs_sissy.sav"]

import pickle

def hs_load():
	if os.path.isfile(hs_fnames[lvl.sissy]):
		hs = pickle.load(open(hs_fnames[lvl.sissy],"rb"))
	else:
		hs = hs_default
	return hs

def hs_save(hs):
	pickle.dump(hs,open(hs_fnames[lvl.sissy],"wb"))

def hs_check(sc):
	hs = hs_load()
	for k in range(0,hs_entries):
		v = hs[k]
		if v[0] < sc:
			return True
	return False

def hs_add(sc,name):
	hs = hs_load()
	for k in range(0,hs_entries):
		v = hs[k]
		if v[0] < sc:
			hs[k:k] = [(sc,name)]
			hs_save(hs[0:hs_entries])
			return True
	return False

def enter(text,maxlen,e):
	if e.key == K_BACKSPACE:
		text = text[:-1]
	else:
		if len(text) < maxlen:
			try: text = text + str(e.unicode)
			except: pass
	return text

def state_newhs():
	grab(0)
	sc = lvl.score
	lvl.score = 0
	name = ""

	img = pygame.image.load("images/title.jpg")

	sfx['hey'].play()

	done = False
	while not done:
		screen.blit(img,(0,0))
		pprint("new record",fontlarge,colortitle,(0,0,screen.get_width(),0),8)
		pprint("please enter your name below",fontsmall,colortext,(0,130,screen.get_width(),0),8)

		pprint(name+"_",fontmedium,colorbright,(0,250,screen.get_width(),0),8)
		pygame.display.flip()
		pygame.time.wait(100)

		e = getch()
		if e.key == K_RETURN: done = 1
		else:
			name = enter(name,15,e)

	hs_add(sc,name)
	return state_hs

def state_hs():
	grab(0)
	sc = lvl.score
	if hs_check(sc):
		return state_newhs
	hs = hs_load()

	img = pygame.image.load("images/title.jpg")
	screen.blit(img,(0,0))
	pprint("high scores",fontlarge,colortitle,(0,0,screen.get_width(),0),8)

	x,y,w,h = 50,145,640-100,100
	c = colorbright
	for h in hs:
		pprint(h[1],fontmedium,c,(x,y,w,h),7)
		pprint(str(h[0]),fontmedium,c,(x,y,w,h),9)
		y += 60
		c = colortext

	pygame.display.flip()

	getch()

	return state_menu

def state_normal():
	lvl.sissy = 0
	return state_play

def state_sissy():
	lvl.sissy = 1
	return state_play


def state_intro():
	return state_menu

def state_menu():
	#pygame.mixer.music.load("budda1.far")
	#pygame.mixer.music.play()
	grab(0)
	bg = pygame.image.load("images/title.jpg")
	#ball = pygame.image.load("bigball.png")
	menu = [
		('mode: <M>',state_play),
		('level: <L>',state_play),
		('high scores',state_hs),
		('help & info',state_help),
		('quit',state_quit),
		]
		
	if lvl.cur > 23: lvl.cur = 1
	if lvl.cur < 0: lvl.cur = 1
	modes = ('normal','sissy')

	pos = 0
	while 1:
		screen.blit(bg,(0,0))
		r = pprint("nannoid",fontlarge,colortitle,(0,0,screen.get_width(),0),8)
		x,y = r.left,130+abs(len(menu)-5)*40 #sissy mode stuff..
		boxes = []
		for k in range(0,len(menu)):
			v = menu[k]
			vv = v[0]
			vv = vv.replace("L",str(lvl.cur))
			vv = vv.replace("M",modes[lvl.sissy])
			
			if pos == k:
				#screen.blit(ball,(x-60,y+32))
				r=pprint(vv,fontmedium,colorbright,(x,y),7)
			else:
				r=pprint(vv,fontmedium,colortext,(x,y),7)
			boxes.append((r,k))
			y += 64
		pygame.display.flip()

		done = 0
		while not done:
			for e in pygame.event.get():
				if e.type is KEYDOWN:
					if e.key == K_UP:
						pos -= 1
						sfx['bloop'].play()
					if e.key == K_DOWN:
						pos += 1
						sfx['bloop'].play()
					pos = (pos+len(menu))%len(menu)
					done = 1
					if e.key == K_LEFT:
						sfx['bloop'].play()
						if pos == 0: lvl.sissy ^= 1
						if pos == 1: lvl.cur = max(1,(lvl.cur-1))
					if e.key == K_RIGHT:
						sfx['bloop'].play()
						if pos == 0: lvl.sissy ^= 1
						if pos == 1: lvl.cur = min(23,(lvl.cur+1))
					if e.key == K_ESCAPE:
						return state_quit
					if e.key == K_RETURN:
						return menu[pos][1]
				if e.type is MOUSEMOTION:
					for box,p in boxes:
						if done == 0 and box.collidepoint(e.pos):
							if p != pos:
								sfx['bloop'].play()
								pos = p
							done = 1
				if e.type is MOUSEBUTTONDOWN:
					return menu[pos][1]

			pygame.time.wait(1)


def state_help():
	grab(0)
	bg = pygame.image.load("images/title.jpg")
	helps =[
		[
		"help",
		"this is a paddle, ball, bricks game. ",
		"we're sure you can figure it out. ",
		"",
		"23 levels ",
		"11 points per brick ",
		"37 points per pill ",
		"23 points per weird floaty thing ",
		"extra life at 20,000 points ",
		],
		[
		"credits",
		"phil hassey",
		"    code, graphics, sfx, levels,...",
		"",
		"luke ulrich",
		"    blender tutorial",
		"",
		"daniel nicholson",
		"    music",
		],
		[
		"about",
		"coded using ",
		"    pygame, sdl, python",
		"",
		"graphics created with ",
		"    the gimp, blender ",
		"",
		"sfx created with audacity and",
		"    various kitchen implements",
		],

		]

	for help in helps:
		screen.blit(bg,(0,0))
		pprint(help[0],fontlarge,colortitle,(0,0,screen.get_width(),0),8)

		x,y = 32,150
		for line in help[1:]:
			pprint(line,fontsmall,colortext,(x,y),7)
			y+=38

		pygame.display.flip()

		getch()

	return state_menu

class kevt:
	def __init__(self,key):
		self.type = KEYDOWN
		self.key = key
		self.unicode = '';

def getch():
    dx,dy = 0,0
    while 1:
    	ok = 1
	r = 0
    	while ok:
        	e = pygame.event.poll()
		ok = e.type
		if e.type is KEYDOWN:
		        return e
		if e.type is MOUSEBUTTONDOWN:
			r=kevt(K_RETURN)
		"""
		if e.type is MOUSEMOTION:
			dx+=e.rel[0]
			dy+=e.rel[1]
			if max(abs(dx),abs(dy)) > 24:
				if abs(dx) > abs(dy):
					if dx<0: r=kevt(K_LEFT)
					if dx>0: r=kevt(K_RIGHT)
				else:
					if dy<0: r=kevt(K_UP)
					if dy>0: r=kevt(K_DOWN)
		"""
	if r: return r

        pygame.time.wait(10)

def pprint(s,fnt,clr,box,align=7):
	text = fnt.render(s,1,clr)
	shadow = fnt.render(s,1,(0,0,0))
	high = fnt.render(s,1,(255,255,255))
	w,h = text.get_width(),text.get_height()
	if len(box) == 2:
		box = (box[0],box[1],0,0)
	x,y = box[0],box[1]
	if align in (8,5,2): x += (box[2]-w)/2
	if align in (9,6,3): x += box[2]-w
	if align in (4,5,6): y += (box[3]-h)/2
	if align in (1,2,3): y += box[3]-h
	#screen.blit(shadow,(x-1,y-1))
	#screen.blit(shadow,(x+3,y+3))
	screen.blit(high,(x-1,y-1))
	screen.blit(shadow,(x+2,y+2))
	screen.blit(text,(x,y))
	return Rect(x,y,w,h)

def pause(s,s2=""):
    #render()
    p=grab(0)
    r = pprint(s,fontlarge,colorpause,(0,0,screen.get_width(),screen.get_height()),5)
    pprint(s2,fontmedium,colorpause,(0,r.bottom,screen.get_width(),0),8)

    pygame.display.flip()
    ok = 1
    while ok:
	e = getch()
	if e.key == K_RETURN: ok = 0
    lvl.loop_paint()
    #update_all()
    #render()
    p=grab(p)

def spause(s,s2=""):
    #render()
    p=grab(0)
    r = pprint(s,fontlarge,colorpause,(0,0,screen.get_width(),screen.get_height()),5)
    pprint(s2,fontmedium,colorpause,(0,r.bottom,screen.get_width(),0),8)

    pygame.display.flip()

    ok = 1
    while ok:
	e = getch()
	if e.key in (K_1,K_2,K_3,K_4,K_5):
		lvl.loop_paint()
		grab(p)
		return e.key - K_1+1
	elif e.key == K_ESCAPE:
		lvl.loop_paint()
		grab(p)
		return 0
    lvl.loop_paint()

    #update_all()
    #render()

grab_state = 0
def grab(n):
	global grab_state
	p = grab_state
	if n:
		pygame.event.set_grab(True)
		pygame.mouse.set_visible(False)
		
	else:
		pygame.event.set_grab(False)
		pygame.mouse.set_visible(True)
	grab_state = n
	return p



