from math import sqrt
import pygame
from random import seed, randint

class vector:
	def __init__(self,x = 0,y=0):
		self.x = x
		self.y = y

	def xy(self):
		return (self.x,self.y)

	def __str__(self):
		return "(%s,%s)" %(self.x,self.y)

	def get_magnitude(self):
		return sqrt(self.x**2 + self.y**2)

	def normalize(self):
		if self.x == 0 and self.y == 0:
			return
		magnitude = self.get_magnitude()
		self.x /= magnitude
		self.y /= magnitude

	def __add__(self,rhs):
		return vector(self.x+rhs.x,self.y+rhs.y)

	def __sub__(self,rhs):
		return vector(self.x - rhs.x, self.y - rhs.y)

	def __mul__(self,scalar):
		return vector(self.x*scalar,self.y*scalar)

	def __div__(self,scalar):
		return vector(self.x / scalar, self.y / scalar)

class Arrow(pygame.sprite.Sprite):
                def __init__(self):
                        pygame.sprite.Sprite.__init__(self)
                        self.image = pygame.image.load("arrow.png").convert_alpha()
                        self.rect = self.image.get_rect()
                        self.cords = vector(190,240)
                        self.rect.topleft = self.cords.xy()

                def update(self,option):
                        if option == 1: self.cords.y = 240
                        if option == 2: self.cords.y = 280
                        if option == 3: self.cords.y = 320
                        self.rect.topleft = self.cords.xy()

class Man_No_Sheild(pygame.sprite.Sprite):
                def __init__(self,x,y):
                        pygame.sprite.Sprite.__init__(self)
                        self.image = pygame.image.load('man_no_sheild.png').convert_alpha()
                        self.rect = self.image.get_rect()
                        self.cords = vector(x,y)
                        self.rect.midbottom = self.cords.xy()
                        self.direction = vector(0,0)
                        self.alive = True
                        self.speed = 350

                def update(self,time):
                        if self.cords.x < 5: self.cords.x = 495
                        if self.cords.x > 495: self.cords.x = 5
                        if self.alive == False: self.kill()
                        self.cords += self.direction*self.speed*time
                        self.rect.midbottom = self.cords.xy()

class Man(pygame.sprite.Sprite):
                def __init__(self,x,y):
                        pygame.sprite.Sprite.__init__(self)
                        self.image = pygame.image.load('man.png').convert_alpha()
                        self.rect = self.image.get_rect()
                        self.cords = vector(x,y)
                        self.rect.midbottom = self.cords.xy()
                        self.direction = vector(0,0)
                        self.alive = True
                        self.speed = 350

                def update(self,time):
                        if self.cords.x < 20: self.cords.x = 480
                        if self.cords.x > 480: self.cords.x = 20
                        if self.alive == False: self.kill()
                        self.cords += self.direction*self.speed*time
                        self.rect.midbottom = self.cords.xy()

class Icicle(pygame.sprite.Sprite):
                def __init__(self):
                        pygame.sprite.Sprite.__init__(self)
                        self.image = pygame.image.load('icicle.png').convert_alpha()
                        self.rect = self.image.get_rect()
                        self.cords = vector(randint(0,485),randint(-400,-30))
                        self.rect.topleft = self.cords.xy()
                        self.direction = vector(0,1)
                        self.alive = True
                        self.speed = randint(100,150)
                        self.acceleration = randint(10,80)

                def update(self,time,wind):
                        if self.cords.x < 5: self.cords.x = 490
                        if self.cords.x > 490: self.cords.x = 5
                        if self.alive == False: self.kill()
                        if self.cords.y > 0: self.speed += .20 * self.acceleration
                        self.direction  = vector(wind,1)
                        self.direction.normalize()
                        self.cords += self.direction*self.speed*time
                        self.rect.midbottom = self.cords.xy()

class Particle(pygame.sprite.Sprite):
                def __init__(self,x,y,intensity,life,speed,image):
                        pygame.sprite.Sprite.__init__(self)
                        self.image = pygame.image.load(image).convert_alpha()
                        self.rect = self.image.get_rect()
                        self.cords = vector(x,y)
                        self.rect.center = self.cords.xy()
                        self.dx = randint(intensity[0][0],intensity[0][1]) / intensity[0][2]
                        self.dy = randint(intensity[1][0],intensity[1][1]) / intensity[1][2]
                        self.direction = vector(self.dx,self.dy)
                        self.direction.normalize()
                        self.life = randint(life[0],life[1])
                        self.speed = randint(speed[0],speed[1])

                def update(self,time):
                        self.life -= 1
                        self.cords += self.direction*self.speed * time
                        self.cords.y += .3*(18 - self.life)
                        self.rect.center = self.cords.xy()
                        if self.life == 0: self.kill()

class Explosion(pygame.sprite.Sprite):
                def __init__(self,x,y,number,intensity,life,speed,image):
                        pygame.sprite.Sprite.__init__(self)
                        self.container = pygame.sprite.RenderUpdates()
                        for z in range(number):
                                self.container.add(Particle(x,y,intensity,life,speed,image))

                def update(self,time,root,bg):
                        self.container.clear(root,bg)
                        self.container.update(time)
                        self.container.draw(root)
                        if self.container == []:
                                self.kill()

class Oneup(pygame.sprite.Sprite):
                def __init__(self):
                        pygame.sprite.Sprite.__init__(self)
                        self.image = pygame.image.load('heart.png').convert_alpha()
                        self.rect = self.image.get_rect()
                        self.cords = vector(randint(0,485),randint(-150,-30))
                        self.rect.center = self.cords.xy()
                        self.direction = vector(0,1)
                        self.alive = True
                        self.speed = randint(90,100)

                def update(self,time):
                        if self.cords.y > 465: self.alive = False
                        if self.alive == False: self.kill()
                        self.cords += self.direction*self.speed*time
                        self.rect.center = self.cords.xy()

class Shield(pygame.sprite.Sprite):
                def __init__(self):
                        pygame.sprite.Sprite.__init__(self)
                        self.image = pygame.image.load('shield.png').convert_alpha()
                        self.rect = self.image.get_rect()
                        self.cords = vector(randint(0,485),randint(-150,-30))
                        self.rect.center = self.cords.xy()
                        self.direction = vector(0,1)
                        self.alive = True
                        self.speed = randint(90,100)

                def update(self,time):
                        if self.cords.y > 465: self.alive = False
                        if self.alive == False: self.kill()
                        self.cords += self.direction*self.speed*time
                        self.rect.center = self.cords.xy()

class Bomb(pygame.sprite.Sprite):
                def __init__(self):
                        pygame.sprite.Sprite.__init__(self)
                        self.image = pygame.image.load('bomb.png').convert_alpha()
                        self.rect = self.image.get_rect()
                        self.cords = vector(randint(0,485),440)
                        self.rect.midtop = self.cords.xy()
                        self.direction = vector(0,0)
                        self.alive = True

                def update(self,time):
                        if self.alive == False: self.kill()
                        self.rect.midtop = self.cords.xy()

