import pygame
from pygame.locals import *
import numpy as np 
import time
import sys


WIDTH = 600
HEIGHT = 600
tam = 60

x = int(WIDTH / tam)
y = int(HEIGHT / tam)


GRAY = (0, 0, 0)
RED = (41, 41, 41)
WHITE = (255,255,255)


State = np.zeros((40,40))
NewState = np.copy(State)


pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))



def buscavecinos(M,i,j):
    count = 0
    print("Calculando vecinos")
    #Busca arriba
    if j > 1 :
        if M[i-1][j] == 1 :
            count +=1
    # Busca abajo
    if j < x-1 :
        if M[i+1][j] == 1 :
            count +=1
    #Izquierda
    if i > 1 :
        if M[i][j-1] == 1 :
            count +=1
    #derecha
    if j < x-1:
        if M[i][j+1] == 1 :
            count +=1
    #diagonal arriba izquierda
    if i > 1 and j > 1:
        if M[i-1][j-1] == 1 :
            count +=1
    #diagonl abajo izquierda
    if i < x-1 and j > 1:
        if M[i+1][j-1] == 1 :
            count +=1
    #diagonal arriba derecha
    if i > 1 and j < x-1:
        if M[i-1][j+1] == 1 :
            count +=1
    #diagonal abajo derecha
    if i < x-1 and j < x-1:
        if M[i+1][j+1] == 1 :
            count +=1
    
    return count



State[5][5] =1
State[5][6] =1
State[5][7] =1

while True:
    NewState = np.copy(State)
    screen.fill(GRAY)


    for eventos in pygame.event.get():
        if eventos.type == pygame.QUIT:
            sys.exit(0)

    for i in range(x):
        for j in range(y):
            vecinos = buscavecinos(State,i,j)
            if State[i][j] == 0 and vecinos == 3:
                NewState[i][j] = 1
            elif State[i][j] == 1 and (vecinos <2 or vecinos >3):
                NewState[i][j] = 0

    for i in range(x):
        for j in range(y):
            if(NewState[i][j] == 1):
                pygame.draw.rect(screen, WHITE, (j*tam,i*tam,tam, tam),0,1,1,1,1)
            else :
                pygame.draw.rect(screen, RED, (j*tam,i*tam,tam, tam),1)

    State = np.copy(NewState)
    time.sleep(0.5)
    pygame.display.flip()

    



