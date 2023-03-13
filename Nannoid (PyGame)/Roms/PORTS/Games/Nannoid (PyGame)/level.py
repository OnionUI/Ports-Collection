from kjv import kjv
from tilevid import sprite
from tilevid import tile
from code import *
from pygame.rect import *
from random import *

import game

TW,TH = 32,16

from images import images

#initialize the codes
#image, alignment, new, config
codes = [None for x in range(0,256)]

#initialize the tiles
#agroups,hit,config
tiles = [(0,0,0) for x in range(0,256)]

#0
tiles[0] = (0,0,0)
tiles[1] = ('ball,junk,laser',tile_block,{'top':1,'left':1,'right':1,'bottom':1,'enext':16,'explode':1,'pill':1})
tiles[2] = ('ball,junk,laser',tile_block,{'top':1,'left':1,'right':1,'bottom':1,'enext':16,'explode':1,'pill':1})
tiles[3] = ('ball,junk,laser',tile_block,{'top':1,'left':1,'right':1,'bottom':1,'enext':16,'explode':1,'pill':1})
tiles[4] = ('ball,junk,laser',tile_block,{'top':1,'left':1,'right':1,'bottom':1,'enext':16,'explode':1,'pill':1})
tiles[5] = ('ball,junk,laser',tile_block,{'top':1,'left':1,'right':1,'bottom':1,'enext':16,'explode':1,'pill':1})
tiles[6] = ('ball,junk,laser',tile_block,{'top':1,'left':1,'right':1,'bottom':1,'enext':32,'explode':0})
tiles[7] = ('ball,junk,laser',tile_block,{'top':1,'left':1,'right':1,'bottom':1,'enext':16,'explode':1,'pill':1})

tiles[8] = ('ball,junk,laser',tile_block,{'top':1,'left':1,'right':1,'bottom':1,'enext':40,'explode':1})
tiles[9] = ('ball,junk,laser',tile_block,{'top':1,'left':1,'right':1,'bottom':1,'enext':16,'explode':1,'pill':1})

tiles[13] = ('ball,player,junk,laser',tile_block,{'top':0,'left':0,'right':0,'bottom':1,'enext':13}) #at top
tiles[14] = ('ball,player,junk,laser',tile_block,{'top':1,'left':1,'right':1,'bottom':1,'enext':14})
tiles[15] = ('ball,pill,junk,laser',tile_death,0)

tiles[16] = (0,0,{'next':17})
tiles[17] = (0,0,{'next':18})
tiles[18] = (0,0,{'next':19})
tiles[19] = (0,0,{'next':20})
tiles[20] = (0,0,{'next':21})
tiles[21] = (0,0,{'next':22})
tiles[22] = (0,0,{'next':23})
tiles[23] = (0,0,{'next':0})

tiles[32] = ('ball,junk,laser',tile_block,{'top':1,'left':1,'right':1,'bottom':1,'next':33})
tiles[33] = ('ball,junk,laser',tile_block,{'top':1,'left':1,'right':1,'bottom':1,'next':34})
tiles[34] = ('ball,junk,laser',tile_block,{'top':1,'left':1,'right':1,'bottom':1,'next':35})
tiles[35] = ('ball,junk,laser',tile_block,{'top':1,'left':1,'right':1,'bottom':1,'next':36})
tiles[36] = ('ball,junk,laser',tile_block,{'top':1,'left':1,'right':1,'bottom':1,'next':37})
tiles[37] = ('ball,junk,laser',tile_block,{'top':1,'left':1,'right':1,'bottom':1,'next':38})
tiles[38] = ('ball,junk,laser',tile_block,{'top':1,'left':1,'right':1,'bottom':1,'next':39})
tiles[39] = ('ball,junk,laser',tile_block,{'top':1,'left':1,'right':1,'bottom':1,'next':6})

