from pygame.rect import *

class sprite:
	def __init__(self,init,x,y):
		self.cur = Rect((0,0,0,0))
		self.tvcur = Rect((0,0,0,0))

		if hasattr(init,'__class__') and init.__class__ == sprite:
			self.tosprite(init)
		else:
			self.image = init
		image = self.image
		
		w = image.get_width()
		h = image.get_height()
		self.cur = Rect(x,y,w,h)
		self.prev = Rect(x,y,w,h)

		self.xoff = 0
		self.yoff = 0
		self.tvcur = Rect(x,y,w,h)
		self.tvprev = Rect(x,y,w,h)
		self.active=0
		self.image=image
		self.updated=1
		
		#just for good measure
		if hasattr(init,'__class__') and init.__class__ == sprite:
			self.tosprite(init)

	def toimage(self,img):
		self.image = img
		#self.xoff = -s.shape.x
		#self.yoff = -s.shape.y
		#self.cur.w = s.shape.w
		#self.cur.h = s.shape.h
		self.tvcur.w = img.get_width()
		self.tvcur.h = img.get_height()
	
	def tosprite(self,s):
		self.image = s.image
		self.xoff = -s.shape.x
		self.yoff = -s.shape.y
		self.cur.w = s.shape.w
		self.cur.h = s.shape.h
		self.tvcur.w = s.image.get_width()
		self.tvcur.h = s.image.get_height()

class tile:
	def __init__(self):
		self.image=0

