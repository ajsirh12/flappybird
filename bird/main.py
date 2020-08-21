import pygame    # pygame 모듈의 임포트
import sys   # 외장 모듈
from random import randint
from pygame.locals import *  # QUIT 등의 pygame 상수들을 로드한다.

width = 400  # 상수 설정
height = 400
white = (255, 255, 255)
green = (0, 255, 0)
black = (0, 0, 0)
fps = 30
bird_x = int(30)
bird_y = int(height / 2)
bird_up = False
speed = 0
gameover = False

topobs = list()
botobs = list()

bird_image = pygame.image.load("./cave/bird.png")
bird_small = pygame.transform.scale(bird_image, (32, 32))
bang_image = pygame.image.load("./cave/bang.png")


def main():
    pygame.init()
    clock = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird')
    dpsurf = pygame.display.set_mode((width, height), 0, 32)
    cnt = 0
    score = 0
    while True:
        key_input()

        if not gameover:
            move_wall(cnt)
            move_bird()
            spread_img(dpsurf)
            view_score(dpsurf, score)
            cnt += 1
            if cnt % 10 == 0:
                score += 1

        else:
            game_over(dpsurf)

        pygame.display.update()
        clock.tick(fps)


def key_input():
    global bird_up
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_UP:
                bird_up = True


def move_bird():
    global bird_up
    global bird_y
    global speed
    global gameover

    if bird_up:
        bird_y -= 30
        bird_up = False
        speed = 0
    bird_y += speed
    if speed < 5:
        speed += 1

    collision_test()
    if bird_y <= 0 or bird_y > (height-32):
        gameover = True


def move_wall(cnt):
    if cnt % 50 == 0:
        asd = randint(5, 25) * 10
        topobs.append(Rect(width, 0, 50, asd))
        botobs.append(Rect(width, 400, 50, -height + asd + 100))

    for i in range(len(topobs)):
        topobs[i].left -= 5
        botobs[i].left -= 5


def spread_img(dpsurf):
    dpsurf.fill(white)

    dpsurf.blit(bird_small, (bird_x, bird_y))
    for i in range(len(topobs)):
        if topobs[i].left > -100:
            pygame.draw.rect(dpsurf, green, topobs[i])
            pygame.draw.rect(dpsurf, green, botobs[i])


def view_score(dpsurf, score):
    qwe = pygame.font.SysFont(None, 36)
    score_img = qwe.render("SCORE : {}".format(score), True, black)

    dpsurf.blit(score_img, (20, 20))


def collision_test():
    global gameover
    for i in range(len(topobs)):
        if topobs[i].left-25 <= bird_x <= topobs[i].left+25:
            if topobs[i].top <= bird_y-16 and bird_y+16 <= topobs[i].height:
                gameover = True
            if (botobs[i].top + botobs[i].height) <= bird_y+16 and bird_y-16 <= botobs[i].top:
                gameover = True


def game_over(dpsurf):
    font_style = pygame.font.SysFont('굴림', 50)
    gameover_img = font_style.render("GAME OVER", True, black)

    dpsurf.blit(bang_image, (bird_x - 32, bird_y - 32))
    dpsurf.blit(gameover_img, (width/4, height/2))


if __name__ == '__main__':
    main()

