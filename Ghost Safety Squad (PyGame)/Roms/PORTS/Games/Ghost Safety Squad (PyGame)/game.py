#!/usr/bin/env python

# Copyright (C) 2012  Daniel Kinsman
# danielkinsman+gss@gmail.com

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import pygame
import random
import euclid
import math

class CrashPredictor(pygame.sprite.Sprite):
    def __init__(self, vehicle):
        super(CrashPredictor, self).__init__()
        self.vehicle = vehicle
        self.image = pygame.image.load('images/collider.png')
        self.rect = pygame.Rect(0, 0, self.image.get_width(), self.image.get_height())
        
    def update(self):
        xOff = (self.vehicle.image.get_width() / 2) + (self.image.get_width() / 2)
        if self.vehicle.velocity.x > 0:
            offset = euclid.Vector2(xOff, 0)
        else:
            offset = euclid.Vector2(-xOff, 0)
            
        self.rect.center = self.vehicle.position + offset

class Vehicle(pygame.sprite.DirtySprite):
    def __init__(self, image, maxVelocity, brakesound, acceleration):
        super(Vehicle, self).__init__()
        self.image = image
        self.position = euclid.Vector2(0, 0)
        self.velocity = euclid.Vector2(0, 0)
        self.rect = pygame.Rect(0, 0, self.image.get_width(), self.image.get_height())
        self.crashPredictor = CrashPredictor(self)
        self.maxVelocity = maxVelocity
        self.braking = False
        self.brakesound = brakesound
        self.acceleration = acceleration
        
    def update(self):
        self.position += self.velocity #need to include time elapsed here or the speed will depend on frame rate
        self.rect = pygame.Rect(0, 0, self.image.get_width(), self.image.get_height())
        self.rect.center = self.position
        
    def brake(self, collisions):
        #todo set deceleration based on vehicle type
        self.velocity.x *= 1.0 - self.acceleration
        
        #only play sounds when we first start braking
        if self.braking:
            return
            
        self.braking = True
            
        #play sounds if we are braking for a person
        for sprite in collisions:
            if type(sprite) is Person:
                self.brakesound.play()
                
    def accelerate(self):
        self.braking = False
        self.brakesound.stop()
        
        #todo set acceleration based on vehicle type
        self.velocity.x *= 1.0 + self.acceleration
                
        #if the car stops, give it a little push. This is a bit hackish, eh?
        #especially the use of Game.HEIGHT rather than screen.get_height()
        if self.velocity.magnitude() < 1:
            self.velocity.x = -1 if self.position.y > Game.HEIGHT / 2 else 1
            
        #todo vroom sounds
        
        
class Player(pygame.sprite.DirtySprite):
    GHOST_SPEED = 10
    POSSESS_SPEED_MULTIPLIER = 4
    def __init__(self, image):
        super(Player, self).__init__()
        self.baseimage = pygame.image.load(image)
        self.position = euclid.Vector2(0, 0)
        self.rect = pygame.Rect(0, 0, self.baseimage.get_width(), self.baseimage.get_height())
        self.host = None
        self.direction = euclid.Vector2(0, 0)
        self.speed = Player.GHOST_SPEED
        self.animationFrameCount = 0
        self.hostGoalY = 0
        
    def update(self):
        self.position += self.direction * self.speed
        
        if self.host is not None:
            if self.host.dead:
                self.dispossess()
            else:
                self.host.position = euclid.Vector2(self.position.x, self.position.y)
                self.host.goal = self.position + (self.direction * 10)
                
        self.animationFrameCount += 1
        if self.host is None:
            if self.animationFrameCount > 60:
                self.image = self.baseimage
            else:
                angle = self.animationFrameCount * 16
                scale = 0.25 + (0.75 / max(60 - self.animationFrameCount*1, 1))
                self.image = pygame.transform.rotozoom(self.baseimage, angle, scale)
        else:
            if self.animationFrameCount > 60:
                angle = 0
                scale = 0.25
            else:
                angle = self.animationFrameCount * -16
                scale = 0.25 + (0.75 / (self.animationFrameCount*1))
            
            self.image = pygame.transform.rotozoom(self.baseimage, angle, scale)
            
        self.rect = pygame.Rect(0, 0, self.image.get_width(), self.image.get_height())
        self.rect.center = self.position
        
        
    def possess(self, person):
        self.host = person
        self.animationFrameCount = 0
        self.hostGoalY = self.host.goal.y
        self.speed = person.speed * Player.POSSESS_SPEED_MULTIPLIER
        
    def dispossess(self):
        self.host.goal = euclid.Vector2(self.host.position.x, self.hostGoalY)
        self.host = None
        self.animationFrameCount = 0
        self.speed = Player.GHOST_SPEED
        
