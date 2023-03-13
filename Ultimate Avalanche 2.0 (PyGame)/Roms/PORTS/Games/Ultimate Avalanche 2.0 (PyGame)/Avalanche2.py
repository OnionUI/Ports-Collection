'''   Ultimate Avalanche 2.0
     10.12.2010
     Brandon Cerge  | JD Crutchfeild | Joshua Murray
     EEL4834 : Dr. Boykin   '''

from random import randint, seed
import pygame
from Game_Handler import *
from sys import exit
monitor=None
def main():
        global monitor
        pygame.init()
        monitor = pygame.display.set_mode((640,480),0,32)
        root = pygame.Surface((500,500),32)
        pygame.display.set_caption("Ultimate Avalanche 2.0 | University of Florida | bcerge@ufl.edu")
        clock = pygame.time.Clock()
        pygame.mouse.set_visible(0)
        pygame.mixer.pre_init(44100, -16, 2, 1024 * 3)
        pygame.mixer.init()
        pygame.mixer.music.load("stargazers.wav")
        pygame.mixer.music.set_volume(.5)
        pygame.mixer.music.play(-1)

        selection = 0
        score = (2, 1337, 4004)
        while (42):
                if selection == 0: selection = main_menu(root, clock)
                if selection == 1:
                        score = single_player(root,clock) 
                        selection = 4
                if selection == 2: how_to(root,clock)
                if selection == 3: exit()
                if selection == 4:game_over(root,clock,score)
                selection = 0

def game_over(root,clock,score):
        background = pygame.image.load('background.png').convert()
        victim = pygame.image.load('dude.png').convert_alpha()
        gameoverfont = pygame.font.Font('gamecuben.ttf',60)
        text1 = gameoverfont.render('GAME',True,(255,255,255))
        text2 = gameoverfont.render('OVER',True,(255,255,255))
        gameoverfont = pygame.font.Font('gamecuben.ttf',14)
        text5 = gameoverfont.render('press backspace to',True,(0,0,0))
        text6 = gameoverfont.render('return to the menu',True,(0,0,0))
        gameoverfont = pygame.font.Font('gamecuben.ttf',20)
        text3 = gameoverfont.render('your score= %d' % (score), True, (0,0,0))

        root.blit(background,(0,0))
        root.blit(victim,(0,250))

        root.blit(text1,(5,30))
        root.blit(text2,(150,140))
        root.blit(text3,(158,290))
        root.blit(text5,(295,430))
        root.blit(text6,(295,450))
        monitor.blit(pygame.transform.scale(root, (640,480)),(0,0))
        pygame.display.flip()
        
        menu = True

        while menu:
                for e in pygame.event.get():
                        if e.type == pygame.QUIT:
                                exit()
                        if e.type == pygame.KEYDOWN:
                                if e.key == pygame.K_LCTRL:
                                        menu = False
                keys = pygame.key.get_pressed()
                if keys[pygame.K_ESCAPE]:
                       exit()

def how_to(root,clock):
        background = pygame.image.load('background.png').convert()
        victim = pygame.image.load('dude.png').convert_alpha()
        howtofont = pygame.font.Font('gamecuben.ttf',12)
        text1 = howtofont.render(' THE UNIVERSE HAS GONE MAD!',True,(0,0,0))
        text2 = howtofont.render(' IT IS RAINING RAZOR SHARP ICICLES!',True,(0,0,0))
        text3 = howtofont.render(' THE SOUND OF HEAVY METAL OPERA RINGS!',True,(0,0,0))
        text4 = howtofont.render(' NOW MEET OSCAR P.BOYKIN',True,(0,0,0))
        shieldinst = howtofont.render(': invulnerability',True,(0,0,0))
        heartinst = howtofont.render(': extra life',True,(0,0,0))
        bombinst = howtofont.render(': blows up all icicles',True,(0,0,0))
        arrowsinst = howtofont.render(': left and right',True,(0,0,0))
        howtofont = pygame.font.Font('gamecuben.ttf',13)
        text6 = howtofont.render('press backspace to',True,(0,0,0))
        text7 = howtofont.render('return to the menu',True,(0,0,0))
        howtofont = pygame.font.Font('gamecuben.ttf',20)
        text5 = howtofont.render(' DONT LET OSCAR DIE!!!!',True,(0,0,0))
        shield = pygame.image.load('shield.png').convert_alpha()
        heart = pygame.image.load('heart.png').convert_alpha()
        bomb = pygame.image.load('bomb.png').convert_alpha()
        arrows = pygame.image.load('arrows.png').convert_alpha()
        gamefont = pygame.font.Font('gamecuben.ttf',10)
        authortext = gamefont.render('by Brandon Cerge | John Crutchfield | Joshua Murray',True,(0,0,0))
        root.blit(background,(0,0))
        root.blit(victim,(0,250))
        root.blit(text1,(0,20))
        root.blit(authortext,(120,480))
        root.blit(text2,(0,40))
        root.blit(text3,(0,60))
        root.blit(text4,(0,80))
        root.blit(text5,(0,115))
        root.blit(shield, (170,190))
        root.blit(heart, (173,250))
        root.blit(bomb, (171,300))
        root.blit(arrows, (150,365))
        root.blit(shieldinst,(220,200))
        root.blit(heartinst,(220,255))
        root.blit(bombinst,(220,310))
        root.blit(arrowsinst,(240,375))
        root.blit(text6,(285,425))
        root.blit(text7,(285,445))   
        clock.tick(10)
        monitor.blit(pygame.transform.scale(root, (640,480)),(0,0))
        pygame.display.flip()
        menu = True

        while menu:
                for e in pygame.event.get():
                        if e.type == pygame.QUIT:
                                exit()
                        if e.type == pygame.KEYDOWN:
                                if e.key == pygame.K_LCTRL:
                                        menu = False
                keys = pygame.key.get_pressed()
                if keys[pygame.K_ESCAPE]:
                       exit()

