from kjv import actor
import pygame
from pygame.locals import *
from math import *
from random import *
from game import sfx
import game

TW,TH = 32,16

BALL_SPEED_START = 250
BALL_SPEED_MAX = 600

PADDLE_SMALL = 24
PADDLE_MEDIUM = 48
#PADDLE_LONG = 72
PADDLE_LONGER = 36
PADDLE_LONGEST = PADDLE_MEDIUM + PADDLE_LONGER*3

def block_shadow(level,x,y):
	lay0 = level.layers[0]

	n = level.layers[2][y][x]
	m = 24
	if 0<lay0[y][x-1]<10: m += 1
	if 0<lay0[y-1][x-1]<10: m += 2
	if 0<lay0[y-1][x]<10: m += 4
	if 0<lay0[y][x]<10: m = 0
	if m != n:
		level.layers[2][y][x] = m
		level.alayer[y][x] = 1

def tile_death(level,a,b):
	item_kill(level,a,b)
def tile_block(level,a,b):
	return block_hit(level,a,b)

def block_hit(level,a,b):
	c = a.config

	if (c['top'] == 1 and b.prev.bottom <= a.prev.top and b.cur.bottom > a.cur.top):
		b.cur.bottom = a.cur.top
		if b.config['bouncy']: b.vy *= -1

	if (c['left'] == 1 and b.prev.right <= a.prev.left and b.cur.right > a.cur.left):
		b.cur.right = a.cur.left
		if b.config['bouncy']: b.vx *= -1

	if (c['right'] == 1 and b.prev.left >= a.prev.right and b.cur.left < a.cur.right):
		b.cur.left = a.cur.right
		if b.config['bouncy']: b.vx *= -1

	if (c['bottom'] ==1 and b.prev.top >= a.prev.bottom and b.cur.top < a.cur.bottom):
		b.cur.top = a.cur.bottom
		if b.config['bouncy']: b.vy *= -1
		if b.config.get('bouncydie',0):
			level.remove(b)
			level.lasers -= 1 #HACK: assumed



	if (b.config.get('junk',0) == 1):
		return

	if c.get('explode',0) == 1:
		block_explode(level,a)

	elif c.get('enext',0) != 0:
		level.set(a.tx,a.ty,a.config['enext'])
		sfx['hardmetal'].play()


def block_explode(level,a):
	c = a.config
	x,y = a.tx,a.ty
	a.cur.x = x*TW
	a.cur.y = y*TH
	n = level.get(x,y)
	level.set(a.tx,a.ty,a.config['enext'])
	clayer = level.clayer
	alayer = level.alayer
	clayer[y][x] = 0
	if n == 7:
		sfx['tink'].play()
		clayer[y-1][x],clayer[y+1][x],clayer[y][x-1],clayer[y][x+1] = -1,-1,-1,-1
		alayer[y-1][x],alayer[y+1][x],alayer[y][x-1],alayer[y][x+1] = -1,-1,-1,-1
	elif n == 8:
		sfx['metal'].play()
	else:
		sfx['tick'].play()
	block_shadow(level,a.tx,a.ty)
	block_shadow(level,a.tx+1,a.ty)
	block_shadow(level,a.tx,a.ty+1)
	block_shadow(level,a.tx+1,a.ty+1)
	level.score += 11
	#level.scorev += 8
	level.showscore()
	n = 30
	if level.sissy: n = 15
	if c.get('pill',0)==1 and randrange(0,n)==0:
		pill_new(level,a.cur.x,a.cur.y,choice(['e','s','l','c','p','3'])) #'w'
		#pill_new(level,a.cur.x,a.cur.y,choice(['l'])) #'w'



def pill_new(level,x,y,t):
	s = actor(level.images["pills."+t],x,y)

	s.type = t
	s.update = pill_update
	s.vy = 96
	s.agroups = 0
	s.groups = level.string2groups("pill")

	level.add(s)
	#s.shadow = shadow_new(level,level.images["pill_shadow"],s)
	return s

def pill_update(level,a,t):
	a.y += a.vy*t

