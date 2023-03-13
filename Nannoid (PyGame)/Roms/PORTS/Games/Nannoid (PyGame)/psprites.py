
sprites = {
	#'paddle.png':[''],
	#'paddle2.png':[''],
	#'paddlel.png':[''],
	#'paddlem.png':[''],
	#'paddler.png':[''],
	'ball.png':[''],
	'pills.png':['l','w','3','c','e','s','x','p'],
	'paddles.png':['l','w','3','c','e','s','x','p'],
	'pyramid.png':['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16'],
	'sphere.png':['1','2','3','4','5','6','7','8','9','10',
		'11','12','13','14','15','16','17','18','19','20',
		'21','22','23','24',#'25','26','27','28','29','30',
		],
	'cubes.png':[
		'1','2','3','4','5','6','7','8','9','10',
		'11','12','13','14','15','16','17','18','19','20',
		'21','22','23','24','25','26','27','28','29','30',
		'31','32','33','34','35','36','37','38','39','40',
		'41','42','43','44','45','46','47','48',
		],
	'boom.png':['1','2','3','4','5','6','7','8'],
	'laser.png':[''],
	}

import pygame 
from pygame.locals import *
#from game import game

pygame.display.init()

print "images = {}"

for fname in sprites.keys():
	parts = sprites[fname]
	dname,ext = fname.split(".")
	img = pygame.image.load(fname)
	w = img.get_width()/(len(parts)+1)
	h = img.get_height()

	minx,miny,maxx,maxy = w,h,0,0

	for y in range(0,h):
		for x in range(0,w):
			c = img.get_at((x,y))
			if c[1] > 128:
				if x < minx: minx = x
				if y < miny: miny = y
				if x > maxx: maxx = x
				if y > maxy: maxy = y
	
	ww = maxx-minx+1
	hh = maxy-miny+1
	
	n = 1
	for p in parts:
		name = dname
		if p != '': name = "%s.%s" % (dname,p)
		print "images[\'%s\']=('%s',(%d,%d,%d,%d),(%d,%d,%d,%d))" % (name, fname, n*w,0,w,h, minx,miny,ww,hh)
		n += 1

	
	
