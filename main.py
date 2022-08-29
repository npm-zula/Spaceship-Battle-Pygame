import pygame
import os
pygame.font.init()


HEALTH_FONT = pygame.font.SysFont("comicsans",40)
WINNER_FONT = pygame.font.SysFont("comicsans",90)


pygame.display.set_caption("Spaceship Wars")
WIDTH, HEIGHT = 900,500
WIN  = pygame.display.set_mode((WIDTH,HEIGHT))
WHITE = (59,35,52)
RED = (255,0,0)
YELLOW = (255,255,0)
FPS = 60
VEL = 3
BULLET_VEL = 5
MAX_BULLETS = 5

SPACESHIP_SIZE = (55,50)
BORDER = pygame.Rect(WIDTH//2 - 4, 0, 8, HEIGHT)

YELLOW_HIT = pygame.USEREVENT+1
RED_HIT = pygame.USEREVENT+2


YELLOWSHIP = pygame.image.load('Spaceship-Battle-Pygame/Assets/spaceship_yellow.png')
YELLOWSHIP = pygame.transform.scale(YELLOWSHIP,(SPACESHIP_SIZE))
YELLOWSHIP = pygame.transform.rotate(YELLOWSHIP,90)

REDSHIP = pygame.image.load('Spaceship-Battle-Pygame/Assets/spaceship_red.png')
REDSHIP = pygame.transform.scale(REDSHIP,(SPACESHIP_SIZE))
REDSHIP = pygame.transform.rotate(REDSHIP,270)

BACKGROUND = pygame.image.load('Spaceship-Battle-Pygame/Assets/space.png')
BACKGROUND = pygame.transform.scale(BACKGROUND,(WIDTH,HEIGHT))



def draw_window(red,yellow, redBullets, yellowBullets, redHealth, yellowHealth):
    WIN.blit(BACKGROUND,(0,0))
    pygame.draw.rect(WIN,(0,0,0),BORDER)

    redHealth_text = HEALTH_FONT.render("Health: " + str(redHealth), 1, (255,255,255))
    yellowhealth_text = HEALTH_FONT.render("Health: " + str(yellowHealth), 1, (255,255,255))

    WIN.blit(redHealth_text, (WIDTH - redHealth_text.get_width() - 10,10))
    WIN.blit(yellowhealth_text, (10,10))

    WIN.blit(YELLOWSHIP, (yellow.x,yellow.y))
    WIN.blit(REDSHIP, (red.x,red.y))



    for bullet in redBullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellowBullets:
        pygame.draw.rect(WIN,YELLOW,bullet)

    pygame.display.update()


def shipMovementYellow(keysPressed,obj):
    if keysPressed[pygame.K_a] and obj.x - VEL > 0: # left
        obj.x -= VEL
            
    if keysPressed[pygame.K_w] and obj.y - VEL > 0: # up
        obj.y -= VEL

    if keysPressed[pygame.K_d] and obj.x + VEL + obj.width < BORDER.x : # right
        obj.x += VEL
        
    if keysPressed[pygame.K_s] and obj.y + VEL + obj.height < HEIGHT: # down
        obj.y += VEL
    
def shipMovementRed(keysPressed, obj):
    # RED
    if keysPressed[pygame.K_LEFT] and obj.x - VEL > BORDER.x  : # left
        obj.x -= VEL
            
    if keysPressed[pygame.K_UP] and obj.y - VEL > 0: # up
        obj.y -= VEL

    if keysPressed[pygame.K_RIGHT] and obj.x + VEL < WIDTH - obj.width : # right
        obj.x += VEL
        
    if keysPressed[pygame.K_DOWN] and obj.y + VEL + obj.height < HEIGHT: # down
        obj.y += VEL

def handleBullets(yellowBullets,redBullets, yellow, red):
    for bullet in yellowBullets:
        bullet.x += BULLET_VEL
        if(red.colliderect(bullet)):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellowBullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellowBullets.remove(bullet)

    for bullet in redBullets:
        bullet.x -= BULLET_VEL
        if(yellow.colliderect(bullet)):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            redBullets.remove(bullet)
        elif bullet.x < 0:
            redBullets.remove(bullet)

def winner(text):
    text = WINNER_FONT.render(text,1, (255,255,255))
    WIN.blit(text,(WIDTH//2 - text.get_width()/2, HEIGHT//2 - text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(6000)

def main():
    yellow = pygame.Rect(100,200, SPACESHIP_SIZE[0], SPACESHIP_SIZE[1])
    red = pygame.Rect(700,200, SPACESHIP_SIZE[0], SPACESHIP_SIZE[1])

    redBullets = []
    yellowBullets = []

    redHealth = 10
    yellowHealth = 10

    clock = pygame.time.Clock() 
    run = True

    while run:
        clock.tick(FPS)    
 
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellowBullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width//2, yellow.y + yellow.height//2, 10, 5)
                    yellowBullets.append(bullet)

                if event.key == pygame.K_RCTRL and len(redBullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height//2, 10, 5)
                    redBullets.append(bullet)

            if event.type == RED_HIT:
                redHealth -=1

            if event.type == YELLOW_HIT:
                yellowHealth -=1

        announce = ""

        if redHealth <= 0:
           announce = "YELLOW WINS"

        if yellowHealth <= 0:
            announce = "RED WINS"

        if announce != "":
            winner(announce)
            break
            

        keysPressed = pygame.key.get_pressed()
        shipMovementYellow(keysPressed,yellow)
        shipMovementRed(keysPressed,red)        
        handleBullets(yellowBullets,redBullets,yellow,red)
        draw_window(red,yellow, redBullets, yellowBullets, redHealth, yellowHealth)  
          
    main()
    

if __name__ ==  "__main__":
    main()