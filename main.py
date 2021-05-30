import math

import pygame
import random
from pygame import mixer


#When we add any pygame game we add this
pygame.init()

#Make the window 800 in width and 600 in height starts 0,0 at top-left
window = pygame.display.set_mode((800,600))
pygame.display.set_caption("Sully's Space Shooter")
icon = pygame.image.load('ship_icon.png')
pygame.display.set_icon(icon)

#Background image
background = pygame.image.load('background.png')

#Background Music
mixer.music.load("background.wav")
mixer.music.play(-1)

#Add bullet sound
bulletSound = mixer.Sound("laser.wav")

#Explosion enemy sound
explodeSound = mixer.Sound('explosion.wav')

#Load the spaceshit and add positions
playerShip = pygame.image.load('spaceship.png')
playerX = 380
playerY = 480
changeX = 0

#Add enemy element
enemyImage = []
enemyX = []
enemyY = []
changeEnemyX = []
changeEnemyY = []
numofEnemys = 6

for i in range(numofEnemys):
    enemyImage.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,100))
    changeEnemyX.append(2.2)
    changeEnemyY.append(40)

#Bullet
#Ready - Bullet is not on screen
#Fire - Bullet is moving and shows
bulletImage = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletChangeX = 0
bulletChangeY = 10
bulletState = "ready"


#Score
score = 0
score_font = pygame.font.SysFont("Anima",30)
gameover = pygame.font.SysFont("Anima",55)
def scoreUpdate(x,y):
    scoreVal = score_font.render("Score: " + str(score), True, (230,230,230))
    window.blit(scoreVal, (x,y))

def game_over():
    scoreVal = gameover.render("GAME OVER!", True, (230, 230, 230))
    window.blit(scoreVal, (260, 250))
def player(x,y):
    window.blit(playerShip, (x,y))
    #blit actually draws the element to the window

def enemy(x,y,i):
    window.blit(enemyImage[i], (x,y))
    #blit actually draws the element to the window

def bullet(x,y):
    #We set global so we can reassign it
    global bulletState
    bulletState = "fire"
    window.blit(bulletImage,(x+16,y+10))

def collision(x1,y1,x2,y2):
    distane = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    if distane<27:
        return True
    else:
        return False

pygame.display.flip()
game_running = True
while game_running:
    pygame.draw.line(window, (200, 200, 200), (0, 350), (800, 350))
    pygame.display.flip()
    # Change background color for window using .fill(rgb)
    # Keep it at the start we we add on top of it, we dont want to fill the elements
    window.fill((10, 5, 39))
    window.blit(background, (0,0))
    #Here we add every event that happens in the window it will be added to pygame.event.get()
    for event in pygame.event.get():
        #If the event QUIT close was activated then stop the loop
        if event.type == pygame.QUIT:
            game_running = False


        #If keystroke = press left or right add features
        if event.type == pygame.KEYDOWN:
            keys_pressed2 = pygame.key.get_pressed()
            if keys_pressed2[pygame.K_ESCAPE]:
                mixer.music.stop()
                exec(open('Welcome.py').read())
            if event.key == pygame.K_LEFT:
                changeX = -3
            elif event.key == pygame.K_RIGHT:
                changeX = 3
            elif event.key == pygame.K_SPACE:
                if bulletState == "ready":
                    #This gets the X coordinate of the spaceship
                    bulletX = playerX
                    bullet(bulletX,bulletY)
                    bulletSound.play()

        if event.type == pygame.KEYUP:
            if (event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT):
                changeX = 0


    playerX+=changeX
    # We call this here as we want it to show in all frames and never disappear

    #Hit the edges
    if playerX<=0:
        playerX = 0

    # 736 is used because the size of the image is 64px and 800-64 = 736
    elif playerX>=736:
        playerX = 736


    #Do this to all enemys
    for i in range(numofEnemys):

        #Game over is done
        if enemyY[i] > 300:
            for x in range(numofEnemys):
                enemyY[x] = 3000
                #This insures that all enemys disappear at gameover
            game_over()
            break


        enemyX[i]+=changeEnemyX[i]
        # Make enemy boundary
        #We use changeEnemyX, so that we can change that variable whenever it hits a point
        #We also use changeEnemyY=40 so that it moves down after hititng every edge
        if enemyX[i] <= 0:
            changeEnemyX[i] = 2.2
            enemyY[i] += changeEnemyY[i]
        elif enemyX[i] >= 736:
            changeEnemyX[i] = -2.2
            enemyY[i] += changeEnemyY[i]

        # Check collision
        if collision(enemyX[i], enemyY[i], bulletX, bulletY):
            explodeSound.play()
            # Reset the bullet
            bulletState = "ready"
            bulletY = 480
            score += 1


            # Reset enemy position
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(45, 150)
        enemy(enemyX[i], enemyY[i],i)

    #Bullet
    if bulletState=="fire":
        bulletY-=bulletChangeY
        bullet(bulletX,bulletY)

    if bulletY <= 0:
        bulletState = "ready"
        bulletY = 480

    scoreUpdate(10, 10)
    player(playerX, playerY)
    # Add exit text
    exit = score_font.render("Exit: Esc", True, (230, 230, 230))
    window.blit(exit, (680, 10))

    pygame.draw.line(window, (200, 200, 200), (0, 350), (800, 350))
    pygame.display.flip()

    pygame.display.update()
    # We have to add display.update whenever we make a change to update the window
