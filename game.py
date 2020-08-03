import pygame
import random
import math
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((800, 600))
background = pygame.image.load('background.png')

mixer.music.load('music.wav')
mixer.music.play(-1)

pygame.display.set_caption("vrinda's space force")
icon = pygame.image.load('alien.png')
pygame.display.set_icon(icon)

playerImg = pygame.image.load('spaceship.png')
playerX = 370
playerY = 480
playerX_change = 0

enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
number_of_enemies = 6

for i in range(number_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

missileImg = pygame.image.load('nuclear.png')
missileX = 0
missileY = 480
missileX_change = 0
missileY_change = 10
missile_state = "ready"

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

over_font = pygame.font.Font('freesansbold.ttf', 68)

textX = 10
testY = 10


def show_score(x, y):
    score = font.render("Vrinda's Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_missile(x, y):
    global missile_state
    missile_state = "Fire"
    screen.blit(missileImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, missileX, missileY):
    distance = math.sqrt((math.pow(enemyX - missileX, 2)) + (math.pow(enemyY - missileY, 2)))
    if distance < 27:
        return True
    else:
        return False


running = True

while running:

    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            print('incorrect key pressed')
            if event.key == pygame.K_LEFT:
                playerX_change = -4
                print('left arrow is pressed')
            if event.key == pygame.K_RIGHT:
                playerX_change = 4
                print('right arrow is pressed')
            if event.key == pygame.K_SPACE:
                if missile_state is "ready":
                    missile_sound = mixer.Sound('shoot.wav')
                    missile_sound.play()
                    missileX = playerX
                    fire_missile(missileX, missileY)
                    print('spacebar is pressed')
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                print('key released')

    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    if playerX >= 736:
        playerX = 736

    for i in range(number_of_enemies):

        if enemyY[i] > 440:
            for j in range(number_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        collision = isCollision(enemyX[i], enemyY[i], missileX, missileY)
        if collision:
            collision_sound = mixer.Sound('collision.wav')
            collision_sound.play()
            missileY = 480
            missile_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    if missileY <= 0:
        missileY = 480
        missile_state = "ready"
    if missile_state is "Fire":
        fire_missile(missileX, missileY)
        missileY -= missileY_change

    player(playerX, playerY)
    show_score(textX, testY)
    pygame.display.update()
