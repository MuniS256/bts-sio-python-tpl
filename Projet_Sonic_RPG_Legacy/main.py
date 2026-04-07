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

# 1. INITIALISATION
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sonic RPG Legacy")
clock = pygame.time.Clock()

# 2. CRÉATION DES PERSONNAGES
player = Fighter("Sonic", 100, 20, 50, SONIC_SPRITE, 100, 300)
boss = Fighter("Eclipse", 120, 15, 50, ENEMY_SPRITE, 550, 300)

# Variable pour empêcher de frapper 50 fois par seconde pendant la collision
has_hit = False

# 3. BOUCLE DE JEU
running = True
while running:
    # A. Gestion du temps (Delta Time)
    dt = clock.tick(FPS) / 1000.0 

    # B. Événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not player.is_attacking:
                player.is_attacking = True
                player.target_x = boss.x - 50
                has_hit = False # On réinitialise pour la nouvelle attaque

    # C. Mise à jour de la logique
    player.update(dt)
    boss.update(dt)

    # --- GESTION DE LA COLLISION ET DE L'IMPACT ---
    if player.is_attacking and not has_hit:
        if player.rect.colliderect(boss.rect):
            boss.take_damage(player.attack) # Dégâts + Flash Rouge
            has_hit = True                  # On bloque pour cette attaque
            # On peut même forcer Sonic à arrêter son dash ici
            player.is_attacking = False 

    # D. Affichage
    screen.fill(BLACK) 
    
    # On utilise les méthodes draw() pour gérer le flash rouge automatiquement
    player.draw(screen)
    boss.draw(screen)
    
    # Interface
    draw_hp_bar(screen, 100, 250, player.hp, player.max_hp)
    draw_hp_bar(screen, 500, 250, boss.hp, boss.max_hp)

    pygame.display.flip()

pygame.quit()
sys.exit()