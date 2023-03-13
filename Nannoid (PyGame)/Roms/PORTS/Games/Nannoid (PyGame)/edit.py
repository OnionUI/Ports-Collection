from game import *

pygame.mouse.set_visible(1)

AX,AY = 0,0

lvl.bkgr_fname = 'images/bkgr1.jpg'
lvl.tiles_fname = 'images/tiles.png'
lvl.init_graphics()

import sys

if len(sys.argv) != 2:
    print "python edit.py fname.lvl"
    sys.exit()

fname = sys.argv[1]

cur = 0

if str(int(fname)) == fname:
	cur = int(fname)

fname = "levels/%d.lvl" % cur
lvl.level_fname = fname
lvl.load()

n = 0
quit = 0
while not quit:
    lvl.paint(screen)
    pygame.display.flip()
    for e in pygame.event.get():
	if e.type is QUIT:
	    quit = 1
	elif e.type is KEYDOWN:
	    if e.key == K_s:
		lvl.save()
	    elif e.key == K_l:
		lvl.load()
	    elif e.key == K_ESCAPE:
		quit = 1
	    elif e.key in range(K_0,K_9+1):
		n = e.key-K_0
		print n
	    elif e.key in range(K_a,K_f+1):
	    	n = e.key-K_a+10
		print n
	    elif e.key == K_PAGEDOWN:
	    	if cur:
			cur -= 1
			fname = "levels/%d.lvl" % cur
			print fname
			lvl.level_fname = fname
			lvl.load()
	    elif e.key == K_PAGEUP:
	    	if cur:
			cur += 1
			fname = "levels/%d.lvl" % cur
			print fname
			lvl.level_fname = fname
			lvl.load()

	elif e.type is MOUSEMOTION:
	    x,y = (e.pos[0]-AX)/TW,(e.pos[1]-AY)/TH
	    if e.buttons[0]!=0:
		lvl.set(x,y,n)
	elif e.type is MOUSEBUTTONDOWN:
	    x,y = (e.pos[0]-AX)/TW,(e.pos[1]-AY)/TH
	    if e.button==1:
		lvl.set(x,y,n)
	    elif e.button==3:
		n = lvl.get(x,y)