tiles[40] = ('ball,junk,laser',tile_block,{'top':1,'left':1,'right':1,'bottom':1,'next':41,'enext':16,'explode':1,'pill':1})
tiles[41] = ('ball,junk,laser',tile_block,{'top':1,'left':1,'right':1,'bottom':1,'next':42,'enext':16,'explode':1,'pill':1})
tiles[42] = ('ball,junk,laser',tile_block,{'top':1,'left':1,'right':1,'bottom':1,'next':43,'enext':16,'explode':1,'pill':1})
tiles[43] = ('ball,junk,laser',tile_block,{'top':1,'left':1,'right':1,'bottom':1,'next':44,'enext':16,'explode':1,'pill':1})
tiles[44] = ('ball,junk,laser',tile_block,{'top':1,'left':1,'right':1,'bottom':1,'next':45,'enext':16,'explode':1,'pill':1})
tiles[45] = ('ball,junk,laser',tile_block,{'top':1,'left':1,'right':1,'bottom':1,'next':46,'enext':16,'explode':1,'pill':1})
tiles[46] = ('ball,junk,laser',tile_block,{'top':1,'left':1,'right':1,'bottom':1,'next':47,'enext':16,'explode':1,'pill':1})
tiles[47] = ('ball,junk,laser',tile_block,{'top':1,'left':1,'right':1,'bottom':1,'next':9,'enext':16,'explode':1,'pill':1})

tiles[48] = ('ball,junk,laser',tile_block,{'top':1,'left':1,'right':1,'bottom':1,'next':49,'enext':40,'explode':1,'pill':1})
tiles[49] = ('ball,junk,laser',tile_block,{'top':1,'left':1,'right':1,'bottom':1,'next':50,'enext':40,'explode':1,'pill':1})
tiles[50] = ('ball,junk,laser',tile_block,{'top':1,'left':1,'right':1,'bottom':1,'next':51,'enext':40,'explode':1,'pill':1})
tiles[51] = ('ball,junk,laser',tile_block,{'top':1,'left':1,'right':1,'bottom':1,'next':52,'enext':40,'explode':1,'pill':1})
tiles[52] = ('ball,junk,laser',tile_block,{'top':1,'left':1,'right':1,'bottom':1,'next':53,'enext':40,'explode':1,'pill':1})
tiles[53] = ('ball,junk,laser',tile_block,{'top':1,'left':1,'right':1,'bottom':1,'next':54,'enext':40,'explode':1,'pill':1})
tiles[54] = ('ball,junk,laser',tile_block,{'top':1,'left':1,'right':1,'bottom':1,'next':55,'enext':40,'explode':1,'pill':1})
tiles[55] = ('ball,junk,laser',tile_block,{'top':1,'left':1,'right':1,'bottom':1,'next':8,'enext':40,'explode':1,'pill':1})

def nothing_update(level,a,t):
	pass

