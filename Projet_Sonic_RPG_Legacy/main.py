# main.py
"""
from fighter_class import Fighter
from battle import Battle

def main():
    # Création des personnages
    player = Fighter("Sonic", hp=100, attack=20, energy=50)
    boss = Fighter("Eclipse", hp=120, attack=15, energy=50)

    # Création du combat
    battle = Battle(player, boss)

    # Lancer le combat
    battle.run()

if __name__ == "__main__":
    main()
"""
import pygame
import sys
from settings import *
from fighter_class import Fighter
from ui import draw_hp_bar

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Initialisation
player = Fighter("Sonic", 100, 20, 50, SONIC_SPRITE)
boss = Fighter("Eclipse", 120, 15, 50, ENEMY_SPRITE)

running = True
while running:
    # 1. Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE: # Attaque avec Espace
                boss.hp -= player.attack

    # 2. Dessin
    screen.fill(BLACK) # Fond
    
    # Affichage des sprites
    screen.blit(player.image, (100, 300))
    screen.blit(boss.image, (500, 300))
    
    # Affichage des barres de vie
    draw_hp_bar(screen, 100, 250, player.hp, player.max_hp)
    draw_hp_bar(screen, 500, 250, boss.hp, boss.max_hp)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()