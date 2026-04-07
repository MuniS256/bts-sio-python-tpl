import pygame
from settings import GREEN, RED

def draw_hp_bar(surface, x, y, current_hp, max_hp):
    ratio = current_hp / max_hp
    pygame.draw.rect(surface, RED, (x, y, 200, 20)) # Barre rouge (fond)
    pygame.draw.rect(surface, GREEN, (x, y, 200 * ratio, 20)) # Barre verte

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y) # On centre le texte sur les coordonnées
    surface.blit(text_obj, text_rect)