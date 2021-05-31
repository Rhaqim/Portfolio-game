import pygame
import random
import math

# initalise the pygame
pygame.init()

# create a screen
screen = pygame.display.set_mode((800,600))

# background
background = pygame.image.load('level1bk.jpg')

# title and icon
pygame.display.set_caption("Hackerman Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# player
playerimg = pygame.image.load('hacker.png')
playerx = 370
playery = 480
playerx_change = 0
playery_change = 0

#enemy 
enemyimg = []
enemyx = []
enemyy = []
enemyx_change = []
enemyy_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyimg.append(pygame.image.load('foot-clan.png'))
    enemyx.append(random.randint(0,760))
    enemyy.append(random.randint(50,150))
    enemyx_change.append(0.3)
    enemyy_change.append(10)

# bullet
bulletimg = pygame.image.load('bullet.png')
bulletx = 0
bullety = 480
bulletx_change = 0
bullety_change = 0.5
bullet_state = 'ready' #ready means you can't see the bullet on the screen, when it is set to fire, you can then see it


#score 
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textx = 10
texty = 10

def showscore(x,y):
    score = font.render("Score:" + str(score_value), True, (255,0,0))
    screen.blit(score, (x,y))

def player(x,y):
    screen.blit(playerimg, (x,y))

def enemy(x,y,i):
    screen.blit(enemyimg[i ], (x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletimg,(x+16,y+10))

def isCollision(enemyx, enemyy, bulletx, bullety):
    distance = math.sqrt((math.pow(enemyx - bulletx,2)) + (math.pow(enemyy - bullety,2)))
    if distance < 27:
        return True
    else:
        return False

# game loop
running = True
while running:
    # setting the background color, use RGB
    screen.fill((255, 152, 162))

    #background image
    screen.blit(background, (0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed checked if its right or left
        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_LEFT:
                playerx_change = -0.3
            
            if event.key == pygame.K_RIGHT:
                playerx_change = +0.3

            if event.key == pygame.K_UP:
                playery_change = -0.3
            
            if event.key == pygame.K_DOWN:
                playery_change = +0.3
            
            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bulletx = playerx
                    fire_bullet(bulletx, bullety)
                
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerx_change = 0
            
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    playery_change = 0
                
        
    

    playerx += playerx_change
    playery += playery_change

    # setting the boundaries for players left and right
    if playerx <= 0:
        playerx = 0
    if playerx >= 736:
        playerx = 736

    #setting the boundaries for up and down
    if playery <= 0:
        playery = 0
    if playery >= 536:
        playery = 536


    # setting the boundaries for enemy left and right
    for i in range(num_of_enemies):
        enemyx[i] += enemyx_change[i]
        if enemyx[i] <= 0:
            enemyx_change[i] = 0.2
            enemyy[i] += enemyy_change[i]
        elif enemyx[i] >= 736:
            enemyx_change[i] = -0.2
            enemyy[i] += enemyy_change[i]

        #collision on the enemy
        collision = isCollision(enemyx[i], enemyy[i], bulletx, bullety)
        if collision:
            bullety = 480
            bullet_state = 'ready'
            enemyx[i] = random.randint(0,760)
            enemyy[i] = random.randint(50,150)
            score_value += 1

        enemy(enemyx[i], enemyy[i], i)

        collision = isCollision(enemyx[i], enemyy[i], playerx, playery)
        if collision:
            playerx = 370
            playery = 480
            enemyx[i] = random.randint(0,760)
            enemyy[i] = random.randint(50,150)
            score_value -= 1

    # bullet movement
    if bullety <= 0:
        bullety = 480
        bullet_state = 'ready'

    if bullet_state == 'fire':
        fire_bullet(bulletx,bullety)
        bullety -= bullety_change


    # collisiom
    

    
    player(playerx, playery)
    showscore(textx,texty)

    #always update after the state has been changed e.g drawing the player
    pygame.display.update() 