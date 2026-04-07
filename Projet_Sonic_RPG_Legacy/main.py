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
menu_index = 0 
options = ["ATTACK", "MAGIC", "SPECIAL"]
winner = None # Pour savoir qui a gagné à la fin

# Polices
font_interface = pygame.font.SysFont("Arial", 24, bold=True)
font_tour = pygame.font.SysFont("Arial", 32, bold=True)
font_menu = pygame.font.SysFont("Verdana", 22, bold=True)

# 3. BOUCLE DE JEU
running = True
while running:
    dt = clock.tick(FPS) / 1000.0 

    # B. Événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # --- LOGIQUE RESTART (Si GAME OVER) ---
        if game_state == "GAME_OVER":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                # Réinitialisation complète
                player.hp = player.max_hp
                boss.hp = boss.max_hp
                player.x, player.y = player.original_x, player.original_y
                boss.x, boss.y = boss.original_x, boss.original_y
                game_state = "PLAYER_TURN"
                winner = None

        # --- LOGIQUE MENU JOUEUR ---
        if game_state == "PLAYER_TURN":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    menu_index = (menu_index - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    menu_index = (menu_index + 1) % len(options)
                elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    if menu_index == 0: 
                        player.is_attacking = True
                        player.target_x = boss.x - 50
                        has_hit = False 
                        game_state = "PLAYER_ATTACKING"

    # --- C. LOGIQUE DES TOURS & COLLISIONS ---
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
        wait_timer += dt
        if wait_timer >= 0.7:
            boss.is_attacking = True
            boss.target_x = player.x + 80 
            has_hit = False
            game_state = "ENEMY_ATTACKING"
            wait_timer = 0

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

    # --- CHECK MORT (Vérification constante) ---
    if game_state != "GAME_OVER":
        if player.hp <= 0:
            game_state = "GAME_OVER"
            winner = "ECLIPSE"
        elif boss.hp <= 0:
            game_state = "GAME_OVER"
            winner = "SONIC"

    # --- D. MISE À JOUR ET AFFICHAGE ---
    player.update(dt)
    boss.update(dt)

    screen.fill(BLACK) 
    player.draw(screen)
    boss.draw(screen)
    
    # UI FLOTTANTE
    draw_hp_bar(screen, player.x, player.y - 40, player.hp, player.max_hp)
    draw_text(player.name, font_interface, WHITE, screen, player.x + 75, player.y - 55)
    draw_hp_bar(screen, boss.x, boss.y - 40, boss.hp, boss.max_hp)
    draw_text(boss.name, font_interface, RED, screen, boss.x + 75, boss.y - 55)

    # --- AFFICHAGE MENU OU ECRAN DE FIN ---
    if game_state == "GAME_OVER":
        # Voile noir transparent
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0,0))
        
        if winner == "SONIC":
            draw_text("VICTOIRE !", font_tour, (0, 255, 0), screen, WIDTH // 2, HEIGHT // 2 - 50)
            draw_text("ECLIPSE EST VAINCU", font_interface, WHITE, screen, WIDTH // 2, HEIGHT // 2 + 20)
        else:
            draw_text("GAME OVER...", font_tour, RED, screen, WIDTH // 2, HEIGHT // 2 - 50)
            draw_text("SONIC EST HS", font_interface, WHITE, screen, WIDTH // 2, HEIGHT // 2 + 20)
            
        draw_text("APPUYEZ SUR 'R' POUR RECOMMENCER", font_interface, (200, 200, 200), screen, WIDTH // 2, HEIGHT - 100)

    elif game_state == "PLAYER_TURN":
        # Dessin du cadre du menu
        menu_rect = pygame.Rect(30, HEIGHT - 160, 200, 130)
        pygame.draw.rect(screen, (0, 0, 100), menu_rect, border_radius=10)
        pygame.draw.rect(screen, WHITE, menu_rect, 2, border_radius=10)
        
        for i, option in enumerate(options):
            color = WHITE if i == menu_index else (100, 100, 100)
            prefix = "> " if i == menu_index else "  "
            draw_text(prefix + option, font_menu, color, screen, 110, HEIGHT - 130 + (i * 35))
        
        draw_text("CHOISIS TON ACTION", font_tour, WHITE, screen, WIDTH // 2, 50)

    elif game_state == "ENEMY_TURN" or game_state == "ENEMY_ATTACKING":
        draw_text("ATTENTION : ECLIPSE ATTAQUE !", font_tour, RED, screen, WIDTH // 2, 50)

    pygame.display.flip()

pygame.quit()
sys.exit()