class Person(pygame.sprite.DirtySprite):
    def __init__(self, image, stepLeftImage, stepRightImage, deadimage, deathsound):
        super(Person, self).__init__()
        self.baseimage = pygame.image.load(image)
        self.baseImageStepLeft = pygame.image.load(stepLeftImage)
        self.baseImageStepRight = pygame.image.load(stepRightImage)
        self.image = None
        self.deadimage = pygame.image.load(deadimage)
        self.position = euclid.Vector2(0, 0)
        self.rect = pygame.Rect(0, 0, self.baseimage.get_width(), self.baseimage.get_height())
        self.dead = False
        self.deathsound = deathsound
        self.goal = None
        self.speed = 1
        self.currentDirection = euclid.Vector2(0, 1)
        self.animationFrameCount = 0
        self.currentBaseImage = self.baseimage
        
    def update(self):
        if (not self.dead) and (self.goal is not None):
            self.currentDirection = (self.goal - self.position).normalize()
            velocity = self.currentDirection * self.speed
            self.position += velocity
        
            try:
                angle = math.degrees(self.currentDirection.angle(euclid.Vector2(0, 1)))
            except ZeroDivisionError:
                angle = 0 #no direction, probably possessed and no keys depressed
            
            # bit of a hack
            if self.currentDirection.x < 0:
                angle = -angle
            
            self.animationFrameCount += 1
            if self.animationFrameCount % 30 == 0:
                self.animationFrameCount = 0
                if self.currentBaseImage is self.baseImageStepLeft:
                    self.currentBaseImage = self.baseImageStepRight
                else:
                    self.currentBaseImage = self.baseImageStepLeft
            
            self.image = pygame.transform.rotate(self.currentBaseImage, angle)
            self.rect = pygame.Rect(0, 0, self.image.get_width(), self.image.get_height())
            self.rect.center = self.position
        
    def kill(self):
        self.dead = True
        self.deathsound.play()
        self.image = self.deadimage
        
def offscreen(sprite, screen):
    if sprite.position.x < -sprite.rect.width:
        return True
        
    if sprite.position.y < -sprite.rect.height:
        return True
        
    if sprite.position.x > screen.get_width() + sprite.rect.width:
        return True
        
    if sprite.position.y > screen.get_height() + sprite.rect.height:
        return True
        
def vectorApproximatelyEqual(a, b, min_delta):
    if abs(a.x - b.x) >= min_delta:
        return False
        
    if abs(a.y - b.y) >= min_delta:
        return False
        
    return True

        
