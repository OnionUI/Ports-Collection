#I - IMPORT AND INITIALIZE
import pygame, random, Mainfinal3,sys,time
from pygame import *
pygame.init() 
screen = pygame.display.set_mode((640, 480))
def instruction():
    """This is the instrction screen for the game."""

    # DISPLAY
    pygame.display.set_caption("Tower of the Sorcerer V2.0") 
    
    
    
    # ENTITIES
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((255, 255, 255))
    pygame.mixer.music.load('./sound/instruc.wav')
    pygame.mixer.music.set_volume(0.5)    
    pygame.mixer.music.play(-1)

    # create a background of the instruction
    instruction = Mainfinal3.instruction( screen )
    insgroup = pygame.sprite.Group()
    
    #Display the instrction
    instructionfont = pygame.font.Font("./font/PittoresqJugendstil.ttf", 25)
    message = ('                       T o w e r  o f  t h e  S o r c e r e r  V2.0',\
               '                              Developed by:',\
               '                                 Yicheng Chen           ',\
               '                                 W e i y u a n  B a o           ',\
               'SPECIAL thx to my pro cs friend---- Edward Tan          ',\
               'Hope U will get to university of waterloo next year as u wish !!!          ',\
               '                                           ',\
               '      You are a worrior to fight with the darkness,',\
               'You will get stats rewards if U kill those monsters',\
               "Press 'u p', 'd o w n', 'l e f t', 'r i g h t' to control up, down,",\
               "left, and right",\
               "(Press E N T E R ! ! ! to continue when you are ready to fight)")
    instructiontxtlist = []
    for line in message:
        temp = instructionfont.render(line,1,(255,255,255))
        instructiontxtlist.append(temp)
    
    # ASSIGN
    clock = pygame.time.Clock()
    keepGoing = True
    
    insgroup.add(instruction)
    
    # LOOP
    while keepGoing:
    # TIME 
        clock.tick(30) 
        
        # EVENT HANDLING: Player uses arrow keys 
        for event in pygame.event.get():
            if event.type == pygame.QUIT\
               or (event.type == pygame.KEYDOWN\
                  and event.key == pygame.K_ESCAPE):
                    display.quit()
                    sys.exit()
                
            elif event.type == pygame.KEYDOWN: 
              keepGoing = False
        
##        for i in range(len(instructiontxtlist)):
##        screen.blit(instructiontxtlist[i],(50,35*i+20))
        insgroup.clear(screen, background)
        insgroup.draw(screen)
        for i in range(len(instructiontxtlist)):
            screen.blit(instructiontxtlist[i],(50,35*i+20))
        
        
        pygame.display.flip()
    insgroup.clear(screen, background)
    try:
        try:
            game()
        except:
            game()
    except:
        game()

