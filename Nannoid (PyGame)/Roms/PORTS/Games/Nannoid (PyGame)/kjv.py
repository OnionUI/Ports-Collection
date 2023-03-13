import pygame
from pygame.locals import *
from tilevid import *
import math

TW,TH = 32,16

class actor(sprite):
	def __init__(self,image,x,y):
		sprite.__init__(self,image,x,y)
		self.x = x*1.0
		self.y = y*1.0
		self.groups = 0
		self.agroups = 0

class kjv(tilevid):
	def __init__(self):
		#self.game = game
		tilevid.__init__(self)
		self.listeners = {}
		self.groups = {}
		self.images = {}
		self.fps = 0.0
		self.speed = 1.0
		self.nt = 0.0
		#self.sprites = {}

#		self.updates = {}

	def init(self):
		self.paint(self.game.screen)
		pygame.display.flip()

	def string2groups(self,str):
		return self.list2groups(str.split(","))

	def list2groups(self,igroups):
		for s in igroups:
			if not s in self.groups:
				self.groups[s] = 2**len(self.groups)
		v = 0
		for s,n in self.groups.items():
			if s in igroups: v|=n
		return v

	def groups2list(self,groups):
		v = []
		for s,n in self.groups.items():
			if (n&groups)!=0: v.append(s)
		return v

#	def add(self,s):
#		tilevid.add(self,s)
#		if not s.updates in self.updates:
#			self.updates[s.updates] = []
#		self.updates[s.updates].append(s)

#	def remove(self,s):
#		tilevid.remove(self,s)
#		if s in self.updates[s.updates]:
#			self.updates[s.updates].remove(s)

	def event(self,e):
		for l in self.listeners:
			l.event(self,l,e)
		if e.type is QUIT:
			self.game.quit()

	def hit(self,x,y,t,s):
		tw,th = self.tilesize()
		#n = self.layers[0][y][x]
		#t = self.tiles[n]
		t.tx = x
		t.ty = y
		t.cur.x= x*tw
		t.cur.y = y*th
		t.cur.w=tw
		t.cur.h=th
		t.prev = t.cur
		#t.n = n
		if hasattr(t,'hit'):
			t.hit(self,t,s)


	def loop(self):
		self.loop_events()
		self.loop_spriteupdate()
		self.loop_tilehits()
		self.loop_spritehits()
		self.loop_delay()
		self.loop_update()

	def loop_delay(self):
		ft = 1000.0/self.fps
		if not self.nt:
			self.nt = float(pygame.time.get_ticks())
			self.nt += ft
		ct = pygame.time.get_ticks()
		if ct < self.nt:
			pygame.time.wait(int(self.nt-ct))
			self.nt += ft
		else:
			self.nt = float(ct) + ft

	def loop_events(self):
		for e in pygame.event.get():
			self.event(e)

	def loop_spriteupdate(self):
		ft = 1000.0/self.fps
		tt = ft*self.speed/1000.0
