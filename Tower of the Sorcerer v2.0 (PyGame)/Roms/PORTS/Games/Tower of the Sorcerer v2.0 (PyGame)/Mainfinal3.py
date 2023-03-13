# -*- coding: cp936 -*-
import pygame

# all the objects
class Basic(pygame.sprite.Sprite):
    def __init__(self,screen,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.x = 32*x
        self.y = 32*y

    def getY(self):
        return self.y

    def getX(self):
        return self.x

    def setX(self,x):
        self.x = 32*x

    def setY(self,y):
        self.y = 32*y
	
    def update(self):
	self.rect.topleft = ( self.x, self.y )
        
class Player(Basic):
    def __init__(self,screen,x,y):
        Basic.__init__(self,screen,x,y)
        self.imageList = []
        for a in range (8):
	    self.imageList.append( pygame.image.load("./image/player/player"+str(a)+".png"))
        
        self.__anime_index = 0
	self.__animetimer = 0
	
	self.image = self.imageList[self.__anime_index]
	self.rect = self.image.get_rect()
	self.rect.topleft = ( self.x, self.y )
	
        self.__hp = 1
        self.__atk = 5
        self.__def = 8
	self.__yellow_key = 1
	self.__blue_key = 0
	
    def change_image(self, index):
	self.__anime_index = index

    """data update functions"""
    def atk_update(self,n):
        self.__atk += n
    
    def hp_update(self,b):
        self.__hp += b
    
    def def_update(self,d):
        self.__def += d
    
    def ykey_update(self,a):
	self.__yellow_key += a

    def bkey_update(self,a):
	self.__blue_key += a

    def sethp(self, a):
        self.__hp = a
	
    """data accessor functions"""
    def getatk(self):
        return self.__atk

    def gethp(self):
        return self.__hp
    
    def getdef(self):
        return self.__def
    
    def getYkey(self):
        return self.__yellow_key
    
    def getBkey(self):
        return self.__blue_key
    
    def update( self ):
	self.__animetimer += 1
	
	if self.__animetimer == 15:
	    if self.__anime_index % 2 == 0:
		self.__anime_index += 1
	    else:
		self.__anime_index -= 1
	    
	    self.__animetimer = 0
	self.image = self.imageList[self.__anime_index]
	self.rect = self.image.get_rect()
	
	self.rect.topleft = ( self.x, self.y )

class Pickups(Basic):
    def __init__(self,screen, x, y, item_type):
	#redgem r bluegem b yellowkey k  bluekey  K  bluepotion  B   redpotion  R   sword w  shield h
    
	Basic.__init__(self,screen,x,y)
  ##        self.image = Surface((16, 16))
  ##        self.image.convert()
  ##        self.image.fill(Color("#FF0000"))
	self.__type = item_type
	imageList = ['redgem',"bluegem", "yellowkey", "bluekey","bluepotion","redpotion","sword","shield"]
	self.image = pygame.image.load("./image/"+ imageList[self.__type]+".png")
	self.rect = self.image.get_rect()
	self.rect.topleft = ( self.x, self.y )
    
    def get_type(self):
        return self.__type

            
class Monster(Basic):
    def __init__(self,screen, x, y, monster_type):
        Basic.__init__(self,screen,x,y)
        imageList = ["redslime","skeletonwithsword","royalguard","boss"]
        self.__type = monster_type
        self.image = pygame.image.load("./image/monster/"+ imageList[self.__type]+".png")  
##        self.image = Surface((16, 16))
##        self.image.convert()
##        self.image.fill(Color("#FF0000"))
        self.rect = self.image.get_rect()
	self.rect.topleft = ( self.x, self.y )

        #list of monster's data
        self.hp_list = [220,650,1100,15000]
        self.atk_list = [25,140,400,500]
        self.def_list = [8,50,160,450]
##      goldgive_list = [3,4,6,15,40,8,18,13,42,50,75,300,10000]
        
        self.__hp = self.hp_list[monster_type]
        self.__def = self.def_list[monster_type]
        self.__atk = self.atk_list[monster_type]

    def get_type(self):
        return self.__type

    def getatk(self):
        return self.__atk

    def gethp(self):
        return self.__hp

    def getdef(self):
        return self.__def

class Wall(Basic):
    def __init__(self, screen, x, y):#,colour, width, height'''
	Basic.__init__(self,screen,x,y)
	self.image = pygame.image.load("./image/wall.gif")
  ##	 self.__image = pygame.image.load('')#load the image later
  ##	 self.__image = scale_img(20, 20, self.image)
        self.rect = self.image.get_rect()
	self.rect.topleft = ( self.x, self.y )
	
class Door(Basic):
    def __init__(self, screen, x, y, door_type):#, width, height'''
	Basic.__init__(self,screen,x,y)
	self.imageList = [[],[]]
	for a in range (4):
	    self.imageList[0].append( pygame.image.load("./image/door/door"+str(a)+".png"))
        for a in range (4):
	    self.imageList[1].append( pygame.image.load("./image/door/doorb"+str(a)+".png"))
	
	self.__type = door_type
	self.__animeindex = 0
	self.__animetimer = 0
	self.__open = False
	self.image = self.imageList[self.__type][self.__animeindex]
	self.rect = self.image.get_rect()
	self.rect.topleft = ( self.x, self.y )

    def opens( self ):
	self.__open = True
    
    def update( self ):
	self.rect.topleft = ( self.x, self.y )
	
	if self.__open:
	    self.__animetimer += 1
	    if self.__animetimer % 5 == 0:
		self.__animeindex += 1
		self.image = self.imageList[self.__type][self.__animeindex]
		self.rect = self.image.get_rect()
		self.rect.topleft = ( self.x, self.y )
		if self.__animetimer == 15:
		    self.kill()
            
class Stairs(Basic):
    def __init__(self, screen,x, y, stair_type):#,colour, width, height'''
        Basic.__init__(self,screen,x,y)
        imageList = ["stairup", "stairdown"]
        self.__type = stair_type
        self.image = pygame.image.load("./image/"+ imageList[self.__type] +".png")
        self.rect = self.image.get_rect()
	self.rect.topleft = ( self.x, self.y )
	
    def get_type( self ):
	return self.__type
	
class Hp_keeper(pygame.sprite.Sprite):
    def __init__(self,screen,player):

        pygame.sprite.Sprite.__init__(self)

        self.__font = pygame.font.Font("./font/PittoresqJugendstil.ttf", 18)
        self.__screen = screen

        self.__hp = player.gethp()

    def sethp(self,player):
        self.__hp = player.gethp()

    def update(self):
        message = str(self.__hp)
        self.image = self.__font.render(message,1,(255,255,255))
        self.rect = self.image.get_rect()
        self.rect.center =(578,362)#center position


class Atk_keeper(pygame.sprite.Sprite):
    def __init__(self,screen,player):

        pygame.sprite.Sprite.__init__(self)

        self.__font = pygame.font.Font("./font/PittoresqJugendstil.ttf", 18)
        self.__screen = screen

        self.__atk = player.getatk()

    def setatk(self,player):
        self.__atk = player.getatk()
        
    def update(self):
        message = str(self.__atk)
        self.image = self.__font.render(message,1,(255,255,255))
        self.rect = self.image.get_rect()
        self.rect.center =(578,386)#center position

class Def_keeper(pygame.sprite.Sprite):
    def __init__(self,screen,player):

        pygame.sprite.Sprite.__init__(self)

        self.__font = pygame.font.Font("./font/PittoresqJugendstil.ttf", 18)
        self.__screen = screen

        self.__def = player.getdef()

    def setdef(self,player):
        self.__def = player.getdef()
        

    def update(self):
        message = str(self.__def)
        self.image = self.__font.render(message,1,(255,255,255))
        self.rect = self.image.get_rect()
        self.rect.center =(578,410)#center position

class Ykey_keeper(pygame.sprite.Sprite):
    def __init__(self,screen,player):

        pygame.sprite.Sprite.__init__(self)

        self.__font = pygame.font.Font("./font/PittoresqJugendstil.ttf", 19)
        self.__screen = screen

        self.__ykey = player.getYkey()

    def setykey(self,player):
        self.__ykey = player.getYkey()

    def update(self):
        message = "Yellow Keys #: "+str(self.__ykey)
        self.image = self.__font.render(message,1,(255,255,255))
        self.rect = self.image.get_rect()
        self.rect.center =(559,66)#center position

class Bkey_keeper(pygame.sprite.Sprite):
    def __init__(self,screen,player):

        pygame.sprite.Sprite.__init__(self)

        self.__font = pygame.font.Font("./font/PittoresqJugendstil.ttf", 19)
        self.__screen = screen

        self.__bkey = player.getBkey()

    def setbkey(self,player):
        self.__bkey = player.getBkey()

    def update(self):
        message = "Blue Keys #: "+str(self.__bkey)
        self.image = self.__font.render(message,1,(255,255,255))
        self.rect = self.image.get_rect()
        self.rect.center =(559,123)#center position

class Background(pygame.sprite.Sprite):
    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)
        self.__screen = screen
        
        #Set the image and rect attributes for the sky background
        self.image = pygame.image.load('./image/background.png')
        self.image = self.image.convert()
        self.rect = self.image.get_rect()

class instruction(pygame.sprite.Sprite):
    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)
        self.__screen = screen
        
        #Set the image and rect attributes for the sky background
        self.image = pygame.image.load('./image/instruction.jpg')
        self.image = self.image.convert()
        self.rect = self.image.get_rect()

class congratulation(pygame.sprite.Sprite):
    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)
        self.__screen = screen
        
        #Set the image and rect attributes for the sky background
        self.image = pygame.image.load('./image/congs.jpg')
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