def game():
    
    # DISPLAY
    pygame.display.set_caption("Tower of the Sorcerer V2.0") 
    
    # ENTITIES
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((255, 255, 255))
    
    # create a map of the dungeon
    dungeon = Mainfinal3.Background( screen )
    
    dungeon_map = [[[ 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 ],\
        [ 2 , 3 , 7 , 13 , 7 , 14 , 13 , 12 , 11 , 2 , 12 , 2 , 5 , 13 , 2 ],\
        [ 2 , 14 , 13 , 13 , 2 , 13 , 5 , 13 , 12 , 2 , 5 , 7 , 12 , 14 , 2 ],\
        [ 2 , 13 , 9 , 12 , 2 , 13 , 2 , 2 , 2 , 2 , 13 , 14 , 13 , 13 , 2 ],\
        [ 2 , 11 , 12 , 9 , 2 , 5 , 2 , 12 , 13 , 7 , 13 , 2 , 13 , 9 , 2 ],\
        [ 2 , 2 , 2 , 2 , 2 , 7 , 2 , 13 , 14 , 2 , 2 , 2 , 12 , 9 , 2 ],\
        [ 2 , 12 , 7 , 13 , 12 , 13 , 2 , 0 , 13 , 2 , 11 , 2 , 13 , 14 , 2 ],\
        [ 2 , 13 , 2 , 2 , 12 , 5 , 2 , 9 , 14 , 2 , 14 , 2 , 14 , 7 , 2 ],\
        [ 2 , 14 , 2 , 2 , 5 , 2 , 2 , 0 , 12 , 2 , 11 , 2 , 13 , 13 , 2 ],\
        [ 2 , 5 , 5 , 2 , 10 , 7 , 12 , 13 , 14 , 7 , 13 , 2 , 14 , 14 , 2 ],\
        [ 2 , 13 , 13 , 2 , 13 , 2 , 13 , 13 , 13 , 2 , 14 , 2 , 13 , 11 , 2 ],\
        [ 2 , 10 , 9 , 2 , 11 , 2 , 9 , 13 , 13 , 2 , 10 , 2 , 9 , 10 , 2 ],\
        [ 2 , 2 , 2 , 2 , 2 , 2 , 13 , 12 , 14 , 2 , 13 , 2 , 2 , 2 , 2 ],\
        [ 2 , 1 , 11 , 11 , 9 , 10 , 13 , 13 , 5 , 2 , 14 , 15 , 6 , 6 , 2 ],\
        [ 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 ]],\
        [\
        [ 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 ],\
        [ 2 , 11 , 14 , 14 , 2 , 12 , 2 , 12 , 2 , 12 , 7 , 10 , 8 , 3 , 2 ],\
        [ 2 , 12 , 2 , 13 , 2 , 13 , 2 , 5 , 2 , 10 , 2 , 13 , 7 , 0 , 2 ],\
        [ 2 , 12 , 2 , 14 , 2 , 14 , 13 , 13 , 10 , 10 , 2 , 14 , 2 , 14 , 2 ],\
        [ 2 , 14 , 2 , 13 , 2 , 12 , 2 , 2 , 2 , 5 , 2 , 10 , 2 , 9 , 2 ],\
        [ 2 , 13 , 2 , 14 , 2 , 12 , 2 , 4 , 13 , 0 , 2 , 10 , 2 , 9 , 2 ],\
        [ 2 , 13 , 2 , 10 , 2 , 13 , 2 , 2 , 2 , 8 , 2 , 9 , 2 , 13 , 2 ],\
        [ 2 , 13 , 2 , 12 , 2 , 13 , 2 , 9 , 2 , 9 , 2 , 9 , 2 , 9 , 2 ],\
        [ 2 , 13 , 2 , 14 , 2 , 12 , 2 , 13 , 2 , 9 , 2 , 10 , 2 , 14 , 2 ],\
        [ 2 , 13 , 2 , 14 , 13 , 13 , 2 , 13 , 2 , 2 , 2 , 2 , 2 , 13 , 2 ],\
        [ 2 , 12 , 2 , 11 , 2 , 13 , 7 , 5 , 2 , 12 , 11 , 13 , 7 , 13 , 2 ],\
        [ 2 , 14 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 7 , 2 , 14 , 2 , 5 , 2 ],\
        [ 2 , 10 , 5 , 14 , 13 , 14 , 0 , 2 , 5 , 13 , 2 , 2 , 2 , 2 , 2 ],\
        [ 2 , 10 , 12 , 2 , 10 , 9 , 13 , 14 , 14 , 5 , 5 , 9 , 13 , 11 , 2 ],\
        [ 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 ]],\
        [\
        [ 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 ],\
        [ 2 , 3 , 12 , 2 , 2 , 2 , 2 , 2 , 2 , 9 , 11 , 10 , 14 , 12 , 2 ],\
        [ 2 , 0 , 13 , 2 , 2 , 2 , 2 , 2 , 9 , 2 , 9 , 15 , 2 , 5 , 2 ],\
        [ 2 , 15 , 8 , 2 , 2 , 2 , 2 , 9 , 12 , 14 , 2 , 9 , 2 , 10 , 2 ],\
        [ 2 , 14 , 7 , 2 , 2 , 2 , 12 , 5 , 2 , 14 , 14 , 2 , 2 , 9 , 2 ],\
        [ 2 , 13 , 7 , 2 , 2 , 12 , 13 , 2 , 9 , 2 , 13 , 2 , 2 , 8 , 2 ],\
        [ 2 , 14 , 0 , 2 , 13 , 13 , 2 , 13 , 6 , 2 , 0 , 13 , 13 , 13 , 2 ],\
        [ 2 , 13 , 14 , 2 , 14 , 2 , 10 , 2 , 0 , 2 , 7 , 2 , 14 , 13 , 2 ],\
        [ 2 , 13 , 0 , 7 , 11 , 2 , 9 , 2 , 13 , 2 , 0 , 2 , 11 , 14 , 2 ],\
        [ 2 , 14 , 2 , 2 , 13 , 2 , 14 , 2 , 14 , 2 , 0 , 2 , 15 , 10 , 2 ],\
        [ 2 , 2 , 2 , 2 , 14 , 2 , 7 , 2 , 7 , 2 , 0 , 2 , 12 , 14 , 2 ],\
        [ 2 , 13 , 13 , 7 , 13 , 2 , 0 , 11 , 0 , 12 , 6 , 2 , 11 , 9 , 2 ],\
        [ 2 , 10 , 9 , 2 , 0 , 0 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 ],\
        [ 2 , 5 , 12 , 2 , 4 , 0 , 15 , 9 , 11 , 5 , 9 , 10 , 5 , 9 , 2 ],\
        [ 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 ]],\
        [\
        [ 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2],\
        [ 2 , 2 , 4 , 10 , 9 , 0 , 6 , 7 , 11 , 13 , 14 , 10 , 2 , 9 , 2 ],\
        [ 2 , 2 , 2 , 2 , 2 , 2 , 14 , 2 , 2 , 2 , 2 , 2 , 2 , 8 , 2 ],\
        [ 2 , 15 , 14 , 14 , 14 , 12 , 13 , 13 , 2 , 5 , 2 , 12 , 2 , 9 , 2 ],\
        [ 2 , 15 , 2 , 2 , 2 , 2 , 2 , 0 , 7 , 11 , 2 , 11 , 2 , 15 , 2 ],\
        [ 2 , 15 , 2 , 11 , 6 , 9 , 2 , 14 , 2 , 11 , 2 , 15 , 7 , 15 , 2 ],\
        [ 2 , 15 , 2 , 11 , 15 , 15 , 7 , 11 , 2 , 13 , 2 , 2 , 2 , 14 , 2 ],\
        [ 2 , 15 , 2 , 15 , 15 , 15 , 2 , 13 , 2 , 11 , 11 , 2 , 15 , 11 , 2 ],\
        [ 2 , 15 , 2 , 10 , 9 , 10 , 2 , 14 , 2 , 2 , 14 , 2 , 2 , 13 , 2 ],\
        [ 2 , 15 , 2 , 2 , 2 , 2 , 2 , 13 , 0 , 2 , 9 , 2 , 9 , 10 , 2 ],\
        [ 2 , 15 , 2 , 2 , 9 , 2 , 14 , 0 , 14 , 2 , 10 , 2 , 7 , 2 , 2 ],\
        [ 2 , 11 , 7 , 14 , 10 , 2 , 11 , 2 , 8 , 2 , 10 , 7 , 15 , 11 , 2 ],\
        [ 2 , 14 , 2 , 2 , 2 , 2 , 14 , 2 , 10 , 2 , 0 , 2 , 8 , 2 , 2 ],\
        [ 2 , 5 , 2 , 11 , 9 , 10 , 10 , 2 , 12 , 2 , 10 , 2 , 0 , 16 , 2 ],\
        [ 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 ]]]
    
    allgroup = pygame.sprite.OrderedUpdates()
    messageGroup = pygame.sprite.Group()
    
    #list that contains all goups 
    list_of_all_groups = list(pygame.sprite.Group() for x in range (len(dungeon_map)))
    
    #modifes a similar dungeon_map list with object content
    map_object = list( list(list(None for a in range (15) ) for b in range (15) ) for c in range (len(dungeon_map)))
    
    #create objects
    for a in range ( len(list_of_all_groups) ):
        for b in range ( 15 ):
            for c in range ( 15 ):
                # create objects
                if dungeon_map[a][b][c] == 1:
                    player = Mainfinal3.Player(screen, -100, -100,)
                    map_object[a][b][c] = player
                if dungeon_map[a][b][c] == 2:
                    map_object[a][b][c] = Mainfinal3.Wall(screen, -100, -100,)
                if dungeon_map[a][b][c] == 3:
                    map_object[a][b][c] = Mainfinal3.Stairs(screen, -100, -100, 0)
                if dungeon_map[a][b][c] == 4:
                    map_object[a][b][c] = Mainfinal3.Stairs(screen, -100, -100, 1)
                if dungeon_map[a][b][c] == 5:
                    map_object[a][b][c] = Mainfinal3.Pickups(screen, -100, -100, 2)
                if dungeon_map[a][b][c] == 6:
                    map_object[a][b][c] = Mainfinal3.Pickups(screen, -100, -100, 3)
                if dungeon_map[a][b][c] == 7 :
                    map_object[a][b][c] = Mainfinal3.Door(screen, -100, -100, 0)
                if dungeon_map[a][b][c] == 8:
                    map_object[a][b][c] = Mainfinal3.Door(screen, -100, -100, 1)
                if dungeon_map[a][b][c] == 9:
                    map_object[a][b][c] = Mainfinal3.Pickups(screen, -100, -100, 0)
                if dungeon_map[a][b][c] == 10:
                    map_object[a][b][c] = Mainfinal3.Pickups(screen, -100, -100, 1)
                if dungeon_map[a][b][c] == 11:
                    map_object[a][b][c] = Mainfinal3.Pickups(screen, -100, -100, 4)
                if dungeon_map[a][b][c] == 12:
                    map_object[a][b][c] = Mainfinal3.Pickups(screen, -100, -100, 5)
                if dungeon_map[a][b][c] == 13:
                    map_object[a][b][c] = Mainfinal3.Monster(screen, -100, -100, 0)
                if dungeon_map[a][b][c] == 14:
                    map_object[a][b][c] = Mainfinal3.Monster(screen, -100, -100, 1)
                if dungeon_map[a][b][c] == 15:
                    map_object[a][b][c] = Mainfinal3.Monster(screen, -100, -100, 2)
                if dungeon_map[a][b][c] == 16:
                    map_object[a][b][c] = Mainfinal3.Monster(screen, -100, -100, 3)
                
                if map_object[a][b][c] != None :
                    list_of_all_groups[a].add( map_object[a][b][c] )
        
        #add in groups of score keepers
        hp = Mainfinal3.Hp_keeper(screen,player)
        atk = Mainfinal3.Atk_keeper(screen,player)
        defe =  Mainfinal3.Def_keeper(screen,player)
        ykey  = Mainfinal3.Ykey_keeper(screen,player)
        bkey = Mainfinal3.Bkey_keeper(screen,player)
        messageGroup = pygame.sprite.Group()
        messageGroup.add(hp,atk,defe,ykey,bkey)
        
        allgroup.add(dungeon)
        allgroup.add(list_of_all_groups)
        
    # ASSIGN
    clock = pygame.time.Clock()
    keepGoing = True
    quitgame = False
    current_floor = 0
    pygame.mixer.music.load('./sound/background.wav')
    pygame.mixer.music.set_volume(0.5)    
    pygame.mixer.music.play(-1)
    movesound = pygame.mixer.Sound('./sound/move.wav')
    movesound.set_volume(0.5)
    opensound = pygame.mixer.Sound("./sound/opendoor.wav")
    opensound.set_volume(1)
    fightsound = pygame.mixer.Sound("./sound/fight.wav")
    fightsound.set_volume(1)
    picksound = pygame.mixer.Sound("./sound/pick.wav")
    picksound.set_volume(1)
    bosskill = [1]

    # LOOP
    while keepGoing and bosskill:
    # TIME 
        clock.tick(30) 
      
        # EVENT HANDLING: Player uses arrow keys or kill the program
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                keepGoing = False
                quitgame = True
            if event.type == pygame.QUIT\
               or (event.type == pygame.KEYDOWN\
                  and event.key == pygame.K_ESCAPE):
                    display.quit()
                    sys.exit()
                
            elif event.type == pygame.KEYDOWN:
                
                playerx = player.getX()/32
                playery = player.getY()/32
                
                if event.key == pygame.K_UP:
                    player.change_image(6)
                    if movable( player, map_object,dungeon_map, current_floor,playerx, playery-1,movesound,opensound,fightsound,picksound,bosskill):
                        
                        dungeon_map[current_floor][playery-1][playerx]= 1
                        dungeon_map[current_floor][playery][playerx] = 0
                        map_object[current_floor][playery-1][playerx]= player
                        map_object[current_floor][playery][playerx] = None
                        
                    data_change = change_floor(player, map_object,dungeon_map, current_floor,playerx, playery-1)
                    current_floor = data_change[0]
                    dungeon_map = data_change[1]
                    map_object = data_change[2]
                    
                if event.key == pygame.K_DOWN:
                    player.change_image(0)
                    if movable( player, map_object, dungeon_map, current_floor,playerx, playery+1,movesound,opensound,fightsound,picksound,bosskill):
                        
                        dungeon_map[current_floor][playery+1][playerx]= 1
                        dungeon_map[current_floor][playery][playerx] = 0
                        map_object[current_floor][playery+1][playerx]= player
                        map_object[current_floor][playery][playerx] = None
                    
                    data_change = change_floor(player, map_object,dungeon_map, current_floor,playerx, playery+1)
                    current_floor = data_change[0]
                    dungeon_map = data_change[1]
                    map_object = data_change[2]
                    
                if event.key == pygame.K_LEFT:
                    player.change_image(2)
                    if movable( player, map_object, dungeon_map, current_floor,playerx-1, playery,movesound,opensound,fightsound,picksound,bosskill):
                        
                        dungeon_map[current_floor][playery][playerx-1]= 1
                        dungeon_map[current_floor][playery][playerx] = 0
                        map_object[current_floor][playery][playerx-1]= player
                        map_object[current_floor][playery][playerx] = None
                    
                    data_change = change_floor(player, map_object,dungeon_map, current_floor,playerx-1, playery)
                    current_floor = data_change[0]
                    dungeon_map = data_change[1]
                    map_object = data_change[2]
                
                if event.key == pygame.K_RIGHT:
                    
                    player.change_image(4)
                    if movable( player, map_object, dungeon_map,current_floor,playerx+1, playery,movesound,opensound,fightsound,picksound,bosskill):
                        
                        dungeon_map[current_floor][playery][playerx+1]= 1
                        dungeon_map[current_floor][playery][playerx] = 0
                        map_object[current_floor][playery][playerx+1]= player
                        map_object[current_floor][playery][playerx] = None
                        
                    data_change = change_floor(player, map_object,dungeon_map, current_floor,playerx+1, playery)
                    current_floor = data_change[0]
                    dungeon_map = data_change[1]
                    map_object = data_change[2]
                
                
                hp.sethp( player )
                defe.setdef( player )
                atk.setatk( player )
                bkey.setbkey( player )
                ykey.setykey( player )
                
                            
        #display only the current floor at there right posistion
        for b in range ( 15 ):
            for c in range ( 15 ): 
                if map_object[current_floor][b][c] != None:
                    map_object[current_floor][b][c].setX( c )
                    map_object[current_floor][b][c].setY( b )
        # Beat the boss and you win!!!
