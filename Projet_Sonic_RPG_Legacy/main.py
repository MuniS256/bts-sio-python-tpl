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

# --- Etats du jeu ---
# "PLAYER_TURN", "PLAYER_ATTACKING", "ENEMY_TURN", "ENEMY_ATTACKING"
game_state = "PLAYER_TURN" 
wait_timer = 0 # Pour laisser une petite pause entre les actions

# 3. BOUCLE DE JEU
running = True
while running:
    # A. Gestion du temps (Delta Time)
    dt = clock.tick(FPS) / 1000.0 

    # B. Événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # On ne peut attaquer QUE si c'est le tour du joueur et qu'il est immobile
        if game_state == "PLAYER_TURN":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if event.key == pygame.K_SPACE and not player.is_attacking:
                    player.is_attacking = True
                    player.target_x = boss.x - 50
                    has_hit = False # On réinitialise pour la nouvelle attaque
                    game_state = "PLAYER_ATTACKING"

# --- B. LOGIQUE DES TOURS ---
    
    # 1. Si Sonic a fini son attaque et est revenu à sa place
    if game_state == "PLAYER_ATTACKING" and not player.is_attacking and player.x == player.original_x:
        wait_timer += dt
        if wait_timer >= 1.0: # Pause de 1 seconde pour le suspense
            game_state = "ENEMY_TURN"
            wait_timer = 0

    # 2. Tour d'Eclipse (L'IA décide d'attaquer)
    if game_state == "ENEMY_TURN":
        boss.is_attacking = True
        boss.target_x = player.x + 80 # Eclipse fonce vers la gauche !
        has_hit = False
        game_state = "ENEMY_ATTACKING"

    # 3. Si Eclipse a fini son attaque
    if game_state == "ENEMY_ATTACKING" and not boss.is_attacking and boss.x == boss.original_x:
        wait_timer += dt
        if wait_timer >= 1.0:
            game_state = "PLAYER_TURN"
            wait_timer = 0

    # --- C. COLLISIONS (Mise à jour) ---
    if player.is_attacking and not has_hit and player.rect.colliderect(boss.rect):
        boss.take_damage(player.attack)
        has_hit = True
        player.is_attacking = False # Il repart direct après l'impact

    if boss.is_attacking and not has_hit and boss.rect.colliderect(player.rect):
        player.take_damage(boss.attack)
        has_hit = True
        boss.is_attacking = False

    # C. Mise à jour de la logique
    player.update(dt)
    boss.update(dt)

    screen.fill(BLACK)
    player.draw(screen)
    boss.draw(screen)
    # ... (tes barres de vie)
    pygame.display.flip()

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