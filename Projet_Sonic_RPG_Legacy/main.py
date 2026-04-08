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
import random
from settings import *
from fighter_class import Fighter
# Importe bien negative_surface depuis ton fichier ui.py
from ui import draw_hp_bar, draw_mana_bar, draw_text, negative_surface 

# 1. INITIALISATION
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT)) 
pygame.display.set_caption("Sonic RPG Legacy")
clock = pygame.time.Clock()

# --- CHARGEMENT DES ASSETS ---
try:
    background = pygame.image.load("Projet_Sonic_RPG_Legacy/assets/images/c_hill_zone.png").convert()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    # ON PRÉ-CALCULE LE NÉGATIF ICI
    bg_negative = negative_surface(background.copy())
except:
    background = pygame.Surface((WIDTH, HEIGHT))
    background.fill((20, 40, 20))
    bg_negative = pygame.Surface((WIDTH, HEIGHT))
    bg_negative.fill((200, 200, 200)) # Fond clair en fallback pour le négatif

# 2. CRÉATION DES PERSONNAGES
player = Fighter("Sonic", 100, 20, 50, SONIC_SPRITE, 200, 400, frames=1)
boss = Fighter("Eclipse", 120, 15, 50, ENEMY_SPRITE, 900, 400, frames=1)

# --- VARIABLES DE CONTRÔLE ---
game_state = "START_MENU" 
story_index = 0
story_lines = [
    "Sonic: Eclipse ! Rend-moi l'Emeraude du Chaos tout de suite !",
    "Eclipse: Tu arrives trop tard, hérisson bleu...",
    "Eclipse: La puissance du vide est déjà en moi !",
    "Sonic: On va voir si tu tiens encore debout après ça !"
]

has_hit = False
wait_timer = 0 
menu_index = 0 
options = ["ATTACK", "MAGIC", "SPECIAL"]
winner = None 

# Variables Menus
magic_options = ["SOIN (10 MP)", "CHAOS BLAST (20 MP)", "RETOUR"]
in_magic_menu = False
magic_index = 0

special_options = ["SUPER DASH (40 MP)", "RETOUR"]
in_special_menu = False
special_index = 0

