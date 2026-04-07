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
from ui import draw_hp_bar, draw_text

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

# Police pour les noms et l'interface
font_interface = pygame.font.SysFont("Arial", 24, bold=True)
font_tour = pygame.font.SysFont("Arial", 32, bold=True)

# 3. BOUCLE DE JEU
running = True
while running:
    dt = clock.tick(FPS) / 1000.0 

    # B. Événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if game_state == "PLAYER_TURN":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                player.is_attacking = True
                player.target_x = boss.x - 50
                has_hit = False 
                game_state = "PLAYER_ATTACKING"

    # --- C. LOGIQUE DES TOURS & COLLISION ---
    if game_state == "PLAYER_ATTACKING":
        if not has_hit and player.rect.colliderect(boss.rect):
            boss.take_damage(player.attack)
            has_hit = True
            player.is_attacking = False 
            
        if not player.is_attacking and player.x == player.original_x:
            wait_timer += dt
            if wait_timer >= 1.0:
                game_state = "ENEMY_TURN"
                wait_timer = 0

    if game_state == "ENEMY_TURN":
        boss.is_attacking = True
        boss.target_x = player.x + 80 
        has_hit = False
        game_state = "ENEMY_ATTACKING"

    if game_state == "ENEMY_ATTACKING":
        if not has_hit and boss.rect.colliderect(player.rect):
            player.take_damage(boss.attack)
            has_hit = True
            boss.is_attacking = False 
            
        if not boss.is_attacking and boss.x == boss.original_x:
            wait_timer += dt
            if wait_timer >= 1.0:
                game_state = "PLAYER_TURN"
                wait_timer = 0

    # --- D. MISE À JOUR ET AFFICHAGE ---
    player.update(dt)
    boss.update(dt)

    screen.fill(BLACK) 
    
    player.draw(screen)
    boss.draw(screen)
    
    # --- UI FLOTTANTE (Suit les personnages) ---
    
    # Barre et Nom de Sonic
    # On décale de -40 en Y pour être au-dessus de la tête
    draw_hp_bar(screen, player.x, player.y - 40, player.hp, player.max_hp)
    draw_text(player.name, font_interface, WHITE, screen, player.x + 75, player.y - 55)

    # Barre et Nom d'Eclipse
    draw_hp_bar(screen, boss.x, boss.y - 40, boss.hp, boss.max_hp)
    draw_text(boss.name, font_interface, RED, screen, boss.x + 75, boss.y - 55)

    # --- MESSAGE DE TOUR (En bas au centre pour libérer le haut) ---
    if game_state == "PLAYER_TURN":
        draw_text("À TOI DE JOUER !", font_tour, WHITE, screen, WIDTH // 2, HEIGHT - 100)
    elif game_state == "ENEMY_TURN" or game_state == "ENEMY_ATTACKING":
        draw_text("TOUR D'ECLIPSE...", font_tour, RED, screen, WIDTH // 2, HEIGHT - 100)

    pygame.display.flip()

pygame.quit()
sys.exit()