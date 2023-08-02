from socket import *
import json
import pygame
import math

pygame.init()

# init
screen: pygame.Surface = pygame.display.set_mode((32*30, 32*17))
var: tuple[str, int, int, int] = ("alpha", 0, 0, 1)
pygame.display.set_caption(f"sfg2 {var[0]} {var[1]}.{var[2]}.{var[3]} by newkini")
playerImg = pygame.image.load("./player.png")
clock = pygame.time.Clock()
is_running = True

playerPos = [10, 10]
dir = ""  # Initialize the 'dir' variable

tilemap = [[0 for _ in range(0, 30)] for _ in range(0, 17)]

speed = 1

clientSock = socket(AF_INET, SOCK_STREAM)
clientSock.connect(('127.0.0.1', 13659))

nick = "newkini"
game = "testgame"
clientSock.send(json.dumps([game, nick]).encode())

# main loop
while is_running:
    clock.tick(60)

    # update var
    mouse_pos = pygame.mouse.get_pos()

    # events
    for event in pygame.event.get():  # 키입력 감지
        # 나가기
        if event.type == pygame.QUIT:  # 나가기 버튼 눌럿을때
            is_running = False  # 와일문 나가기
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                dir = "l"
            elif event.key == pygame.K_RIGHT:
                dir = "r"
            elif event.key == pygame.K_UP:
                dir = "u"
            elif event.key == pygame.K_DOWN:
                dir = "d"
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                dir = ""
            elif event.key == pygame.K_RIGHT:
                dir = ""
            elif event.key == pygame.K_UP:
                dir = ""
            elif event.key == pygame.K_DOWN:
                dir = "" 
    # 플래이어
    # 움직이기
    if dir == "l":
        playerPos[0] -= speed
        clientSock.send(json.dumps(playerPos).encode())
    elif dir == "r":
        playerPos[0] += speed
        clientSock.send(json.dumps(playerPos).encode())
    elif dir == "u":
        playerPos[1] -= speed
        clientSock.send(json.dumps(playerPos).encode())
    elif dir == "d":
        playerPos[1] += speed
        clientSock.send(json.dumps(playerPos).encode())

    # tile
    tilepos = pygame.Vector2(0, 0)
    for line in tilemap:
        for tile in line:
            if tile == 0:
                screen.blit(pygame.image.load("./up.png"), tilepos*32)
            tilepos.x += 1
        tilepos.y += 1
        tilepos.x = 0

    screen.blit(playerImg, playerPos)

    # update
    pygame.display.update()
    
pygame.quit()