class tilevid:
	
	def __init__(self):
		self.sprites = [] #{}
		self.tiles = [None for x in range(0,4096)]
		self.bounds=None
		self.bkgr=None
		self.origin=Rect(0,0,0,0)
		self.porigin=Rect(0,0,0,0)
		self.resize(1,1)
		self.images = {}
		self.removed = []
		
	def set(self,x,y,v):
		if self.layers[0][y][x]!=v:
			self.layers[0][y][x]=v
			self.alayer[y][x]=1
		
	def get(self,x,y):
		return self.layers[0][y][x]
	
	def add(self,s):
		self.sprites.append(s) #[s] = s
		
	def remove(self,s):
		if s not in self.sprites: return
		self.sprites.remove(s) #del self.sprites[s]
		s.updated = 1
		self.removed.append(s)

	def resize(self,w,h):
		self.w=w
		self.h=h
		self.layers=[[[0 for x in range(0,self.w)] for y in range(0,self.h)] for l in range(0,5)]
		self.clayer = self.layers[3]
		self.alayer = self.layers[4]

	def tilesize(self):
		for t in self.tiles:
			if t != None and t.image != None:
				tw=t.image.get_width()
				th=t.image.get_height()
				return tw,th
		return 0,0 #will cause crash


	def paint(self,g):
		self.dobounds(g)
		
		tiles = self.tiles;
		layers = self.layers;
		alayer = self.alayer;
		sprites = self.sprites;
		origin = self.origin;

		gblit = g.blit
	
		#import pygame
		#surf = pygame.Surface((g.get_width(),g.get_height()))
		#gblit = surf.blit
		
		#if self.bkgr != None:
		#	gblit(self.bkgr,(0,0))

		ox = origin.x
		oy = origin.y

		bounds = self.bounds

		bkgr = self.bkgr
		bg = Rect(0,0,self.bkgr.get_width(),self.bkgr.get_height())
		if bounds.width > origin.width:
			bg.left = (bkgr.get_width()-g.get_width())*(origin.left-bounds.left)/(bounds.width-origin.width)
		if bounds.height > origin.height:
			bg.top = (bkgr.get_height()-g.get_height())*(origin.top-bounds.top)/(bounds.height-origin.height)

		tw,th = self.tilesize()
		w = g.get_width() / tw
		h = g.get_height() / th
		
		if g.get_width() % tw: w = w+1
		if g.get_height() % th: h = h+1
		#if origin.left % tw: w = w+1
		#if origin.top % th: h = h+1

		xi = ox/tw*tw
		yi = oy/th*th

		#print w,h
		#if xi+w*tw > self.w*tw: w = (self.w-xi/tw)
		#print xi,yi
		#if yi+h*th > self.h*th: h = (self.h-yi/th)
		#print w,h

		xf=ox+w*tw
		yf=oy+h*th
		yt=yi/th
		xr=xrange(xi-ox,xf-ox,tw)
		for y in xrange(yi-oy,yf-oy,th):
			xt = xi/tw
			alay = alayer[yt]
			lay0 = layers[0][yt]
			for x in xr:
				#t = tiles[lay0[xt]].image
				image = tiles[lay0[xt]].image
				if image == None:
					#print 'trans'
					gblit(self.bkgr,(x,y),(bg.left+x,bg.top+y,tw,th))
					pass
				else:
					if image.get_alpha() != None:
						#print 'mixed'
						gblit(self.bkgr,(x,y),(bg.left+x,bg.top+y,tw,th))
						#gblit(self.bkgr,(x,y),(x,y,tw,th))
						pass
					else:
						#print 'opaque'
						pass
					gblit(image,(x, y))

				#gblit(tiles[lay0[xt]].image,(x, y))
				alay[xt]=0
				xt += 1
			yt += 1

		for s in sprites:
			s.tvcur.x = s.cur.x+s.xoff
			s.tvcur.y = s.cur.y+s.yoff
			gblit(s.image,(s.tvcur.x - ox,s.tvcur.y - oy))
			s.updated=0
			s.tvprev.x = s.tvcur.x
			s.tvprev.y = s.tvcur.y
			s.tvprev.w = s.tvcur.w
			s.tvprev.h = s.tvcur.h

			s.prev.x = s.cur.x
			s.prev.y = s.cur.y
			s.prev.w = s.cur.w
			s.prev.h = s.cur.h

		#set porigin
		self.porigin.x = self.origin.x
		self.porigin.y = self.origin.y

		#g.blit(surf,(0,0))

		return ([Rect(0,0,g.get_width(),g.get_height())])

	def dobounds(self,g):
		tw,th = self.tilesize()
		if self.bounds == None:
			self.bounds = Rect(0,0,self.w*tw,self.h*th)

		tiles,origin,bounds = self.tiles,self.origin,self.bounds
		if origin.left < bounds.left: origin.left = bounds.left
		if origin.top < bounds.top: origin.top = bounds.top
		origin.w = g.get_width()
		origin.h = g.get_height()
		if origin.right > bounds.right: origin.right = bounds.right
		if origin.bottom > bounds.bottom: origin.bottom = bounds.bottom

	def update(self,g):
		self.dobounds(g)
		
		tiles = self.tiles;
		layers = self.layers
		alayer = self.alayer
		sprites = self.sprites;
		origin = self.origin;
		gblit = g.blit

		#if self.bkgr != None:
		#	return self.paint(g)

		if self.origin.x != self.porigin.x or self.origin.y != self.porigin.y:
			return self.paint(g)

		ox = origin.x
		oy = origin.y

		bounds = self.bounds
		bkgr = self.bkgr
		bg = Rect(0,0,self.bkgr.get_width(),self.bkgr.get_height())
		if bounds.width > origin.width:
			bg.left = (bkgr.get_width()-g.get_width())*(origin.left-bounds.left)/(bounds.width-origin.width)
		if bounds.height > origin.height:
			bg.top = (bkgr.get_height()-g.get_height())*(origin.top-bounds.top)/(bounds.height-origin.height)


		tw,th = self.tilesize()
		w = g.get_width() / tw
		h = g.get_height() / th

		if g.get_width() % tw: w = w+1
		if g.get_height() % th: h = h+1
		#if origin.left % tw: w = w+1
		#if origin.top % th: h = h+1

		#mark places where sprites have moved, or been removed
		aas = self.removed
		self.removed = []
		aas.extend(sprites)
		for s in aas: #sprites:
			s.tvcur.x = s.cur.x+s.xoff
			s.tvcur.y = s.cur.y+s.yoff
			if s.updated:
				r = s.tvprev
				y = r.y/th
				while y < r.bottom/th+1:
					x = r.x/tw
					while x < r.right/tw+1:
						alayer[y][x]=1
						x += 1
					y += 1

				r = s.tvcur
				y = r.y/th
				while y < r.bottom/th+1:
					x = r.x/tw
					while x < r.right/tw+1:
						if alayer[y][x]==0:
							alayer[y][x]=2
						x += 1
					y += 1

		#mark sprites that are not being updated that need to be updated because
		#they are being overwritte by sprites / tiles
		for s in sprites:
			if s.updated==0:
				r = s.tvcur
				y = r.y/th
				while y < r.bottom/th+1:
					x = r.x/tw
					while x < r.right/tw+1:
						if alayer[y][x]==1:
							s.updated=1
						x += 1
					y += 1
	
		#display tiles
		updates = []
		uappend = updates.append
		xi = origin.x/tw*tw
		yi = origin.y/th*th
		xf=origin.x+w*tw
		yf=origin.y+h*th
		yt=yi/th
		xr=xrange(xi-ox,xf-ox,tw)
		for y in xrange(yi-oy,yf-oy,th):
			xt = xi/tw
			us = -1
			alay = alayer[yt]
			lay0 = layers[0][yt]

			for x in xr:
				if alay[xt]==1:
					if us == -1:
						us = x
						ue = 0
					#gblit(tiles[lay0[xt]].image,(x, y))
					image = tiles[lay0[xt]].image
					if image == None:
						#print 'trans'
						gblit(self.bkgr,(x,y),(bg.left+x,bg.top+y,tw,th))
						pass
					else:
						if image.get_alpha() != None:
							#print 'mixed'
							gblit(self.bkgr,(x,y),(bg.left+x,bg.top+y,tw,th))
							#gblit(self.bkgr,(x,y),(x,y,tw,th))
							pass
						else:
							#print 'opaque'
							pass
						gblit(image,(x, y))

					#gblit(tiles[lay0[xt]].image,(x, y))
					#alay[xt]=0
					#xt += 1


					alay[xt]=0
					ue += tw
				elif alay[xt]==2:
					if us == -1:
						us = x
						ue = 0
					alay[xt]=0
					ue += tw
				else:
					if us != -1:
						uappend(Rect(us,y,ue,th))
						us = -1
				xt += 1
			if us!=-1:
				uappend(Rect(us,y,ue,th))
			yt += 1

		#display sprites
		for s in sprites:
			if s.updated:
				gblit(s.image,(s.tvcur.x - origin.x, s.tvcur.y - origin.y))
				s.updated=0
				s.tvprev.x = s.tvcur.x
				s.tvprev.y = s.tvcur.y
				s.tvprev.w = s.tvcur.w
				s.tvprev.h = s.tvcur.h
				
				s.prev.x = s.cur.x
				s.prev.y = s.cur.y
				s.prev.w = s.cur.w
				s.prev.h = s.cur.h
		
		#return updates, heh.
		return updates