class Game(object):
    #constants
    VECTOR_COMPARE_MIN_DELTA = 0.0001
    WIDTH = 1024
    HEIGHT = 768
    SPAWN_PEOPLE_INCREASE_TIME = 30000
    SPAWN_CARS_BELOW = 16
    CAR_VELOCITY = 9
    CAR_ACCELERATION = 0.5
    TRUCK_VELOCITY = 6
    TRUCK_ACCELERATION = 0.035
    MOTORBIKE_VELOCITY = 12
    MOTORBIKE_ACCELERATION = 0.1
    TRAM_VELOCITY = 3
    TRAM_ACCELERATION = 0.025
    CAR_SPAWN_DELAY_AVERAGE = 1500
    DEATHS_TILL_GAME_OVER = 1
    SAVES_TILL_WIN = 20
    FONT_SIZE = 20
        
    def __init__(self):
        self.monitor = pygame.display.set_mode((640, 480), pygame.DOUBLEBUF)
        self.screen = pygame.Surface((Game.WIDTH, Game.HEIGHT))
        #self.screen = pygame.display.set_mode((Game.WIDTH, Game.HEIGHT), pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE)
       
        pygame.mixer.pre_init(44100, -16, 2, 8192)
        pygame.mixer.init()
        self.splat = pygame.mixer.Sound("sound/splat.ogg")
        self.carbrakehorn = pygame.mixer.Sound("sound/carbrakehorn.ogg")
        self.truckbrakehorn = pygame.mixer.Sound("sound/truckbrakehorn.ogg")
        self.motorbikebrakehorn = pygame.mixer.Sound("sound/motorbikebrakehorn.ogg")
        self.trambell = pygame.mixer.Sound("sound/trambell.ogg")
        
        pygame.mixer.music.load("sound/ghostsquishies.ogg")
        
        pygame.font.init()
        self.font = pygame.font.Font("Profaisal-EliteRiqaV1.0.ttf", Game.FONT_SIZE)
        
        self.background = pygame.image.load("images/background.png")
        
        self.carimage = pygame.image.load('images/car.png')
        self.truckimage = pygame.image.load('images/truck.png')
        self.motorbikeimage = pygame.image.load('images/motorbike.png')
        self.tramimage = pygame.image.load('images/tram.png')
        
        gameoversprite = pygame.sprite.DirtySprite()
        gameoversprite.image = pygame.image.load('images/gameover.png')
        gameoversprite.rect = pygame.Rect(0, 0, gameoversprite.image.get_width(), gameoversprite.image.get_height())
        gameoversprite.rect.center = (gameoversprite.image.get_width() / 2 + 50, gameoversprite.image.get_height() / 2 + 50)
        self.gameoverGroup = pygame.sprite.RenderUpdates([gameoversprite])
        
        self.winimage = pygame.image.load('images/win.png')
        
        self.carsSpawnDelay = Game.CAR_SPAWN_DELAY_AVERAGE
        self.bail = False
        
        self.reset()
        
    def reset(self):
        self.carGroup = pygame.sprite.RenderUpdates()
        self.crashPredictGroup = pygame.sprite.RenderUpdates()
        self.carSpawnLast = 0
        
        self.player = Player('images/player.png')
        self.player.position = euclid.Vector2(self.screen.get_width() / 2 + 20, self.screen.get_height() / 2 + 20)
        self.playerGroup = pygame.sprite.RenderUpdates(self.player)
        
        self.people = list()
        self.personGroup = pygame.sprite.RenderUpdates(self.people)
        
        self.possessToggle = False
        self.gameover = False
        
        self.peopleSaved = 0
        self.concurrentPeople = 1
        self.lastDifficultyIncrease = pygame.time.get_ticks()
        
        self.screen.blit(self.background, (0, 0))
        pygame.mixer.music.play(-1)
    
    def run(self):      
        clock = pygame.time.Clock()
        
        self.bail = False
        while not self.bail:
            elapsed = clock.tick(45)
            #if elapsed > 20:
            #    print("frametime drop:%(elapsed)03d" % {'elapsed': elapsed})
            
            now = pygame.time.get_ticks()
            if now - self.lastDifficultyIncrease > Game.SPAWN_PEOPLE_INCREASE_TIME * self.concurrentPeople:
                self.lastDifficultyIncrease = now
                self.concurrentPeople += 1
            
            #input
            self.processInput()
            
            if self.peopleSaved >= Game.SAVES_TILL_WIN:
                self.gameover = True
                while self.gameover and (not self.bail):
                    clock.tick(10)
                    self.screen.blit(self.winimage, (0, 0))
                    self.monitor.blit(pygame.transform.scale(self.screen, (640, 480)), (0,0))
                    pygame.display.flip()
                    self.processInput()
                    
                continue
                    
            #sim
            self.spawnPeople()
            self.spawnCars()
            
            self.carGroup.update()
            self.playerGroup.update()
            self.personGroup.update()
            self.crashPredictGroup.update()
            
            self.runCars()
            self.runPeople()
            self.runPlayer()
            
            dead = 0
            for person in self.personGroup:
                dead += 1 if person.dead else 0
                
            if dead >= Game.DEATHS_TILL_GAME_OVER:
                self.gameover = True
            
            #render
            self.personGroup.clear(self.screen, self.background)
            self.carGroup.clear(self.screen, self.background)
            self.playerGroup.clear(self.screen, self.background)
            #self.crashPredictGroup.clear(self.screen, self.background) #debug only
            
            self.personGroup.draw(self.screen)
            self.carGroup.draw(self.screen)
            self.playerGroup.draw(self.screen)
            #self.crashPredictGroup.draw(self.screen) #debug only
            fontsurf = self.font.render("Saved %(saved)d / %(savesTillWin)d" % {'saved': self.peopleSaved, 'savesTillWin' : Game.SAVES_TILL_WIN}, True, pygame.Color("white"))
            self.screen.blit(self.background, (0, 0), fontsurf.get_rect())
            self.screen.blit(fontsurf, (0, 0))
            
            if self.gameover:
                pygame.mixer.music.stop()
                self.gameoverGroup.draw(self.screen)
            self.monitor.blit(pygame.transform.scale(self.screen, (640, 480)), (0,0))
            pygame.display.flip()
        
        #clean up before exit
        pygame.display.quit()
        pygame.mixer.quit()
        pygame.font.quit()
        
    def runPeople(self):
        for person in self.people:
            if not person.dead:
                collisions = pygame.sprite.spritecollide(person, self.carGroup, False)
                if len(collisions) > 0:
                    for car in collisions:
                        if car.velocity.magnitude() > 1.0:
                            person.kill()
                elif offscreen(person, self.screen):
                    self.personGroup.remove(person)
                    self.people.remove(person)
                    if not self.gameover:
                        self.peopleSaved += 1
            else:
                pass
            
    def runCars(self):
        for car in self.carGroup.sprites():
            if offscreen(car, self.screen):
                self.carGroup.remove(car)
                
            #slow down if there's an obstacle ahead
            collisions = pygame.sprite.spritecollide(car.crashPredictor, self.carGroup, False)
            collisions.extend(pygame.sprite.spritecollide(car.crashPredictor, self.personGroup, False))
            
            braked = False
            
            if len(collisions) > 0 and ((collisions[0] is not car) or (len(collisions) > 1)):
                car.brake(collisions)
                braked = True
                #don't brake for dead people
                #print(collisions)
                #for sprite in collisions:
                    #if (type(sprite) is not Person) or (not sprite.dead):
                        #car.brake(collisions)
                        #braked = True
            
            
            if (not braked) and (car.velocity.magnitude() < car.maxVelocity):
                car.accelerate()
                
            
    def runPlayer(self):
        if self.possessToggle:
            if self.player.host is None:
                collisions = pygame.sprite.spritecollide(self.player, self.personGroup, False)
                if len(collisions) > 0:
                    self.player.possess(collisions[0])
                else:
                    pass
            else:
                self.player.dispossess()
                
            self.possessToggle = False
        else:
            pass
        
    def spawnPeople(self):
        aliveCount = 0
        for person in self.people:
            if not person.dead:
                aliveCount += 1
            else:
                pass
            
        if aliveCount < self.concurrentPeople:
            self.spawnPerson()
            
    def spawnPerson(self):
        #randomly choose top or bottom for y
        y = random.choice([0, self.screen.get_height()])
        goalY = self.screen.get_height() + 100 if y == 0 else -100
        
        #pick random x value
        x = random.randint(200, self.screen.get_width() - 200)
        
        #spawn person at x y
        character = random.choice(['1', '2', '3'])
        stand = 'images/person' + character + '.png'
        stepLeft = 'images/personstepleft' + character + '.png'
        stepRight = 'images/personstepright' + character + '.png'
        dead = 'images/deadperson' + character + '.png'
        person = Person(stand, stepLeft, stepRight, dead, self.splat)
        person.position = euclid.Vector2(x, y)
        person.goal = euclid.Vector2(x, goalY)
        self.people.append(person)
        self.personGroup.add(person)
        
    def spawnCars(self):
        now = pygame.time.get_ticks()
        elapsed = now - self.carSpawnLast
        if elapsed < self.carsSpawnDelay:
            return
        
        self.carsSpawnDelay = Game.CAR_SPAWN_DELAY_AVERAGE + random.randint(-500, +500)
        self.carSpawnLast = now
        
        if len(self.carGroup.sprites()) < Game.SPAWN_CARS_BELOW:
            #car or truck?
            vehicleType = random.choice(['car', 'truck', 'motorbike', 'tram'])
            if vehicleType == 'car':
                wheels = Vehicle(self.carimage, Game.CAR_VELOCITY, self.carbrakehorn, Game.CAR_ACCELERATION)
            elif vehicleType == 'truck':
                wheels = Vehicle(self.truckimage, Game.TRUCK_VELOCITY, self.truckbrakehorn, Game.TRUCK_ACCELERATION)
            elif vehicleType == 'motorbike':
                wheels = Vehicle(self.motorbikeimage, Game.MOTORBIKE_VELOCITY, self.motorbikebrakehorn, Game.MOTORBIKE_ACCELERATION)
            else:
                wheels = Vehicle(self.tramimage, Game.TRAM_VELOCITY, self.trambell, Game.TRAM_ACCELERATION)
            
            #pick a random side (left or right)
            x = random.choice([-100, self.screen.get_width() + 100])
            y = self.screen.get_height() / 2
            
            if x <= 0:
                xVelocity = wheels.maxVelocity
                y += -200 if vehicleType != 'tram' else -70
            else:
                xVelocity = -wheels.maxVelocity
                y += 200 if vehicleType != 'tram' else 70
                wheels.image = pygame.transform.flip(wheels.image, True, False)
            
            wheels.velocity = euclid.Vector2(xVelocity, 0)
            wheels.position = euclid.Vector2(x, y)
            wheels.update()
            
            #see if there is another (non-dead) sprite occupying the space, if so, do nothing
            collisions = pygame.sprite.spritecollide(wheels, self.carGroup, False)
            if len(collisions) == 0:
                self.carGroup.add(wheels)
                self.crashPredictGroup.add(wheels.crashPredictor)
            else:
                wheels.crashPredictor.vehicle = None
                wheels.crashPredictor = None
        
    def processInput(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.bail = True
                    break
                elif event.key == pygame.K_SPACE and not self.gameover:
                    self.possessToggle = True
                elif event.key == pygame.K_RETURN and self.gameover:
                    self.reset()
                else:
                    pass
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.possessToggle = False
                else:
                    pass
            elif event.type == pygame.QUIT:
                self.bail = True
            else:
                pass
            
                
        pygame.event.clear()
        
        self.player.direction = euclid.Vector2(0, 0)
        
        if self.gameover:
            return
        
        pressed = pygame.key.get_pressed()
        if (pressed[pygame.K_a] or pressed[pygame.K_LEFT]) and self.player.position.x > 0:
            self.player.direction.x -= 1
            
        if (pressed[pygame.K_d] or pressed[pygame.K_RIGHT]) and self.player.position.x < self.screen.get_width():
            self.player.direction.x += 1
            
        if (pressed[pygame.K_w] or pressed[pygame.K_UP]) and self.player.position.y > 0:
            self.player.direction.y -= 1
            
        if (pressed[pygame.K_s] or pressed[pygame.K_DOWN]) and self.player.position.y < self.screen.get_height():
            self.player.direction.y += 1
                

if __name__ == '__main__':
    Game().run()
