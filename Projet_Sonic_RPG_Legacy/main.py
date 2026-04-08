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

# --- CHARGEMENT DES ASSETS ---
try:
    background = pygame.image.load("Projet_Sonic_RPG_Legacy/assets/images/c_hill_zone.png").convert()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
except:
    background = pygame.Surface((WIDTH, HEIGHT))
    background.fill((20, 40, 20))

# 2. CRÉATION DES PERSONNAGES
player = Fighter("Sonic", 100, 20, 50, SONIC_SPRITE, 200, 400, frames=1)
boss = Fighter("Eclipse", 120, 15, 50, ENEMY_SPRITE, 900, 400, frames=1)

# --- VARIABLES MENU & HISTOIRE ---
game_state = "START_MENU" 
story_index = 0
story_lines = [
    "Sonic: Eclipse ! Rend-moi l'Emeraude du Chaos tout de suite !",
    "Eclipse: Tu arrives trop tard, hérisson bleu...",
    "Eclipse: La puissance du vide est déjà en moi !",
    "Sonic: On va voir si tu tiens encore debout après ça !"
]

# Contrôle du combat
has_hit = False
wait_timer = 0 
menu_index = 0 
options = ["ATTACK", "MAGIC", "SPECIAL"]
winner = None 

# --- ÉTAPE 2 : Variables Magic ---
magic_options = ["SOIN (10 MP)", "CHAOS BLAST (20 MP)", "RETOUR"]
in_magic_menu = False
magic_index = 0

# Polices
font_interface = pygame.font.SysFont("Arial", 28, bold=True)
font_tour = pygame.font.SysFont("Arial", 40, bold=True)
font_menu = pygame.font.SysFont("Verdana", 26, bold=True)
font_title = pygame.font.SysFont("Verdana", 60, bold=True)