class level(kjv):
	def load(self):
		f = open(self.level_fname)

		#load bkgr, music
		self.bkgr_fname = f.readline().strip()
		self.music_fname = f.readline().strip()

		f.readline()

		#load w,h
		w,h = f.readline().split()
		w,h = int(w),int(h)
		self.resize(w,h)

		f.readline()

		#load layer 0
		for y in range(0,self.h):
			vals = f.readline().split()
			#print y,vals
			for x in range(0,self.w):
				self.set(x,y,int(vals[x]))

		f.readline()

		#load clayer
		for y in range(0,self.h):
			vals = f.readline().split()
			for x in range(0,self.w):
				self.clayer[y][x] = int(vals[x])

		f.close()

	def save(self,fname=None):
		if fname == None:
			fname = self.level_fname
		f = open(fname,'w')

		f.write("%s\n" % self.bkgr_fname)
		f.write("%s\n" % self.music_fname)

		f.write("\n")

		#write w,h
		f.write("%d %d\n" % (self.w,self.h))

		f.write("\n")

		#write layer 0
		for y in range(0,self.h):
			vals = [str(self.layers[0][y][x]) for x in range(0,self.w)]
			f.write(" ".join(vals) + "\n")

		f.write("\n")

		#write clayer
		for y in range(0,self.h):
			vals = [str(self.clayer[y][x]) for x in range(0,self.w)]
			f.write(" ".join(vals) + "\n")

		f.close()

	def init(self):
		self.frame = 0

		l = self.layers[0]
		self.resize(24,36)

		xr = xrange(0,20)
		for y in xrange(0,30):
			for x in xr:
				self.layers[0][y+3][x+2]=l[y][x]

		xr = xrange(0,len(self.layers[0][0]))
		yr = xrange(0,len(self.layers[0]))

		for x in xr:
			self.layers[0][0][x] = 14
			self.layers[0][1][x] = 13
			self.layers[0][2][x] = 13
			self.layers[0][35][x] = 15

		for y in yr:
			self.layers[0][y][2] = 14
			self.layers[0][y][21] = 14



		self.origin.x = 64
		self.origin.y = 48

		level_init(self)

	def start(self):
		self.sprites = []
		self.listeners = {}

		self.string2groups('lives')
		self.showlives()
		self.string2groups('score')
		self.showscore()

		self.dead = 0

		self.balls = 0
		self.junks = 0
		self.lasers = 0
		#blocks are unchanged

		level = self
		p = player_new(level,self.origin.x+320-24,TH*30)
		level.listeners[p]=p
		b = ball_new(level,p.cur.centerx,p.cur.top,BALL_SPEED_START)
		b.cur.bottom = p.cur.top
		b.y = b.cur.y
		b.vx,b.vy = 0,-BALL_SPEED_START
		player_catch(level,p,b)

		self.loop_paint()

		game.pause("Get Ready","Level %d"%self.cur)

		self.sparkle()


	def showlives(self):
		for a in self.sprites[:]:
			if (a.groups & self.groups['lives']):
				self.sprites.remove(a)
		for i in range(0,self.lives-1):
			a = sprite(self.images['paddle.p.24'],self.origin.x+TW*(i+1)+8,self.origin.y+29.5*TH)
			a.x,a.y,a.groups,a.agroups = a.cur.x,a.cur.y,self.string2groups('lives'),0
			a.update = nothing_update
			self.add(a)

	def showscore(self):
		for a in self.sprites[:]:
			if (a.groups & self.groups['score']):
				self.sprites.remove(a)
		s = "%06d"%self.score
		img = game.fontsmall.render(s,1,game.colorscore)
		"""
		m1 = game.fontsmall.render(s,1,(255,255,255))
		m2 = game.fontsmall.render(s,1,(0,230,250))
		m3 = game.fontsmall.render(s,1,(0,0,0))
		img = pygame.Surface((m1.get_width()+2,m1.get_height()+2),SRCALPHA)
		img.blit(m3,(2,2))
		img.blit(m1,(0,0))
		img.blit(m2,(1,1))
		"""
		a = sprite(img,self.origin.x+TW*19-8-img.get_width(),self.origin.y)
		a.x,a.y,a.groups,a.agroups = a.cur.x,a.cur.y,self.groups['score'],0
		a.update = nothing_update
		self.add(a)


	def sparkle(self):
		for y in range(0,self.h):
			for x in range(0,self.w):
				n = self.get(x,y)
				if n == 6: n = 32
				if n == 8: n = 48
				self.set(x,y,n)



	def nextlevel(self):
		self.game.goto(level(self.game,self.level+1))

	def loop(self):
		#print self.junks,self.balls,self.blocks

		if self.scorev:
			self.score += self.scorev
			self.scorev -= 1
			self.showscore()

		if self.junks<3 and (self.frame%(40*3))==0: #(randrange(0,65536)%(40*3))==0:
			a = junk_new(self,randrange(2,21)*TW,1*TH)

		layer = self.layers[0]
		alayer = self.alayer
		clayer = self.clayer
		next = self.next
		lay2 = self.layers[2]
		tiles = self.tiles
		xr = xrange(0,len(layer[0]))
		yr = xrange(0,len(layer))

		#should already be reset
		for y in yr:
			for x in xr:
				alayer[y][x] = 0


		if self.frame % 1== 0:
			for y in yr:
				for x in xr:
					if alayer[y][x] == 0:
						n = layer[y][x]
						if next[n]!=n:
							layer[y][x]=next[n]
							if layer[y][x] == 0:
								self.blocks -= 1
								#if self.blocks == 0:
								#	self.nextlevel()
							alayer[y][x]=1



		if self.frame % 3 == 0:
			for y in yr:
				for x in xr:
					if alayer[y][x] != -1:
						if clayer[y][x] == -1:

							n = layer[y][x]
							t = tiles[n]
							c = t.config
							t.tx = x
							t.ty = y
							if c.get('explode',0) == 1:
								block_explode(self,t)
							elif c.get('enext',0) != 0:
								self.set(t.tx,t.ty,t.config['enext'])
							clayer[y][x] = 0




		kjv.loop(self)

		#pygame.time.delay(100)

		self.frame += 1

	def init_graphics(self,tiles_fname="tiles.png",alpha_fname="alpha.txt",bkgr_fname=None):
		self._carried = {}
		self._carries = {}

		if self.bkgr == None:
			if bkgr_fname == None and self.bkgr_fname != None:
				bkgr_fname = self.bkgr_fname
			if bkgr_fname != None:
				self.bkgr = pygame.image.load(bkgr_fname).convert()

		alphas = open(alpha_fname,"r")

		#img = pygame.image.load("tiles.png").convert()
		img = pygame.image.load("images/"+ tiles_fname)
		aimg = img.convert_alpha()
		oimg = img.convert()
	#	img.set_alpha(255,RLEACCEL)
		for y in range(0,16):
			for x in range(0,8):
				anum,atype = alphas.readline().strip().split()
				t = tile()
				#t.trans = TRANS_PARTIAL
				if atype == 'trans':
					t.image = None
				elif atype == 'opaque':
					t.image = oimg.subsurface((x*TW,y*TH,TW,TH))
				elif atype == 'mixed':
					t.image = aimg.subsurface((x*TW,y*TH,TW,TH))
				else:
					print 'uh no, no nothing?'
				#t.image = pygame.Surface((TW,TH))
				#t.image.blit(img.subsurface((x*TW,y*TH,TW,TH)),(0,0))
				#t.image.set_alpha(255,RLEACCEL)
				n = y*8+x
				t.agroups,t.hit,t.config = 0,None,{}
				agroups,hit,config = tiles[n]
				if agroups: t.agroups = self.string2groups(agroups)
				if hit: t.hit = hit
				if config: t.config = config
				t.anext = t.config.get('anext',n)
				t.aspeed = t.config.get('aspeed',1)
				if t.anext != n: t.animate = 1
				else: t.animate = 0
				#print t.animate,t.anext,t.aspeed
				t.cur = Rect((0,0,0,0))
				t.prev = t.cur
				self.tiles[n] = t

		level.codes = [None for n in range(0,256)]
		for n in range(0,256):
			if codes[n] != None:
				image,align,new,new_config,agroups,hit,config = codes[n]
				c = code()
				c.image = image
				c.align = align
				c.new = new
				c.new_config = new_config
				c.agroups = 0
				if agroups:
					c.agroups = self.string2groups(agroups)
				c.hit = hit
				c.config = config
				c.cur = Rect((0,0,0,0))
				c.prev = t.cur
				level.codes[n] = c
			#else:
			#	c = code()
			#	c.agroups = 0
			#	level.codes[n] = c

		iloader = {}

		for k in images.keys():
			fname,location,shape = images[k]
			if not fname in iloader: iloader[fname] = pygame.image.load("images/"+fname).convert_alpha()
			img = iloader[fname]
			e = sprite(img.subsurface(location),0,0)
			e.shape = Rect(shape)
			self.images[k] = e


		#generate the paddles
		for p in ['l','w','3','c','e','s','x','p']:
			img = self.images['paddles.%s'%p].image
			l,m,r = img.subsurface((0,0,6,6)),img.subsurface((6,0,6,6)),img.subsurface((12,0,6,6))
			for w in range(PADDLE_SMALL,PADDLE_LONGEST+1):
				img = pygame.Surface((w,6),SRCALPHA)
				img.blit(l,(0,0))
				img.blit(pygame.transform.scale(m,(w-12,6)),(6,0))
				img.blit(r,(w-6,0))
				e = sprite(img,0,0)
				e.shape = Rect(0,0,img.get_width(),img.get_height())
				self.images["paddle.%s.%d"%(p,w)] = e

		#self.fps = 10
		#self.speed = 0.25
		self.fps = 40
		self.speed = 1
		self.frame = 0

	#def loop_delay(self): pass

	def loop_update(self):
		#self.paint(self.screen)
		#pygame.display.flip()
		#return

		aas = self.sprites[:]
		for s in aas:
			#if s.cur.x != s.prev.x or s.cur.y != s.prev.y:
			s.updated=1 #not many sprites anyways.

		#if randrange(0,40)==0:
		u = self.update(self.screen)
		pygame.display.update(u)
		#return
		#print len(u)
		#if randrange(0,40)==0:
		#	self.paint(self.screen)
		#	pygame.display.flip()
		pygame.display.flip()