# --- EFFETS ---
flash_effect_timer = 0
flash_color = (255, 255, 255)
# NOUVELLES VARIABLES POUR L'EFFET NÉGATIF
negative_timer = 0  
time_crystals = []  

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
                if event.key == pygame.K_SPACE: game_state = "STORY"
            
            elif game_state == "STORY":
                if event.key in [pygame.K_SPACE, pygame.K_RETURN]:
                    story_index += 1
                    if story_index >= len(story_lines): game_state = "PLAYER_TURN"

            elif game_state == "GAME_OVER":
                if event.key == pygame.K_r:
                    player.hp, player.display_hp = player.max_hp, player.max_hp
                    player.energy, player.display_energy = 50, 50
                    boss.hp, boss.display_hp = boss.max_hp, boss.max_hp
                    boss.energy, boss.display_energy = 50, 50
                    player.x, boss.x = player.original_x, boss.original_x
                    player.is_attacking, boss.is_attacking = False, False
                    story_index, winner, wait_timer, has_hit = 0, None, 0, False
                    in_magic_menu, in_special_menu = False, False
                    game_state = "START_MENU"

            elif game_state == "PLAYER_TURN":
                if not in_magic_menu and not in_special_menu:
                    if event.key == pygame.K_UP: menu_index = (menu_index - 1) % len(options)
                    elif event.key == pygame.K_DOWN: menu_index = (menu_index + 1) % len(options)
                    elif event.key in [pygame.K_SPACE, pygame.K_RETURN]:
                        if menu_index == 0: 
                            player.is_attacking, player.target_x, has_hit = True, boss.x - 100, False 
                            game_state = "PLAYER_ATTACKING"
                        elif menu_index == 1: in_magic_menu = True
                        elif menu_index == 2: in_special_menu = True
                
                elif in_magic_menu:
                    if event.key == pygame.K_UP: magic_index = (magic_index - 1) % len(magic_options)
                    elif event.key == pygame.K_DOWN: magic_index = (magic_index + 1) % len(magic_options)
                    elif event.key == pygame.K_ESCAPE: in_magic_menu = False
                    elif event.key in [pygame.K_SPACE, pygame.K_RETURN]:
                        if magic_index == 0 and player.use_energy(10):
                            in_magic_menu, wait_timer, game_state = False, 0, "PREPARE_SOIN"
                        elif magic_index == 1 and player.use_energy(20):
                            in_magic_menu, wait_timer, game_state = False, 0, "PREPARE_ATTAQUE"
                        elif magic_index == 2: in_magic_menu = False
                
                elif in_special_menu:
                    if event.key == pygame.K_UP: special_index = (special_index - 1) % len(special_options)
                    elif event.key == pygame.K_DOWN: special_index = (special_index + 1) % len(special_options)
                    elif event.key == pygame.K_ESCAPE: in_special_menu = False
                    elif event.key in [pygame.K_SPACE, pygame.K_RETURN]:
                        if special_index == 0 and player.use_energy(40):
                            in_special_menu, wait_timer, game_state = False, 0, "PREPARE_SUPER_DASH"
                        elif special_index == 1: in_special_menu = False

    # --- LOGIQUE DE COMBAT ---
    if game_state == "PREPARE_SOIN":
        wait_timer += dt
        if wait_timer >= 0.6:
            player.heal(30); flash_color = (100, 255, 100); flash_effect_timer = 0.2
            wait_timer = 0; game_state = "WAIT_AFTER_MAGIC"

    if game_state == "PREPARE_ATTAQUE":
        wait_timer += dt
        if wait_timer >= 0.8:
            boss.take_damage(40); flash_color = (255, 255, 255); flash_effect_timer = 0.3
            wait_timer = 0; game_state = "WAIT_AFTER_MAGIC"

    if game_state == "PREPARE_SUPER_DASH":
        wait_timer += dt
        # ACTIVER L'EFFET NÉGATIF
        if wait_timer < 0.1 and negative_timer <= 0:
            negative_timer = 1.0 # Durée de l'effet
            # Créer des éclats de cristaux blancs/dorés
            time_crystals = []
            for _ in range(15):
                time_crystals.append({
                    "x": random.randint(50, WIDTH-50),
                    "y": random.randint(50, HEIGHT-150),
                    "size": random.randint(4, 10),
                    "alpha": random.randint(150, 255)
                })
        
        if wait_timer >= 0.8:
            boss.take_damage(80); flash_color = (255, 215, 0); flash_effect_timer = 0.4
            wait_timer = 0; game_state = "WAIT_AFTER_MAGIC"
            time_crystals = [] # Nettoyage

    if game_state == "WAIT_AFTER_MAGIC":
        wait_timer += dt
        if wait_timer >= 1.0: game_state = "ENEMY_TURN"; wait_timer = 0

    if game_state == "PLAYER_ATTACKING":
        if not has_hit and player.rect.colliderect(boss.rect):
            boss.take_damage(player.attack); has_hit = True; player.is_attacking = False 
        if not player.is_attacking and player.x == player.original_x:
            wait_timer += dt
            if wait_timer >= 0.8: game_state = "ENEMY_TURN"; wait_timer = 0

    if game_state == "ENEMY_TURN":
        wait_timer += dt
        if wait_timer >= 0.7:
            boss.is_attacking, boss.target_x, has_hit = True, player.x + 100, False
            game_state = "ENEMY_ATTACKING"; wait_timer = 0

    if game_state == "ENEMY_ATTACKING":
        if not has_hit and boss.rect.colliderect(player.rect):
            player.take_damage(boss.attack); has_hit = True; boss.is_attacking = False 
        if not boss.is_attacking and boss.x == boss.original_x:
            wait_timer += dt
            if wait_timer >= 0.8: game_state = "PLAYER_TURN"; wait_timer = 0

    if game_state not in ["START_MENU", "STORY", "GAME_OVER"]:
        if player.hp <= 0: game_state = "GAME_OVER"; winner = "ECLIPSE"
        elif boss.hp <= 0: game_state = "GAME_OVER"; winner = "SONIC"

    # --- AFFICHAGE ---
    player.update(dt); boss.update(dt)
    
    # GESTION DU FOND (NORMAL OU NÉGATIF)
    if negative_timer > 0:
        screen.blit(bg_negative, (0, 0))
        negative_timer -= dt
    else:
        screen.blit(background, (0, 0)) 

    player.draw(screen); boss.draw(screen)

    # DESSIN DES CRISTAUX DE TEMPS (Plus esthétique que les lignes)
    if negative_timer > 0:
        for crystal in time_crystals:
            # Création d'un éclat en forme de losange
            s = crystal["size"]
            surf = pygame.Surface((s*2, s*2), pygame.SRCALPHA)
            color = (255, 255, 255, crystal["alpha"])
            pygame.draw.polygon(surf, color, [(s, 0), (s*2, s), (s, s*2), (0, s)])
            screen.blit(surf, (crystal["x"], crystal["y"]))
            # Scintillement
            crystal["alpha"] = max(0, crystal["alpha"] - (150 * dt))

    # UI et Barres
    if game_state not in ["START_MENU", "STORY"]:
        draw_hp_bar(screen, player.x, player.y - 50, player.display_hp, player.max_hp)
        draw_mana_bar(screen, player.x, player.y - 25, player.display_energy, 50)
        draw_hp_bar(screen, boss.x, boss.y - 50, boss.display_hp, boss.max_hp)
        draw_mana_bar(screen, boss.x, boss.y - 25, boss.display_energy, 50)

        if game_state == "PLAYER_TURN":
            menu_rect = pygame.Rect(50, HEIGHT - 200, 280, 160)
            pygame.draw.rect(screen, (0, 0, 120), menu_rect, border_radius=12)
            pygame.draw.rect(screen, WHITE, menu_rect, 3, border_radius=12)
            draw_text(f"ENERGIE: {int(player.display_energy)} MP", font_interface, (0, 200, 255), screen, 190, HEIGHT - 180)
            
            if in_magic_menu: current_menu, current_idx, title_msg = magic_options, magic_index, "MAGIE DU CHAOS"
            elif in_special_menu: current_menu, current_idx, title_msg = special_options, special_index, "CAPACITÉ SPÉCIALE"
            else: current_menu, current_idx, title_msg = options, menu_index, "CHOISIS TON ACTION"
            
            draw_text(title_msg, font_tour, WHITE, screen, WIDTH // 2, 80)
            for i, opt in enumerate(current_menu):
                txt_color = WHITE if i == current_idx else GRAY
                draw_text("> " + opt if i == current_idx else "  " + opt, font_menu, txt_color, screen, 190, HEIGHT - 140 + (i * 35))

    # Overlays
    if game_state == "START_MENU":
        overlay = pygame.Surface((WIDTH, HEIGHT)); overlay.set_alpha(150); overlay.fill(BLACK); screen.blit(overlay, (0,0))
        draw_text("SONIC RPG LEGACY", font_title, (0, 200, 255), screen, WIDTH // 2, HEIGHT // 3)
        if (current_time // 500) % 2 == 0: draw_text("APPUYEZ SUR ESPACE", font_interface, WHITE, screen, WIDTH // 2, HEIGHT // 2 + 50)
    
    elif game_state == "STORY":
        dialog_rect = pygame.Rect(50, HEIGHT - 150, WIDTH - 100, 120)
        pygame.draw.rect(screen, BLACK, dialog_rect); pygame.draw.rect(screen, WHITE, dialog_rect, 3)
        draw_text(story_lines[story_index], font_interface, WHITE, screen, WIDTH // 2, HEIGHT - 90)

    elif game_state == "GAME_OVER":
        overlay = pygame.Surface((WIDTH, HEIGHT)); overlay.set_alpha(200); overlay.fill(BLACK); screen.blit(overlay, (0,0))
        msg = "VICTOIRE !" if winner == "SONIC" else "GAME OVER..."
        draw_text(msg, font_title, GREEN if winner == "SONIC" else RED, screen, WIDTH // 2, HEIGHT // 2 - 50)
        draw_text("APPUYEZ SUR 'R' POUR REJOUER", font_interface, WHITE, screen, WIDTH // 2, HEIGHT // 2 + 50)

    # Flash final
    if flash_effect_timer > 0:
        flash_surf = pygame.Surface((WIDTH, HEIGHT)); flash_surf.fill(flash_color)
        flash_surf.set_alpha(int((flash_effect_timer / 0.5) * 255))
        screen.blit(flash_surf, (0, 0)); flash_effect_timer -= dt

    pygame.display.flip()

pygame.quit()
sys.exit()