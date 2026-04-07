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
screen = pygame.display.set_mode((WIDTH, HEIGHT)) # Utilise 1280x720 de settings.py
pygame.display.set_caption("Sonic RPG Legacy")
clock = pygame.time.Clock()

# --- CHARGEMENT DU BACKGROUND ---
try:
    # L'image sera automatiquement étirée en 1280x720
    background = pygame.image.load("Projet_Sonic_RPG_Legacy/assets/images/c_hill_zone.png").convert()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
except:
    background = pygame.Surface((WIDTH, HEIGHT))
    background.fill((20, 40, 20))

# 2. CRÉATION DES PERSONNAGES
# Ajustement des positions pour le 1280x720 :
# Sonic à gauche (x=200), Eclipse à droite (x=900), et les deux plus bas (y=400)
player = Fighter("Sonic", 100, 20, 50, SONIC_SPRITE, 200, 400)
boss = Fighter("Eclipse", 120, 15, 50, ENEMY_SPRITE, 900, 400)

# Variables de contrôle
has_hit = False
game_state = "PLAYER_TURN" 
wait_timer = 0 
menu_index = 0 
options = ["ATTACK", "MAGIC", "SPECIAL"]
winner = None 

# Polices (Un peu plus grandes pour la HD)
font_interface = pygame.font.SysFont("Arial", 28, bold=True)
font_tour = pygame.font.SysFont("Arial", 40, bold=True)
font_menu = pygame.font.SysFont("Verdana", 26, bold=True)

# 3. BOUCLE DE JEU
running = True
while running:
    dt = clock.tick(FPS) / 1000.0 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if game_state == "GAME_OVER":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                player.hp = player.max_hp
                boss.hp = boss.max_hp
                player.x, player.y = player.original_x, player.original_y
                boss.x, boss.y = boss.original_x, boss.original_y
                game_state = "PLAYER_TURN"
                winner = None

        if game_state == "PLAYER_TURN":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    menu_index = (menu_index - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    menu_index = (menu_index + 1) % len(options)
                elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    if menu_index == 0: 
                        player.is_attacking = True
                        player.target_x = boss.x - 100 # S'arrête un peu avant car l'écran est grand
                        has_hit = False 
                        game_state = "PLAYER_ATTACKING"

    # --- LOGIQUE TOURS & COLLISIONS ---
    if game_state == "PLAYER_ATTACKING":
        if not has_hit and player.rect.colliderect(boss.rect):
            boss.take_damage(player.attack)
            has_hit = True
            player.is_attacking = False 
            
        if not player.is_attacking and player.x == player.original_x:
            wait_timer += dt
            if wait_timer >= 0.8:
                game_state = "ENEMY_TURN"
                wait_timer = 0

    if game_state == "ENEMY_TURN":
        wait_timer += dt
        if wait_timer >= 0.7:
            boss.is_attacking = True
            boss.target_x = player.x + 100 
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
            if wait_timer >= 0.8:
                game_state = "PLAYER_TURN"
                wait_timer = 0

    if game_state != "GAME_OVER":
        if player.hp <= 0:
            game_state = "GAME_OVER"
            winner = "ECLIPSE"
        elif boss.hp <= 0:
            game_state = "GAME_OVER"
            winner = "SONIC"

    # --- AFFICHAGE ---
    player.update(dt)
    boss.update(dt)

    screen.blit(background, (0, 0)) 
    player.draw(screen)
    boss.draw(screen)
    
    # UI FLOTTANTE (Ajustée pour la nouvelle résolution)
    draw_hp_bar(screen, player.x, player.y - 50, player.hp, player.max_hp)
    draw_text(player.name, font_interface, WHITE, screen, player.x + 80, player.y - 65)
    
    draw_hp_bar(screen, boss.x, boss.y - 50, boss.hp, boss.max_hp)
    draw_text(boss.name, font_interface, RED, screen, boss.x + 80, boss.y - 65)

    if game_state == "GAME_OVER":
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        screen.blit(overlay, (0,0))
        
        msg = "VICTOIRE !" if winner == "SONIC" else "GAME OVER..."
        color = GREEN if winner == "SONIC" else RED
        draw_text(msg, font_tour, color, screen, WIDTH // 2, HEIGHT // 2 - 50)
        draw_text("APPUYEZ SUR 'R' POUR REJOUER", font_interface, WHITE, screen, WIDTH // 2, HEIGHT // 2 + 50)

    elif game_state == "PLAYER_TURN":
        # Menu décalé un peu plus dans le coin avec la nouvelle taille
        menu_rect = pygame.Rect(50, HEIGHT - 180, 220, 140)
        pygame.draw.rect(screen, (0, 0, 120), menu_rect, border_radius=12)
        pygame.draw.rect(screen, WHITE, menu_rect, 3, border_radius=12)
        
        for i, option in enumerate(options):
            txt_color = WHITE if i == menu_index else GRAY
            prefix = "> " if i == menu_index else "  "
            draw_text(prefix + option, font_menu, txt_color, screen, 140, HEIGHT - 145 + (i * 40))
        
        draw_text("CHOISIS TON ACTION", font_tour, WHITE, screen, WIDTH // 2, 80)

    elif "ENEMY" in game_state:
        draw_text("TOUR DE L'ENNEMI...", font_tour, RED, screen, WIDTH // 2, 80)

    pygame.display.flip()

pygame.quit()
sys.exit()