def ball_speed(level,a,v):
	a.v = v
	if a.v > BALL_SPEED_MAX:
		a.v = BALL_SPEED_MAX
	#print 'ball speed: ' + `a.v`
	an = atan2(a.vy,a.vx)
	a.vx = cos(an)*a.v
	a.vy = sin(an)*a.v



def item_angle(a):
	an = atan2(a.vy,a.vx)
	an = an*360.0/(2.0*pi)
	an = int(an)
	m = an/90
	n = an%90
	d = 6#15
	if n<d: n = d
	if n>90-d: n=90-d
	an = m*90+n
	an = an*2.0*pi/360.0
	a.vx = cos(an)*a.v
	a.vy = sin(an)*a.v


def ball_update(level,a,t):
	if a.caught == 0:
		a.x += a.vx*t
		a.y += a.vy*t
		a.t += t
		n = 5
		if level.sissy: n = 10
		if a.t > n:
			ball_speed(level,a,a.v+10)
			a.t = 0
		item_angle(a)
	else:
		a.cur.bottom = a.caught.cur.top
		a.x = a.caught.x + a.caught_x
		#a.caught = 0 #HACK

def ball_updates(level,aas,t):
	for a in aas:
		a.x += a.vx*t
		a.y += a.vy*t

def sign(v):
	if v<0: return -1
	if v>0: return 1
	return 0

def player_update(level,a,t):
	#if hasattr(a,'ball'): a.cur.centerx = a.ball.cur.centerx

	a.x += a.vx*t
	if a.dw != a.cw:
		a.x -= sign(a.dw-a.cw)
		a.cw += sign(a.dw-a.cw)*2
	a.tosprite(level.images['paddle.%s.%d'%(a.cp,a.cw)])
	if level.balls == 0:
		a.update = player_update_boom
		a.frame = 0
		level.listeners = {}
		sfx['bang'].play()



def player_update_boom(level,a,t):
	a.frame += 1
	if a.frame == 16:
		level.remove(a)
		level.dead = 1
		return
	x,y = a.cur.centerx,a.cur.centery
	a.tosprite(level.images['boom.%d'%(a.frame/2+1)])
	a.cur.centerx,a.cur.centery = x,y


def updates(level,aas,t):
	for a in aas:
		a.update(level,a,t)

def player_hit(level,a,b):
	if b.prev.bottom <= a.prev.bottom:
		gl = level.groups2list(b.groups)
		"""
		if 'ball' in gl:
			b.cur.bottom = a.cur.top
			a.ball = b

			v = (b.vx**2 + b.vy**2)**0.5
			#p = float(b.cur.centerx - a.cur.x) / float(a.cur.width)
			p = randrange(0,1000)/1000.0
			n = pi + pi/4 + p*pi*2/4
			b.vx = cos(n)*v
			b.vy = sin(n)*v

			level.score += 3
			level.showscore()
			level.hits += 1
		if 'pill' in gl:
			pass

		return
		"""

		if 'ball' in gl:
			b.cur.bottom = a.cur.top

			v = (b.vx**2 + b.vy**2)**0.5
			p = float(b.cur.centerx - a.cur.x) / float(a.cur.width)
			#n = pi + pi/4 + p*pi*2/4
			n = pi + pi/6 + p*pi*4/6
			b.vx = cos(n)*v
			b.vy = sin(n)*v

			if a.catch:
				player_catch(level,a,b)

			level.hits += 1
			level.score += 3
			level.showscore()
			sfx['snap'].play()

		elif 'pill' in gl:
			pdw = a.dw
			a.dw = PADDLE_MEDIUM
			if level.sissy:
				a.dw += PADDLE_LONGER
			a.catch = 0
			a.laser = 0
			a.cp = 'p'
			level.score += 37
			level.showscore()
			sfx['blip'].play()
			if b.type == 'e':
				a.dw = min(PADDLE_LONGEST,pdw+PADDLE_LONGER)
				a.cp = 'e'
				#a.tosprite(level.images['paddle.72'])
				#a.shadow.setimage(level.images['paddle2_shadow'])
				sfx['woop'].play()
				pass
			elif b.type == 's':
				bgroup = level.groups['ball']
				for s in level.sprites:
					if (s.groups & bgroup)!=0:
						ball_speed(level,s,BALL_SPEED_START)
			elif b.type == '3':
				bgroup = level.groups['ball']
				for s in level.sprites[:]:
					if (s.groups & bgroup)!=0:
						ball_new(level,s.x,s.y,s.v)
						ball_new(level,s.x,s.y,s.v)
						break
			elif b.type == 'l':
				a.cp = 'l'
				a.laser = 1
			elif b.type == 'c':
				a.cp = 'c'
				a.catch = 1
			elif b.type == 'w':
				level.nextlevel()
			elif b.type == 'p':
				level.lives += 1
				level.showlives()
			if pdw > a.dw:
				sfx['bew'].play()

			item_kill(level,a,b)

