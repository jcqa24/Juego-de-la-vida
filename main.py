import pygame
from pygame.locals import *
import numpy as np 
import time
import sys

def buscavecinos(M,i,j):
    print("Buscando vecinos.....")







WIDTH = 600
HEIGHT = 600
tam = 15



GRAY = (0, 0, 0)
RED = (41, 41, 41)
WHITE = (255,255,255)


State = np.zeros((40,40))
CopyState = State


pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))


while True:
    CopyState = State
    for eventos in pygame.event.get():
        if eventos.type == pygame.QUIT:
            sys.exit(0)

    screen.fill(GRAY)
    for i in range(40):
        for j in range(40):
            buscavecinos(State,i,j)
            if (State[i][j] == 1):
                pygame.draw.rect(screen, WHITE, (j*tam,i*tam,tam, tam))
            else:
                pygame.draw.rect(screen, RED, (j*tam,i*tam,tam, tam),1)
    pygame.display.flip()
    