#		for u,as in self.updates.items(): u(self,as,tt)
		aas = self.sprites[:]
		for s in aas:
			curx = s.cur.x
			cury = s.cur.y
			s.update(self,s,tt)
			if curx != s.cur.x:
				s.x = s.cur.x
			if cury != s.cur.y:
				s.y = s.cur.y
			s.cur.x = s.x
			s.cur.y = s.y

	def loop_tilehits(self):
		tw,th = self.tilesize()

		tiles = self.tiles
		layer = self.layers[0]

		aas = self.sprites[:]
		for s in aas:
			if s.groups != 0:


				prev = s.prev
				cur = s.cur

				prevx = prev.x
				prevy = prev.y
				prevw = prev.w
				prevh = prev.h

				curx = cur.x
				cury = cur.y
				curw = cur.w
				curh = cur.h

				cur.y = prev.y
				cur.h = prev.h

				hits = []
				ct,cb,cl,cr = cur.top,cur.bottom,cur.left,cur.right
				#nasty ol loops
				y = ct/th*th
				while y < cb:
					x = cl/tw*tw
					yy = y/th
					while x < cr:
						xx = x/tw
						t = tiles[layer[yy][xx]]
						if (s.groups & t.agroups)!=0:
							"""
							t.tx = xx
							t.ty =yy
							t.cur.x= xx*tw
							t.cur.y = yy*th
							self.hit(xx,yy,t,s)
							#t.hit(self,t,s)
							"""
							hits.append((xx,yy))
						x += tw
					y += th

				bh = None
				bd = 256
				for h in hits:
					xx,yy=h
					d = math.hypot(cur.centerx-(xx*TW-TW/2),cur.centery-(yy*TH-TH/2))
					if d < bd: bd,bh = d,h
				if bh != None:
					xx,yy = h
					t = tiles[layer[yy][xx]]
					t.tx = xx
					t.ty =yy
					t.cur.x= xx*tw
					t.cur.y = yy*th
					self.hit(xx,yy,t,s)

				#switching directions...
				prev.x = cur.x
				prev.w = cur.w
				cur.y = cury
				cur.h = curh

				hits = []
				ct,cb,cl,cr = cur.top,cur.bottom,cur.left,cur.right
				#nasty ol loops
				y = ct/th*th
				while y < cb:
					x = cl/tw*tw
					yy = y/th
					while x < cr:
						xx = x/tw
						t = tiles[layer[yy][xx]]
						if (s.groups & t.agroups)!=0:
							"""
							t.tx = xx
							t.ty =yy
							t.cur.x= xx*tw
							t.cur.y = yy*th
							self.hit(xx,yy,t,s)
							#t.hit(self,t,s)
							"""
							hits.append((xx,yy))
						x += tw
					y += th

				#done with loops

				bh = None
				bd = 256
				for h in hits:
					xx,yy=h
					d = math.hypot(cur.centerx-(xx*TW-TW/2),cur.centery-(yy*TH-TH/2))
					if d < bd: bd,bh = d,h
				if bh != None:
					xx,yy = h
					t = tiles[layer[yy][xx]]
					t.tx = xx
					t.ty =yy
					t.cur.x= xx*tw
					t.cur.y = yy*th
					self.hit(xx,yy,t,s)

				prev.x = prevx
				prev.y = prevy

				if curx != cur.x:
					s.x = cur.x
				if cury != cur.y:
					s.y = cur.y

		for s in aas:
			s.cur.x = s.x
			s.cur.y = s.y


	def loop_spritehits(self):
		aas = self.sprites[:]
		
		groups = {}
		for n in range(0,31):
			groups[1<<n] = []
		for s in aas:
			g = s.groups
			n = 1
			while g:
				if (g&1)!=0: groups[n].append(s)
				g >>= 1
				n <<= 1
				
		for s in aas:
			if s.agroups!=0:
				g = s.agroups
				n = 1
				while g:
					if (g&1)!=0: 
						for b in groups[n]:	
							if s != b and (s.agroups & b.groups)!=0 and s.cur.colliderect(b.cur):
								scurx = s.cur.x
								scury = s.cur.y
								bcurx = b.cur.x
								bcury = b.cur.y
								s.hit(self,s,b)
								if scurx != s.cur.x:
									s.x = s.cur.x
								if scury != s.cur.y:
									s.y = s.cur.y
								if bcurx != b.cur.x:
									b.x = b.cur.x
								if bcury != b.cur.y:
									b.y = b.cur.y
					g >>= 1
					n <<= 1

		for s in aas:
			s.cur.x = s.x
			s.cur.y = s.y

	def loop_update(self):
		aas = self.sprites[:]
		for s in aas:
			if s.cur.x != s.prev.x or s.cur.y != s.prev.y:
				s.updated=1

		self.paint(self.screen)
		pygame.display.flip()

	def loop_paint(self):
		self.paint(self.screen)
		pygame.display.flip()

	#	self.game.screen.fill(0xffffffff)
	#	self.update(self.game.screen)

	#	self.paint(self.game.screen)
	#	pygame.display.flip()