##        lord = Mainfinal3.Monster(screen, -100, -100, 3)
##        if lord.exist() == False:
##            KeepGoing = False
##            pygame.quit()

        # REFRESH SCREEN 
        allgroup.clear(screen, background)
        messageGroup.clear(screen, background)
        allgroup.update()
        messageGroup.update()
        allgroup.draw(screen)
        messageGroup.draw(screen)
        
        pygame.display.flip()
    allgroup.clear(screen, background)
    messageGroup.clear(screen, background)
    congratulation()

def congratulation():
    """This is the instrction screen for the game."""

    # DISPLAY
    pygame.display.set_caption("Tower of the Sorcerer V2.0") 
    
    
    
    # ENTITIES
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((255, 255, 255))
    congsound = pygame.mixer.Sound('./sound/congs.wav')
    congsound.set_volume(0.5)
    
    

    # create a background of the instruction
    congratulation = Mainfinal3.congratulation( screen )
    conggroup = pygame.sprite.Group()
    
    #Display the instrction
    instructionfont = pygame.font.Font("./Font/PittoresqJugendstil.ttf", 40)
    message = ('    YOU BEAT THE DARKNESS FORCE!!!',\
               '                                           ',\
               '            YOU SAVE THE WORLD!!!'
               '                                           ',\
               '                                           ',\
               '            (Press Esc for quit)')
    instructiontxtlist = []
    for line in message:
        temp = instructionfont.render(line,1,(255,255,255))
        instructiontxtlist.append(temp)
    
    # ASSIGN
    clock = pygame.time.Clock()
    keepGoing = True
    
    conggroup.add(congratulation)
    congsound.play()
    # LOOP
    while keepGoing:
    # TIME 
        clock.tick(30) 
        
        # EVENT HANDLING: Player uses arrow keys 
        for event in pygame.event.get():
            if event.type == pygame.QUIT\
               or (event.type == pygame.KEYDOWN\
                  and event.key == pygame.K_ESCAPE):
                    display.quit()
                    sys.exit()
                    congsound.stop()
                
            elif event.type == pygame.KEYDOWN: 
              keepGoing = False
        
        conggroup.clear(screen, background)
        conggroup.draw(screen)
        for i in range(len(instructiontxtlist)):
            screen.blit(instructiontxtlist[i],(50,35*i+200))
        
        
        pygame.display.flip()
    display.quit()
    sys.exit()
    congsound.stop()
    conggroup.clear(screen, background)