def main_menu(root,clock):
        background = pygame.image.load('background.png').convert()
        victim = pygame.image.load('dude.png').convert_alpha()
        title_text = pygame.image.load('title_text.png').convert_alpha()
        menufont = pygame.font.Font('gamecuben.ttf',24)
        gamefont = pygame.font.Font('gamecuben.ttf',10)
        authortext = gamefont.render('by Brandon Cerge | John Crutchfield | Joshua Murray',True,(0,0,0))
        optiontext1 = menufont.render('Play!',True,(0,0,0))
        optiontext2 = menufont.render('How To Play',True,(0,0,0))
        optiontext3 = menufont.render('Exit',True,(0,0,0))
        arrow = pygame.sprite.RenderUpdates(Arrow())
        root.blit(background,(0,0))
        root.blit(victim,(0,250))
        root.blit(title_text,(0,0))
        root.blit(optiontext1,(260,240))
        root.blit(optiontext2,(260,280))
        root.blit(optiontext3,(260,320))
        root.blit(authortext,(120,480))
        menu = True
        option = 1

        while menu:
                for e in pygame.event.get():
                        if e.type == pygame.QUIT:
                                exit()
                        if e.type == pygame.KEYDOWN:
                                if e.key == pygame.K_SPACE:
                                        menu = False
                                if e.key == pygame.K_UP:
                                        option -= 1
                                        if option < 1:
                                                option = 3
                                if e.key == pygame.K_DOWN:
                                        option += 1
                                        if option > 3:
                                                option = 1
            
                arrow.clear(root,background)
                arrow.update(option)
                arrow.draw(root)
                clock.tick(10)
                monitor.blit(pygame.transform.scale(root, (640,480)),(0,0))
                pygame.display.flip()
        return option

