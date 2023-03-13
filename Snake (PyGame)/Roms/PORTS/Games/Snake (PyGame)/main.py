import pygame
import sys
import random

from snake import Snake
from food import Food

pygame.init()


INFO = pygame.display.Info()

TILE_SIZE = 24
LINE_SIZE = int(TILE_SIZE/15)
TILE_NUMBER = 20

monitor = pygame.display.set_mode((640,480))
s = pygame.Surface((TILE_NUMBER * TILE_SIZE, TILE_NUMBER * TILE_SIZE))
pygame.display.set_caption('Snake')

food_img = pygame.Surface((TILE_SIZE - 2 * LINE_SIZE, TILE_SIZE - 2 * LINE_SIZE))
food_img.fill((255, 0, 0))
eaten_food_img = pygame.Surface((TILE_SIZE - 2 * LINE_SIZE, TILE_SIZE - 2 * LINE_SIZE))
eaten_food_img.fill((240, 128, 128))
head_img = pygame.Surface((TILE_SIZE - 2 * LINE_SIZE, TILE_SIZE - 2 * LINE_SIZE))
head_img.fill((153, 153, 0))
tail_img = pygame.Surface((TILE_SIZE - 2 * LINE_SIZE, TILE_SIZE - 2 * LINE_SIZE))
tail_img.fill((0, 128, 0))
clock = pygame.time.Clock()
font_score = pygame.font.Font(pygame.font.get_default_font(), int(TILE_SIZE))

food_list = []
python = Snake()


def draw(score):
    for i in range(TILE_NUMBER):
        for j in range(TILE_NUMBER):
            if (j+i) % 2 == 0:
                pygame.draw.rect(s, pygame.Color(176, 224, 230), (i*TILE_SIZE, j*TILE_SIZE, TILE_SIZE, TILE_SIZE), 0)
            else:
                pygame.draw.rect(s, pygame.Color(173, 216, 230), (i*TILE_SIZE, j*TILE_SIZE, TILE_SIZE, TILE_SIZE), 0)

    for i in range(len(python.pozX)):
        if i == 0:
            s.blit(head_img, (LINE_SIZE + python.pozX[i] * TILE_SIZE, LINE_SIZE + python.pozY[i] * TILE_SIZE))
        else:
            s.blit(tail_img, (LINE_SIZE + python.pozX[i] * TILE_SIZE, LINE_SIZE + python.pozY[i] * TILE_SIZE))
           
    for i in food_list:
        if i.eaten:
            s.blit(eaten_food_img, (LINE_SIZE + i.poz_x * TILE_SIZE, LINE_SIZE + i.poz_y * TILE_SIZE))
        else:
            s.blit(food_img, (LINE_SIZE + i.poz_x * TILE_SIZE, LINE_SIZE + i.poz_y * TILE_SIZE))

    pygame.draw.line(s, pygame.Color(0, 191, 255), (0, 0), (0, TILE_SIZE * TILE_NUMBER), LINE_SIZE)
    pygame.draw.line(s, pygame.Color(0, 191, 255), (0, 0), (TILE_SIZE * TILE_NUMBER, 0), LINE_SIZE)
    pygame.draw.line(s, pygame.Color(0, 191, 255), (0, TILE_SIZE * TILE_NUMBER), (TILE_SIZE * TILE_NUMBER, TILE_SIZE * TILE_NUMBER), 2 *LINE_SIZE)
    pygame.draw.line(s, pygame.Color(0, 191, 255), (TILE_SIZE * TILE_NUMBER, 0), (TILE_SIZE * TILE_NUMBER, TILE_SIZE * TILE_NUMBER), 2 * LINE_SIZE)
    text = font_score.render('Score: ' + str(score), False, (0, 0, 0))
    s.blit(text, (5, 5))
    monitor.blit(pygame.transform.scale(s, (640,480)),(0,0))
    pygame.display.flip()
    
    
def collision(x, y, score):
    if x > TILE_NUMBER - 1 or x < 0 or y > TILE_NUMBER - 1 or y < 0:
        death(score)
        
    for i in range(1, len(python.pozX) - 1):
        if python.pozX[0] == python.pozX[i] and python.pozY[0] == python.pozY[i]:
            death(score)


def add_food():
    temp_x = random.randint(0, TILE_NUMBER - 1)
    temp_y = random.randint(0, TILE_NUMBER - 1)
    for i in range(len(python.pozX)):
        if python.pozX[i] == temp_x and python.pozY[i] == temp_y:
            add_food()
            return
    temp_food = Food(temp_x, temp_y)
    food_list.insert(0, temp_food)


def death(score):
    font = pygame.font.Font(pygame.font.get_default_font(), int(40))
    text = font.render('Score: ' + str(score), False, (0, 0, 0))
    text2 = font.render(' Press A to restart game', False, (0, 0, 0))

    #font_w = text.get_width()
    #font_h = text.get_height()
    #s.blit(text, (s.get_width() // 2 - font_w // 2, s.get_height() // 2 - font_h // 2))

    font_w = text2.get_width()
    font_h = text2.get_height()
    s.blit(text2, (s.get_width() // 2 - font_w // 2, s.get_height() // 2 - font_h // 2 + int(TILE_SIZE)))
    monitor.blit(pygame.transform.scale(s, (640,480)),(0,0))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    global food_list
                    food_list = []
                    main()
                    return
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()


def main():
    score = 0
    add_food()
    python.pozX = [10, 9, 8]
    python.pozY = [10, 10, 10]
    python.direction = 2
    python.speed = 3
    while python.live:
        clock.tick(python.speed)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit(0)
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if e.key == pygame.K_UP and python.direction != 1:
                    python.direction = 3
                elif e.key == pygame.K_DOWN and python.direction != 3:
                    python.direction = 1
                elif e.key == pygame.K_LEFT and python.direction != 2:
                    python.direction = 0
                elif e.key == pygame.K_RIGHT and python.direction != 0:
                    python.direction = 2

        for i in range(len(python.pozX) - 1, 0, -1):
            if i == 0:
                break
            python.pozX[i] = python.pozX[i - 1]
            python.pozY[i] = python.pozY[i - 1]

        if python.direction == 0:
            python.pozX[0] -= 1
        elif python.direction == 1:
            python.pozY[0] += 1
        elif python.direction == 2:
            python.pozX[0] += 1
        elif python.direction == 3:
            python.pozY[0] -= 1
            
        collision(python.pozX[0], python.pozY[0], score)
        
        if food_list[0].poz_x == python.pozX[0] and food_list[0].poz_y == python.pozY[0]:
            food_list[0].eaten = True
            score += 1
            if python.speed < 10:
                python.speed += 0.5
            add_food()
        if food_list[-1].poz_x == python.pozX[-1] and food_list[-1].poz_y == python.pozY[-1]:
            python.pozX.insert(-1, food_list[-1].poz_x)
            python.pozY.insert(-1, food_list[-1].poz_y)
            food_list.remove(food_list[-1])

        draw(score)


main()