def player_catch(level,a,b):
	b.cur.bottom = a.cur.top
	b.caught = a
	b.caught_x = b.cur.x-a.cur.x
	if b.vy > 0: b.vy=-b.vy

def player_event(level,a,e):
	shoot = 0
	if e.type is KEYDOWN:
		if e.key == K_LEFT:
			a.vx -= 600
		elif e.key == K_RIGHT:
			a.vx += 600
		elif e.key == K_ESCAPE:
			level.quit=1
		elif e.key == K_f:
			pygame.display.toggle_fullscreen()
		elif e.key == K_3:
			bgroup = level.groups['ball']
			for s in level.sprites:
				if (s.groups & bgroup)!=0:
					ball_new(level,s.x,s.y,s.v)
					ball_new(level,s.x,s.y,s.v)
					break
		elif e.key == K_F12:
			level.blocks=0
		elif e.key in (K_p, K_RETURN):
			game.pause("Pause")
   			level.loop_paint()
		elif e.key == K_SPACE:
			shoot = 1


	elif e.type is KEYUP:
		if e.key == K_LEFT:
			a.vx += 600
		elif e.key == K_RIGHT:
			a.vx -= 600
	elif e.type is MOUSEMOTION:
		#a.x = e.pos[0] - a.cur.width/2 + level.origin.x
		#if
		a.cur.centerx = e.pos[0]+level.origin.x
		if a.cur.left < level.origin.x+TW: a.cur.left = level.origin.x+TW
		if a.cur.right > level.origin.x+TW*19: a.cur.right = level.origin.x+TW*19
		a.x = a.cur.x
		a.y = a.cur.y

	elif e.type is MOUSEBUTTONDOWN:
		shoot = 1

	if shoot == 1:
		g = level.string2groups("ball")
		for s in level.sprites:
			if (s.groups & g) !=0 and s.caught == a:
				if s.vy > 0: s.vy = -s.vy #in case it hit a floating thing
				s.caught=0
		if a.laser and level.lasers == 0:
			laser_new(level,a)
			sfx['laser'].play()

def player_new(level,x,y):
	w=PADDLE_MEDIUM
	if level.sissy:
		w += PADDLE_LONGER
	s = actor(level.images["paddle.p.%d"%w],x,y)
	s.hit = player_hit
	s.event = player_event
	s.update = player_update
	s.updates = updates
	s.vx,s.vy = 0,0
	s.cw,s.dw = w,w
	s.cp = 'p'

	s.config = {'bouncy':0}
	s.groups = level.string2groups("player")
	s.agroups = level.string2groups("ball,pill")
	level.add(s)
	#s.shadow = shadow_new(level,level.images["paddle_shadow"],s)
	s.catch = 0
	s.laser = 0
	return s

def rsign():
	return randrange(0,2)*2-1

def laser_new(level,p):
	v = -900
	a = actor(level.images['laser'],p.cur.left,p.cur.top)
	a.update = laser_update
	a.groups = level.string2groups('laser')
	a.config = {'bouncy':0,'bouncydie':1}
	a.vy = v
	a.vx = 0
	level.add(a)

	a = actor(level.images['laser'],p.cur.right-a.cur.w,p.cur.top)
	a.update = laser_update
	a.groups = level.string2groups('laser')
	a.config = {'bouncy':0,'bouncydie':1}
	a.vy = v
	a.vx = 0
	level.add(a)

	level.lasers = 2

