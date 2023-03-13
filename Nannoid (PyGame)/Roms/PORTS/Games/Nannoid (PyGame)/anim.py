import os,sys
import Image

w,h = 32,32
n =  int(sys.argv[1])
x = 0
out = Image.new('RGBA',(w*(n+1),h))
img = Image.open('green.png')
out.paste(img,(x,0))
x+=w
for i in range(1,n+1):
	fname = '%04d'%i
	img = Image.open(fname)
	out.paste(img,(x,0))
	x+=w
out.save('anim.png')