def movable ( player, map_object, dungeon_map,currentLevel,x, y,movesound,opensound,fightsound,picksound,bosskill):
    """This function will determine if the player can reach the trageted area
    (x,y). It will deal with all event collision happened, and return true/false"""
     
    if dungeon_map[currentLevel][y][x] == 0:
        movesound.play()
        return True
    
    if (dungeon_map[currentLevel][y][x] > 2) and (dungeon_map[currentLevel][y][x] <5):
        return False
     
    if dungeon_map[currentLevel][y][x] == 2:
        return False
     
    if dungeon_map[currentLevel][y][x] == 5:
        player.ykey_update(1)
        picksound.play()
        map_object[currentLevel][y][x].kill()
        return True
    
     
    if dungeon_map[currentLevel][y][x] == 6:
        player.bkey_update(1)
        picksound.play()
        map_object[currentLevel][y][x].kill()
        return True
     
    if dungeon_map[currentLevel][y][x] == 7 :
        if player.getYkey() > 0:
            map_object[currentLevel][y][x].opens()
            player.ykey_update(-1)
            opensound.play()
            return True
        else:
            return False
          
    if dungeon_map[currentLevel][y][x] == 8:
        if player.getBkey() > 0:
            map_object[currentLevel][y][x].opens()
            player.bkey_update(-1)
            opensound.play()
            return True
        else:
            return False
          
    if dungeon_map[currentLevel][y][x] == 9:
        player.atk_update( 10 )
        picksound.play()
        map_object[currentLevel][y][x].kill()
        return True
     
    if dungeon_map[currentLevel][y][x] == 10:
        player.def_update( 4 )
        picksound.play()
        map_object[currentLevel][y][x].kill()
        return True
     
    if dungeon_map[currentLevel][y][x] == 11:
        player.hp_update( 400 )
        picksound.play()
        map_object[currentLevel][y][x].kill()
        return True
     
    if dungeon_map[currentLevel][y][x] == 12:
        player.hp_update( 200 )
        picksound.play()
        map_object[currentLevel][y][x].kill()
        return True
     
    if dungeon_map[currentLevel][y][x] == 13:
        if fightable( player, map_object[currentLevel][y][x] ):
            player.atk_update(3)
            fightsound.play()
            return True
        else:
            return False

    if dungeon_map[currentLevel][y][x] == 14:
        if fightable( player, map_object[currentLevel][y][x] ):
            player.def_update(2)
            fightsound.play()
            return True
        else:
            return False

    if dungeon_map[currentLevel][y][x] == 15:
        if fightable( player, map_object[currentLevel][y][x] ):
            fightsound.play()
            player.def_update(5)
            player.atk_update(15)
            return True
        else:
            return False

    if dungeon_map[currentLevel][y][x] == 16:
        lord = Mainfinal3.Monster(screen, -100, -100, 3)
