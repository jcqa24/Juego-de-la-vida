import pygame
from pygame.locals import *
import numpy as np 
import time
import sys


WIDTH = 600
HEIGHT = 700
tam = 60

x = int(WIDTH / tam)
y = int((HEIGHT - 100) / tam)


GRAY = (0, 0, 0)
RED = (41, 41, 41)
WHITE = (255, 255, 255)
BUTTON_BG = (100, 100, 100)
BUTTON_HOVER = (150, 150, 150)
BUTTON_TEXT = (255, 255, 255)


State = np.zeros((40, 40))
NewState = np.copy(State)


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game of Life")
font = pygame.font.Font(None, 24)


class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.is_hovered = False
    
    def draw(self, screen):
        color = BUTTON_HOVER if self.is_hovered else BUTTON_BG
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 2)
        text_surface = font.render(self.text, True, BUTTON_TEXT)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
    
    def update_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)


class Slider:
    def __init__(self, x, y, width, height, min_val, max_val, initial_val):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.dragging = False
        self.knob_radius = height // 2
    
    def draw(self, screen):
        pygame.draw.line(screen, WHITE, (self.x, self.y + self.height // 2), 
                        (self.x + self.width, self.y + self.height // 2), 2)
        
        knob_x = self.x + (self.value - self.min_val) / (self.max_val - self.min_val) * self.width
        pygame.draw.circle(screen, WHITE, (int(knob_x), self.y + self.height // 2), self.knob_radius)
        pygame.draw.circle(screen, BUTTON_HOVER, (int(knob_x), self.y + self.height // 2), self.knob_radius - 2)
        
        label = f"Velocidad: {self.value:.2f}s"
        text_surface = font.render(label, True, WHITE)
        screen.blit(text_surface, (self.x - 50, self.y - 25))
    
    def handle_click(self, pos):
        knob_x = self.x + (self.value - self.min_val) / (self.max_val - self.min_val) * self.width
        if ((pos[0] - knob_x) ** 2 + (pos[1] - self.y - self.height // 2) ** 2) <= self.knob_radius ** 2:
            self.dragging = True
            return True
        return False
    
    def update(self, pos):
        if self.dragging:
            relative_x = max(0, min(pos[0] - self.x, self.width))
            self.value = self.min_val + (relative_x / self.width) * (self.max_val - self.min_val)
    
    def stop_dragging(self):
        self.dragging = False


play_btn = Button(20, 620, 80, 40, "Play")
pause_btn = Button(110, 620, 80, 40, "Pausa")
next_btn = Button(200, 620, 80, 40, "Next")
clear_btn = Button(290, 620, 80, 40, "Limpiar")

speed_slider = Slider(380, 635, 200, 20, 0.1, 1.0, 0.5)

game_running = False
step_once = False
can_place = True
last_generation_time = 0
generation_count = 0



def buscavecinos(M, i, j):
    count = 0
    #Busca arriba
    if j > 0:
        if M[i-1][j] == 1:
            count += 1
    # Busca abajo
    if j < x-1:
        if M[i+1][j] == 1:
            count += 1
    #Izquierda
    if i > 0:
        if M[i][j-1] == 1:
            count += 1
    #derecha
    if j < x-1:
        if M[i][j+1] == 1:
            count += 1
    #diagonal arriba izquierda
    if i > 0 and j > 0:
        if M[i-1][j-1] == 1:
            count += 1
    #diagonl abajo izquierda
    if i < x-1 and j > 0:
        if M[i+1][j-1] == 1:
            count += 1
    #diagonal arriba derecha
    if i > 0 and j < x-1:
        if M[i-1][j+1] == 1:
            count += 1
    #diagonal abajo derecha
    if i < x-1 and j < x-1:
        if M[i+1][j+1] == 1:
            count += 1
    
    return count


def update_generation():
    global State, NewState
    NewState = np.copy(State)
    for i in range(x):
        for j in range(y):
            vecinos = buscavecinos(State, i, j)
            if State[i][j] == 0 and vecinos == 3:
                NewState[i][j] = 1
            elif State[i][j] == 1 and (vecinos < 2 or vecinos > 3):
                NewState[i][j] = 0
    State = np.copy(NewState)


# Tablero inicial vacío
# State[5][5] = 1
# State[5][6] = 1
# State[5][7] = 1

clock = pygame.time.Clock()

def toggle_cell(mouse_pos):
    """Activa/desactiva una celda si el clic está en el grid"""
    global State
    if mouse_pos[1] < HEIGHT - 100:  # Dentro del grid
        col = mouse_pos[0] // tam
        row = mouse_pos[1] // tam
        if 0 <= row < x and 0 <= col < y:
            State[row][col] = 1 - State[row][col]

while True:
    clock.tick(60)
    mouse_pos = pygame.mouse.get_pos()
    current_time = time.time()
    
    screen.fill(GRAY)
    
    # Actualizar hover state de botones
    play_btn.update_hover(mouse_pos)
    pause_btn.update_hover(mouse_pos)
    next_btn.update_hover(mouse_pos)
    clear_btn.update_hover(mouse_pos)
    
    # Actualizar slider si está siendo arrastrado
    speed_slider.update(mouse_pos)
    
    # Manejo de eventos
    for eventos in pygame.event.get():
        if eventos.type == pygame.QUIT:
            sys.exit(0)
        if eventos.type == pygame.MOUSEBUTTONDOWN:
            if play_btn.is_clicked(mouse_pos):
                game_running = True
                last_generation_time = current_time
            elif pause_btn.is_clicked(mouse_pos):
                game_running = False
            elif next_btn.is_clicked(mouse_pos):
                step_once = True
                game_running = False
            elif clear_btn.is_clicked(mouse_pos):
                State = np.zeros((40, 40))
                game_running = False
                generation_count = 0
            elif speed_slider.handle_click(mouse_pos):
                pass
            else:
                if not game_running:
                    toggle_cell(mouse_pos)
        elif eventos.type == pygame.MOUSEBUTTONUP:
            speed_slider.stop_dragging()
    
    # Actualizar generación con delay
    if game_running:
        if current_time - last_generation_time >= speed_slider.value:
            update_generation()
            generation_count += 1
            last_generation_time = current_time
    elif step_once:
        update_generation()
        generation_count += 1
        step_once = False
    
    # Dibujar grid
    for i in range(x):
        for j in range(y):
            if State[i][j] == 1:
                pygame.draw.rect(screen, WHITE, (j*tam, i*tam, tam, tam), 0, 1, 1, 1, 1)
            else:
                pygame.draw.rect(screen, RED, (j*tam, i*tam, tam, tam), 1)
    
    # Dibujar botones
    play_btn.draw(screen)
    pause_btn.draw(screen)
    next_btn.draw(screen)
    clear_btn.draw(screen)
    
    # Dibujar slider
    speed_slider.draw(screen)
    
    # Dibujar contador de generaciones
    gen_text = font.render(f"Generaciones: {generation_count}", True, WHITE)
    screen.blit(gen_text, (20, 10))
    
    pygame.display.flip()