def laser_update(level,a,t):
	a.x += a.vx*t
	a.y += a.vy*t

def junk_new(level,x,y):
	js = [('sphere',24),('pyramid',16),('cubes',48)]
	img,imgframes = js[level.junks_cur] #choice(js)
	a = actor(level.images['%s.1'%img],x,y)
	a.update = junk_update
	a.hit = junk_hit
	a.img = img
	a.frame = 0
	a.imgframes = imgframes
	a.groups = level.string2groups("junk")
	a.agroups = level.string2groups("ball,player,laser")
	a.v = randrange(30,60)
	an = randrange(0,360)*2.0*pi/360.0
	a.vx = cos(an)*a.v
	a.vy = sin(an)*a.v
	item_angle(a)
	#a.vy = abs(a.vy)
	a.config = {'bouncy':1,'junk':1}
	a.boom = 0
	level.add(a)
	level.junks += 1
	return a

def junk_update(level,a,t):
	a.frame += 1
	if not a.boom:
		a.tosprite(level.images['%s.%d'%(a.img,(a.frame%a.imgframes)+1)])
		a.x += a.vx*t
		a.y += a.vy*t
		if level.sissy and a.y > TH*20 and a.vy > 0:
			a.vy = -a.vy
	else:
		if a.frame == 16:
			level.remove(a)
			level.junks -= 1
			return
		a.tosprite(level.images['boom.%d'%(a.frame/2+1)])

def junk_hit(level,a,b):
	a.boom = 1
	a.frame = 0
	a.agroups = 0
	a.groups = 0
	if (b.groups & level.groups['ball'])!=0:
		an = randrange(0,100)*pi/100.0
		b.vx = cos(an)*b.v
		b.vy = sin(an)*b.v
	if (b.groups & level.groups['laser'])!=0:
		level.remove(b)
		level.lasers -= 1
	level.score += 23
	level.showscore()
	sfx['bang'].play()

def shadow_update(level,a,t):
	a.x = a.shadowing.x+8
	a.y = a.shadowing.y+8

def shadow_updates(level,aas,t):
	for a in aas:
		a.x = a.shadowing.x+8
		a.y = a.shadowing.y+8

def shadow_new(level,image,a):
	s = actor(image,a.x,a.y)
	s.update = shadow_update
	s.updates = shadow_updates
	s.groups = 0
	s.agroups = 0
	s.z = 4
	s.shadowing = a
	level.add(s)
	return (s)

def ball_new(level,x,y,v):
	s = actor(level.images["ball"],x,y)
	s.hit = 0
	s.update = ball_update
	s.updates = ball_updates
	a = randrange(1,1000)
	s.v = v
	s.vx,s.vy = cos(a)*v,sin(a)*v
	s.config = {'bouncy':1}
	s.agroups = 0
	s.groups = level.string2groups("ball")
	level.add(s)
	#s.shadow = shadow_new(level,level.images["ball_shadow"],s)
	s.caught = 0
	s.t = 0
	level.balls += 1
	return s


def item_kill(level,a,b):
	if hasattr(b,'killed'): return
	level.remove(b)
	if hasattr(b,'shadow'):
		level.remove(b.shadow)
	if (b.groups & level.groups['ball'])!=0:
		level.balls -= 1
		if level.balls == 0:
			gp = level.groups['player']
			for p in level.sprites:
				if (p.groups & gp) != 0:
					level.lives -= 1
					level.showlives()
					#if level.lives:
					#	d = ball_new(level,p.cur.centerx,p.cur.top,BALL_SPEED_START)
					#	player_catch(level,p,d)
	if (b.groups & level.groups['junk'])!=0:
		level.junks -= 1
	b.killed = 1



def level_init(level):
	level.balls = 0
	level.blocks = 0
	level.junks = 0

	for yl in level.layers[0]:
		for t in yl:
			if level.tiles[t].config.get('explode',0) == 1: level.blocks += 1

	level.next = [0 for x in xrange(0,256)]
	id = 0
	for e in level.tiles:
		if e != None:
			#id = int(e.config['id'],16)
			level.next[id] = e.config.get("next",id)
		id += 1