##        map_object[a][b][c] = lord
        if fightable(player, map_object[currentLevel][y][x] ) == True:
            bosskill.remove(1)
            KeepGoing = True
        
def fightable( player, monster ):
    """ This function will determine if the player is able to survive the battle 
    with the targeted monster. The monster sprite will be killed if the it is 
    fightable. Return true and false based on the condition"""
    
    #the target is not fightable if the player cannot deal damages
    if ( player.getatk() <= monster.getdef() ):
        return False

    
    playerDmg = player.getatk() - monster.getdef()
    if monster.getatk() <player.getdef():
        monsterDmg = 0
    else:
        monsterDmg = monster.getatk() - player.getdef()

    playerHealth = player.gethp()
    monsterHealth = monster.gethp()
    
    while (playerHealth > 0 and monsterHealth > 0 ):
        playerHealth -= monsterDmg
        monsterHealth -= playerDmg
        
    if playerHealth <= 0:
        return False
    
    else:
        monster.kill()
        player.sethp( playerHealth)
        
        return True
    
def change_floor ( player, map_object, dungeon_map,currentLevel,x, y ):
    """This function will determine if the player reaches a stairs and requrires
    to go to the next or previous floor, returns value of current floor"""
     
    # the drop points of the player when changing floors (y,x)
    down = [[1,2],[2,13],[2,1],[-1,-1]]
    up = [[-1,-1],[5,8],[12,4],[1,3]]
    playerx = player.getX()/32
    playery = player.getY()/32
    
    if (dungeon_map[currentLevel][y][x] > 2) and (dungeon_map[currentLevel][y][x] <5):
        for b in range ( 15 ):
            for c in range ( 15 ): 
                if map_object[currentLevel][b][c] != None:
                    map_object[currentLevel][b][c].setX( -999 )
                    map_object[currentLevel][b][c].setY( -999 )
    
        if dungeon_map[currentLevel][y][x] == 3:
            currentLevel += 1
            print currentLevel
            dungeon_map[currentLevel][up[currentLevel][0]][up[currentLevel][1]]= 1
            dungeon_map[currentLevel-1][playery][playerx] = 0
            map_object[currentLevel][up[currentLevel][0]][up[currentLevel][1]]= player
            map_object[currentLevel-1][playery][playerx] = None


        if dungeon_map[currentLevel][y][x] == 4:
            currentLevel -= 1 
            print currentLevel
            dungeon_map[currentLevel][down[currentLevel][0]][down[currentLevel][1]]= 1
            dungeon_map[currentLevel+1][playery][playerx] = 0
            map_object[currentLevel][down[currentLevel][0]][down[currentLevel][1]]= player
            map_object[currentLevel+1][playery][playerx] = None


    return [currentLevel, dungeon_map, map_object]

instruction()
