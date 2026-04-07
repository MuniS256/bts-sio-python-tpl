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

# Variables de contrôle
has_hit = False
game_state = "PLAYER_TURN" 
wait_timer = 0 

# 3. BOUCLE DE JEU
running = True
while running:
    # A. Gestion du temps (Delta Time)
    dt = clock.tick(FPS) / 1000.0 

    # B. Événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Action du joueur
        if game_state == "PLAYER_TURN":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                player.is_attacking = True
                player.target_x = boss.x - 50
                has_hit = False 
                game_state = "PLAYER_ATTACKING"

    # --- C. LOGIQUE DES TOURS & COLLISION ---
    
    # 1. État : Sonic attaque
    if game_state == "PLAYER_ATTACKING":
        if not has_hit and player.rect.colliderect(boss.rect):
            boss.take_damage(player.attack)
            has_hit = True
            player.is_attacking = False # Retour immédiat après impact
            
        # Si Sonic est revenu à sa place après l'impact
        if not player.is_attacking and player.x == player.original_x:
            wait_timer += dt
            if wait_timer >= 1.0:
                game_state = "ENEMY_TURN"
                wait_timer = 0

    # 2. État : Tour d'Eclipse (L'IA lance l'attaque)
    if game_state == "ENEMY_TURN":
        boss.is_attacking = True
        boss.target_x = player.x + 80 
        has_hit = False
        game_state = "ENEMY_ATTACKING"

    # 3. État : Eclipse attaque
    if game_state == "ENEMY_ATTACKING":
        if not has_hit and boss.rect.colliderect(player.rect):
            player.take_damage(boss.attack)
            has_hit = True
            boss.is_attacking = False # Retour immédiat
            
        # Si Eclipse est revenu à sa place
        if not boss.is_attacking and boss.x == boss.original_x:
            wait_timer += dt
            if wait_timer >= 1.0:
                game_state = "PLAYER_TURN"
                wait_timer = 0

    # --- D. MISE À JOUR ET AFFICHAGE ---
    
    # Mise à jour de la logique des classes
    player.update(dt)
    boss.update(dt)

    # Dessin
    screen.fill(BLACK) 
    
    player.draw(screen)
    boss.draw(screen)
    
    # Interface (Fixe en haut)
    draw_hp_bar(screen, 50, 50, player.hp, player.max_hp) 
    draw_hp_bar(screen, 550, 50, boss.hp, boss.max_hp) 

    pygame.display.flip()

pygame.quit()
sys.exit()