import random
import sys
import pygame
from pygame.locals import *


# Global variables

FPS = 32
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = SCREENHEIGHT*0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
BACKGROUND = "gallery/sprites/background.png"
PLAYER = "gallery/sprites/bird.png"
PIPE = "gallery/sprites/pipe.png"
ALIVE=3

def welcomeScreen():
    playerx = int(SCREENWIDTH/5)
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2)
    messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width())/2)
    messagey = int(SCREENHEIGHT*0.13)
    basex = 0
    while True:
        for event in pygame.event.get():
            # if user clicks on cross button, close the game
            if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # If the user presses space or up key, start the game for them
            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'], (0, 0))    
                SCREEN.blit(GAME_SPRITES['message'], (messagex,messagey ))    
                SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))    
                SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))    
                pygame.display.update()
                FPSCLOCK.tick(FPS)

def mainGame():
    global ALIVE
    score = 0
    player_x = int(SCREENWIDTH/5)
    player_y = int(SCREENHEIGHT/2)
    basex = 0
    Alive_meter = myfont.render(f"Alive:{ALIVE}", False, (0, 0, 0))
    Score_meter = myfont.render(f"Score:{score}", False, (0, 0, 0))
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    upperPipes = [{"x": SCREENWIDTH+200, "y": newPipe1[0]["y"]},
                  {"x": SCREENWIDTH+200+(SCREENWIDTH/2), "y": newPipe2[0]["y"]},
                  ]
    lowerPipes = [{"x": SCREENWIDTH+200, "y": newPipe1[1]["y"]},
                  {"x": SCREENWIDTH+200+(SCREENWIDTH/2), "y": newPipe2[1]["y"]},
                  ]
    pipVelX = -4
    playerVelY = -8
    playerMaxVelY = 10
    playerAccY = 1
    playerFlapacc = -8
    playerFlapped = False
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.type == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYUP:
                if player_y > 0:
                    playerVelY = playerFlapacc
                    playerFlapped = True
                    GAME_SOUNDS["wing"].play()

        crashTest = isCollide(player_x, player_y, upperPipes, lowerPipes)
        if crashTest:
            print(ALIVE)
            if ALIVE>1:
                ALIVE-=1
                return mainGame()
            else:
                ALIVE+=3
                return 
        playerMidPos = player_x+GAME_SPRITES['player'].get_width()/2
        for pipe in upperPipes:
            pipMidPos = pipe["x"]+GAME_SPRITES["pipe"][0].get_width()/2
            if pipMidPos <= playerMidPos <pipMidPos+4:
                score += 1
                GAME_SOUNDS["point"].play()
                Score_meter = myfont.render(f"Score:{score}", False, (0, 0, 0))
                print(f"your point is {score} ")
        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY
        if playerFlapped:
            playerFlapped = False
        playerHeight = GAME_SPRITES["player"].get_height()
        player_y = player_y+min(playerVelY, GROUNDY-player_y-playerHeight)

        for upperpipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperpipe["x"] += pipVelX
            lowerPipe["x"] += pipVelX

        if 0<upperPipes[0]["x"] <5:
            newpipe=getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])
        if upperPipes[0]["x"]< -GAME_SPRITES["pipe"][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)
        
        SCREEN.blit(GAME_SPRITES["background"], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES["pipe"][0], (upperPipe["x"], upperPipe["y"]))
            SCREEN.blit(GAME_SPRITES["pipe"][1], (lowerPipe["x"], lowerPipe["y"]))
        SCREEN.blit(Alive_meter,(0,0))
        SCREEN.blit(Score_meter,(210,0))
        SCREEN.blit(GAME_SPRITES["base"], (basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES["player"], (player_x, player_y))
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def isCollide(playerx, playery, upperPipes, lowerPipes):
    if playery> GROUNDY - 25  or playery<0:
        GAME_SOUNDS['hit'].play()
        return True
    
    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True

    for pipe in lowerPipes:
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True

    return False


def getRandomPipe():
    pipeHeight = GAME_SPRITES["pipe"][0].get_height()
    offset = int(SCREENHEIGHT/4)+random.randint(0,5)
    y2 = random.randrange(
        offset, int(SCREENHEIGHT-GAME_SPRITES["base"].get_height()-1.2*offset))
    pipex = SCREENWIDTH+15
    y1 = pipeHeight-y2+offset
    pipe = [{"x": pipex, "y": -y1},
            {"x": pipex, "y": y2}
            ]
    return pipe


if __name__ == "__main__":
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.font.init() 
    myfont = pygame.font.SysFont('Times', 20,"bold")

    pygame.display.set_caption("FLAPPY BIRD")
    GAME_SPRITES["player"] = pygame.image.load(PLAYER).convert_alpha()
    GAME_SPRITES["background"] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES["message"] = pygame.image.load(
        "gallery/sprites/message.jpg").convert_alpha()
    GAME_SPRITES["base"] = pygame.image.load(
        "gallery/sprites/base.png").convert_alpha()
    GAME_SPRITES["pipe"] = (pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
                            pygame.image.load(PIPE).convert_alpha())

    GAME_SOUNDS['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')

    while True:
        welcomeScreen()
        mainGame()
