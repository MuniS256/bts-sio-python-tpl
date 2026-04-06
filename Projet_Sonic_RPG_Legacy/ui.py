import pygame
from settings import GREEN, RED

def draw_hp_bar(surface, x, y, current_hp, max_hp):
    ratio = current_hp / max_hp
    pygame.draw.rect(surface, RED, (x, y, 200, 20)) # Barre rouge (fond)
    pygame.draw.rect(surface, GREEN, (x, y, 200 * ratio, 20)) # Barre verte