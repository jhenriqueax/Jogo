from ast import While
import random
from tkinter import font
from turtle import _Screen, Screen
import pygame

pygame.init()

x = 1280
y = 720

pos_monstro_x = 500
pos_monstro_y = 200

pos_nave_x = 100
pos_nave_y = 300

vel_bala_x = 0
pos_bala_x = pos_nave_x + 30
pos_bala_y = pos_nave_y + 42

pontos = 3

font = pygame.font.SysFont(None, 50)

Screen = pygame.display.set_mode((x, y))
pygame.display.set_caption('Meu jogo em Python')

back = pygame.image.load('imagens/fundo.jpg').convert_alpha()
back = pygame.transform.scale(back, (x, y))

monstro = pygame.image.load('imagens/monstro.png').convert_alpha()
monstro = pygame.transform.scale(monstro, (100, 50))

nave = pygame.image.load('imagens/nave.png').convert_alpha()
nave = pygame.transform.scale(nave, (150, 100))

bala = pygame.image.load('imagens/bala.png').convert_alpha()
bala = pygame.transform.scale(bala, (40, 15))


tiro = False
rodando = True


nave_rect = nave.get_rect()
monstro_rect = monstro.get_rect()
bala_rect = bala.get_rect()


def respawn():
    x = 1350
    y = random.randint(1, 640)
    return [x, y]


def respawn_bala():
    tiro = False
    respawn_bala_x = pos_nave_x + 30
    respawn_bala_y = pos_nave_y + 42
    vel_bala = 0
    return [respawn_bala_x, respawn_bala_y, tiro, vel_bala]


def colisao():
    global pontos
    if nave_rect.colliderect(monstro_rect) or monstro_rect.x == 60:
        pontos -= 1
        return True
    elif bala_rect.colliderect(monstro_rect):
        pontos += 1
        return True
    else:
        return False


while rodando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

    Screen.blit(back, (0, 0))

    rel_x = x % back.get_rect().width
    Screen.blit(back, (rel_x - back.get_rect().width, 0))
    if rel_x < 1280:
        Screen.blit(back, (rel_x, 0))

    # teclas

    tecla = pygame.key.get_pressed()
    if tecla[pygame.K_UP] and pos_nave_y > 0:
        pos_nave_y -= 2

        if not tiro:
            pos_bala_y -= 2

    if tecla[pygame.K_DOWN] and pos_nave_y < 670:
        pos_nave_y += 2

        if not tiro:
            pos_bala_y += 2

    if tecla[pygame.K_SPACE]:
        tiro = True
        vel_bala_x = 6

    if pos_monstro_x == 50 or colisao():
        pos_monstro_x = respawn()[0]
        pos_monstro_y = respawn()[1]

    if pos_bala_x > 1200:
        pos_bala_x, pos_bala_y, tiro, vel_bala_x = respawn_bala()

    if pontos == 0:
        rodando = False

    nave_rect.y = pos_nave_y
    nave_rect.x = pos_nave_x

    bala_rect.x = pos_bala_x
    bala_rect.y = pos_bala_y

    monstro_rect.x = pos_monstro_x
    monstro_rect.y = pos_monstro_y

    x -= 3
    pos_monstro_x -= 3
    pos_bala_x += vel_bala_x

    score = font.render(f'Pontos: {int(pontos)}', True, (0, 0, 0))
    Screen.blit(score, (50, 50))

    Screen.blit(monstro, (pos_monstro_x, pos_monstro_y))
    Screen.blit(bala, (pos_bala_x, pos_bala_y))
    Screen.blit(nave, (pos_nave_x, pos_nave_y))

    pygame.display.update()