def single_player(root,clock):
        seed()
        lives = 3
        score = 0
        menu = True
        level = 1
        lvl_counter = 2000
        ice_counter = 0
        count = 4
        level_ice = 2
        ice_shards = 0
        pwrup_counter = 900
        bomb_timer = 150
        deathflag = 0
        shield_flag = 0
        shield_counter = 350
        wnd = 0
        wind_timer = randint(1000,2000)
        wind_flag = 0
        death_timer = 0
        blood_intensity = [(-100,100,40.0),(-100,-35,120.0)]
        blood_life = (15,100)
        blood_speed = (200,300)
        blood_image = 'blood.png'
        ice_intensity = [(-100,100,50.0),(-100,-35,20.0)]
        ice_sky_intensity = [(-100,100,100.0),(-100,100,100.0)]
        ice_life = (15,25)
        ice_sky_life = (15,55)
        ice_speed = (200,250)
        ice_image = 'iceshard.png'
        cloud_intensity = [(-100,100,50.0),(-100,0,40.0)]
        cloud_life = (15,100)
        cloud_speed = (200,300)
        cloud_image = 'cloud.png'

        levelfont = pygame.font.Font('gamecuben.ttf',30)
        gamefont = pygame.font.Font('gamecuben.ttf',10)
        livesfont = pygame.font.Font('gamecuben.ttf',18)
        leveltext = levelfont.render('Level %d' % (level),True,(0,0,0))
        livestext = livesfont.render('X %d' % (lives),True,(0,0,0))
        heart = pygame.image.load('heart.png').convert_alpha()
        
        background = pygame.image.load('background.png').convert()
        dude = pygame.sprite.RenderUpdates(Man_No_Sheild(250,475))
        dude_with_shield = pygame.sprite.RenderUpdates()
        icicles = pygame.sprite.RenderUpdates()
        launcher = pygame.sprite.RenderUpdates()
        oneup = pygame.sprite.RenderUpdates()
        shield = pygame.sprite.RenderUpdates() 
        bomb = pygame.sprite.RenderUpdates() 
        
        pygame.mixer.pre_init(44100, -16, 2, 1024 * 3)
        pygame.mixer.init()
        scream = pygame.mixer.Sound("scream.wav")
        scream.set_volume(.7)
        nxtlvl = pygame.mixer.Sound('powerup.wav')
        wind = pygame.mixer.Sound("wind.wav")
        wind.set_volume(.3)
        icesmash = pygame.mixer.Sound("pistol.wav")
        icesmash.set_volume(.4)
        shieldhum = pygame.mixer.Sound("MachineHeavyHum.wav")
        shieldhum.set_volume(1)
        boom = pygame.mixer.Sound("bomb.wav")
        boom.set_volume(.5)
        oneupsound = pygame.mixer.Sound("1 up.wav")
        oneupsound.set_volume(.6)

        while menu:
                for e in pygame.event.get():
                        if e.type == pygame.QUIT:
                                exit()

                keys = pygame.key.get_pressed()
                if (dude.sprites()):
                        if menu == True:
                                dude.sprites()[0].direction = vector(0,0)
                                if keys[pygame.K_LEFT]:
                                        dude.sprites()[0].direction.x = -1
                                if keys[pygame.K_RIGHT]:
                                        dude.sprites()[0].direction.x = 1
                if (dude_with_shield.sprites()):
                        if menu == True:
                                dude_with_shield.sprites()[0].direction = vector(0,0)
                                if keys[pygame.K_LEFT]:
                                        dude_with_shield.sprites()[0].direction.x = -1
                                if keys[pygame.K_RIGHT]:
                                        dude_with_shield.sprites()[0].direction.x = 1
                if keys[pygame.K_ESCAPE]:
                       exit()

                if (lvl_counter < 1700):
                        ice_shards = count
                        ice_counter += 1
                        if ice_counter == 550:
                                count += 1
                                ice_counter = 0
                if lvl_counter == 0:
                        for y in icicles.sprites():
                                launcher.add(Explosion(y.cords.x,y.cords.y,5,ice_sky_intensity,ice_sky_life,ice_speed,ice_image))
                                y.alive = False
                        nxtlvl.play()
                        pwrup_counter = 930
                        level_ice = count
                        ice_shards = 0
                        ice_counter = 0
                        lvl_counter = 2000
                        level += 1
                        score += 300*level*level
                        leveltext = levelfont.render('Level %d' % (level),True,(0,0,0))

                if (lvl_counter == 1710 and deathflag == 1):
                        deathflag = 0
                        dude.add(Man_No_Sheild(250,475))

                lvl_counter -= 1
                pwrup_counter -= 1
                
                if pwrup_counter == 0:
                        temp = randint(1,3)
                        pwrup_counter = 630
                        if temp == 1: oneup.add(Oneup())
                        if temp == 2: shield.add(Shield())
                        if temp == 3:
                                bomb.add(Bomb())
                                bombtimer = 200

                if (bomb.sprites()):
                        bombtimer -= 1
                        if bombtimer < 50:
                                if (bombtimer % 2) == 0: bomb.sprites()[0].cords.x += 5
                                else: bomb.sprites()[0].cords.x -= 5
                        if bombtimer == 0:
                                bomb.sprites()[0].alive = False
                                launcher.add(Explosion(bomb.sprites()[0].cords.x,bomb.sprites()[0].cords.y,50,cloud_intensity,cloud_life,cloud_speed,cloud_image))
                                boom.play()

                if shield_flag == 1:
                        shield_counter -= 1
                        if shield_counter == 0:
                                dude_with_shield.sprites()[0].alive = False
                                dude.add(Man_No_Sheild(dude_with_shield.sprites()[0].cords.x,dude_with_shield.sprites()[0].cords.y -10))
                                shield_flag = 0
                                shield_counter = 350

                if len(icicles.sprites()) < ice_shards:  icicles.add(Icicle())

                for x in icicles.sprites():
                        if x.cords.y > 465:
                                x.alive = False
                                icesmash.play()
                                launcher.add(Explosion(x.cords.x,470,4,ice_intensity,ice_life,ice_speed,ice_image))
                                if (dude.sprites()):
                                        score += level * randint(2,9)

                ice_man_collide = pygame.sprite.groupcollide(icicles,dude,0,0).values()
                for x in ice_man_collide:
                        x[0].alive = False
                        launcher.add(Explosion(x[0].cords.x,x[0].cords.y,200,blood_intensity,blood_life,blood_speed,blood_image))
                        scream.play()
                        ice_shards = 0
                        lvl_counter = 2000
                        count = level_ice
                        lives -= 1
                        deathflag = 1
                        if lives == 0:
                                death_timer = 75
                        livestext = livesfont.render('X %d' % (lives),True,(0,0,0))

                man_heart_collide = pygame.sprite.groupcollide(dude,oneup,0,0).values()
                for x in man_heart_collide:
                        x[0].alive = False
                        oneupsound.play()
                        lives += 1
                        score += level * randint(1,9)
                        livestext = livesfont.render('X %d' % (lives),True,(0,0,0))

                man_bomb_collide = pygame.sprite.groupcollide(dude,bomb,0,0).values()
                for x in man_bomb_collide:
                        x[0].alive = False
                        boom.play()
                        for y in icicles.sprites():
                                launcher.add(Explosion(y.cords.x,y.cords.y,5,ice_sky_intensity,ice_sky_life,ice_speed,ice_image))
                                y.alive = False
                                score += level * 100

                man_shield_collide = pygame.sprite.groupcollide(dude,shield,0,0).values()
                for x in man_shield_collide:
                        x[0].alive = False
                        shieldhum.play()
                        dude.sprites()[0].alive = False
                        dude_with_shield.add(Man(dude.sprites()[0].cords.x,dude.sprites()[0].cords.y + 10))
                        shield_flag = 1

                shield_ice_collide = pygame.sprite.groupcollide(dude_with_shield,icicles,0,0).values()
                for x in shield_ice_collide:
                        for y in x:
                                y.alive = False
                                icesmash.play()
                                launcher.add(Explosion(y.cords.x,y.cords.y,4,ice_intensity,ice_life,ice_speed,ice_image))
                                score += 9*randint(2,9)

                wind_timer -= 1
                if (wind_timer == 420):
                        wind.play(1)
                        tflag = randint(1,2)
                        if tflag == 1: wnd = randint(25,80) / 150.0
                        if tflag == 2: wnd = -1 * randint(25,80) / 150.0

                if wind_timer == 0:
                        wind_timer = randint(1280,2280)
                        wnd = 0

                death_timer -= 1
                if death_timer == 1: menu = False

                scoretext = gamefont.render('SCORE: %d' % (score),True,(0,0,0))
                lvltext = gamefont.render('NEXT LEVEL: %d' %(lvl_counter),True,(0,0,0))
                lvltext2 = gamefont.render('Level: %d' % (level),True,(0,0,0))             
                time = clock.tick(55) / 1000.0
                root.blit(background,(0,0))
                oneup.clear(root,background)
                oneup.update(time)
                oneup.draw(root)
                shield.clear(root,background)
                shield.update(time)
                shield.draw(root)
                bomb.clear(root,background)
                bomb.update(time)
                bomb.draw(root)
                icicles.clear(root,background)
                icicles.update(time,wnd)
                icicles.draw(root)
                dude.clear(root,background)
                dude.update(time)
                dude.draw(root)
                dude_with_shield.clear(root,background)
                dude_with_shield.update(time)
                dude_with_shield.draw(root)
                launcher.update(time,root,background)
                root.blit(scoretext,(10,480))
                root.blit(lvltext,(190,480))
                if (lvl_counter > 1700):
                        root.blit(leveltext,(180,100))
                root.blit(heart,(10,10))
                root.blit(livestext,(45,15))
                root.blit(lvltext2,(420,480))
                monitor.blit(pygame.transform.scale(root, (640,480)),(0,0))
                pygame.display.flip()
        return score
        
if __name__ == '__main__': main()
