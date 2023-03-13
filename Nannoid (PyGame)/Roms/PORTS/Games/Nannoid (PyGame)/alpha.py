import pygame 
from pygame.locals import *
#from game import game

pygame.init()

TW,TH = 32,16
import sys

img = pygame.image.load(sys.argv[1])
for y in range(0,16):
	for x in range(0,8):
		n = y*8+x
		tile = img.subsurface((x*TW,y*TH,TW,TH))
		alpha = 0
		opaque = 0
		for yy in range(0,TH):
			for xx in range(0,TW):
				p = tile.get_at((xx,yy))
				if p[3] != 255: alpha += 1
				if p[3] != 0: opaque += 1
		if alpha == 0:
			print n,'opaque'
		elif opaque == 0:
			print n,'trans'
		else:
			print n,'mixed'