# 3. BOUCLE DE JEU
running = True
while running:
    dt = clock.tick(FPS) / 1000.0 
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if game_state == "START_MENU":
                if event.key == pygame.K_SPACE:
                    game_state = "STORY"
            
            elif game_state == "STORY":
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    story_index += 1
                    if story_index >= len(story_lines):
                        game_state = "PLAYER_TURN"

            elif game_state == "GAME_OVER":
                if event.key == pygame.K_r:
                    player.hp = player.max_hp
                    player.display_hp = player.max_hp
                    player.energy = 50 # Reset Energie
                    boss.hp = boss.max_hp
                    boss.display_hp = boss.max_hp
                    player.x, player.y = player.original_x, player.original_y
                    boss.x, boss.y = boss.original_x, boss.original_y
                    story_index = 0
                    game_state = "START_MENU"
                    winner = None

            elif game_state == "PLAYER_TURN":
                # --- ÉTAPE 2 : Logique Menu Magic ---
                if not in_magic_menu:
                    if event.key == pygame.K_UP:
                        menu_index = (menu_index - 1) % len(options)
                    elif event.key == pygame.K_DOWN:
                        menu_index = (menu_index + 1) % len(options)
                    elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        if menu_index == 0: # ATTACK
                            player.is_attacking = True
                            player.target_x = boss.x - 100 
                            has_hit = False 
                            game_state = "PLAYER_ATTACKING"
                        elif menu_index == 1: # Ouvrir le menu MAGIC
                            in_magic_menu = True
                else:
                    if event.key == pygame.K_UP:
                        magic_index = (magic_index - 1) % len(magic_options)
                    elif event.key == pygame.K_DOWN:
                        magic_index = (magic_index + 1) % len(magic_options)
                    elif event.key == pygame.K_ESCAPE: # Touche pour revenir en arrière
                        in_magic_menu = False
                    elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        if magic_index == 0: # SOIN
                            if player.use_energy(10):
                                player.heal(30)
                                in_magic_menu = False
                                game_state = "ENEMY_TURN"
                        elif magic_index == 1: # CHAOS BLAST
                            if player.use_energy(20):
                                boss.take_damage(40)
                                in_magic_menu = False
                                game_state = "ENEMY_TURN"
                        elif magic_index == 2: # RETOUR
                            in_magic_menu = False

    # --- LOGIQUE DE COMBAT (Identique) ---
    if game_state == "PLAYER_ATTACKING":
        if not has_hit and player.rect.colliderect(boss.rect):
            boss.take_damage(player.attack)
            has_hit = True
            player.is_attacking = False 
        if not player.is_attacking and player.x == player.original_x:
            wait_timer += dt
            if wait_timer >= 0.8:
                game_state = "ENEMY_TURN"; wait_timer = 0

    if game_state == "ENEMY_TURN":
        wait_timer += dt
        if wait_timer >= 0.7:
            boss.is_attacking = True
            boss.target_x = player.x + 100; has_hit = False
            game_state = "ENEMY_ATTACKING"; wait_timer = 0

    if game_state == "ENEMY_ATTACKING":
        if not has_hit and boss.rect.colliderect(player.rect):
            player.take_damage(boss.attack); has_hit = True
            boss.is_attacking = False 
        if not boss.is_attacking and boss.x == boss.original_x:
            wait_timer += dt
            if wait_timer >= 0.8:
                game_state = "PLAYER_TURN"; wait_timer = 0

    if game_state not in ["START_MENU", "STORY", "GAME_OVER"]:
        if player.hp <= 0: game_state = "GAME_OVER"; winner = "ECLIPSE"
        elif boss.hp <= 0: game_state = "GAME_OVER"; winner = "SONIC"

    # --- AFFICHAGE ---
    player.update(dt)
    boss.update(dt)
    screen.blit(background, (0, 0)) 

    if game_state == "START_MENU":
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(150); overlay.fill(BLACK)
        screen.blit(overlay, (0,0))
        draw_text("SONIC RPG LEGACY", font_title, (0, 200, 255), screen, WIDTH // 2, HEIGHT // 3)
        if (current_time // 500) % 2 == 0:
            draw_text("APPUYEZ SUR ESPACE", font_interface, WHITE, screen, WIDTH // 2, HEIGHT // 2 + 50)

    elif game_state == "STORY":
        player.draw(screen)
        boss.draw(screen)
        dialog_rect = pygame.Rect(50, HEIGHT - 150, WIDTH - 100, 120)
        pygame.draw.rect(screen, (0, 0, 0), dialog_rect)
        pygame.draw.rect(screen, WHITE, dialog_rect, 3)
        draw_text(story_lines[story_index], font_interface, WHITE, screen, WIDTH // 2, HEIGHT - 90)

    else:
        player.draw(screen)
        boss.draw(screen)
        draw_hp_bar(screen, player.x, player.y - 50, player.display_hp, player.max_hp)
        draw_text(player.name, font_interface, WHITE, screen, player.x + 80, player.y - 65)
        draw_hp_bar(screen, boss.x, boss.y - 50, boss.display_hp, boss.max_hp)
        draw_text(boss.name, font_interface, RED, screen, boss.x + 80, boss.y - 65)

        # --- ÉTAPE 3 : Affichage des Menus Dynamiques ---
        if game_state == "PLAYER_TURN":
            menu_rect = pygame.Rect(50, HEIGHT - 180, 280, 140)
            pygame.draw.rect(screen, (0, 0, 120), menu_rect, border_radius=12)
            pygame.draw.rect(screen, WHITE, menu_rect, 3, border_radius=12)
            
            current_menu = magic_options if in_magic_menu else options
            current_idx = magic_index if in_magic_menu else menu_index
            
            for i, opt in enumerate(current_menu):
                txt_color = WHITE if i == current_idx else GRAY
                prefix = "> " if i == current_idx else "  "
                draw_text(prefix + opt, font_menu, txt_color, screen, 190, HEIGHT - 145 + (i * 40))
            
            # Titre et Points de Magie
            title_msg = "QUEL SORT ?" if in_magic_menu else "CHOISIS TON ACTION"
            draw_text(title_msg, font_tour, WHITE, screen, WIDTH // 2, 80)
            draw_text(f"MP: {player.energy}", font_interface, (0, 200, 255), screen, 190, HEIGHT - 210)

        if game_state == "GAME_OVER":
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(200); overlay.fill(BLACK); screen.blit(overlay, (0,0))
            msg = "VICTOIRE !" if winner == "SONIC" else "GAME OVER..."
            draw_text(msg, font_tour, GREEN if winner == "SONIC" else RED, screen, WIDTH // 2, HEIGHT // 2 - 50)
            draw_text("APPUYEZ SUR 'R' POUR REJOUER", font_interface, WHITE, screen, WIDTH // 2, HEIGHT // 2 + 50)

    pygame.display.flip()

pygame.quit()
sys.exit()