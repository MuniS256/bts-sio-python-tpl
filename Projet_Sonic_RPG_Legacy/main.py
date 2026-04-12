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
from ui import draw_hp_bar, draw_mana_bar, draw_text, negative_surface 

# 1. INITIALISATION
pygame.init()
pygame.mixer.init() # Initialisation du son
screen = pygame.display.set_mode((WIDTH, HEIGHT)) 
pygame.display.set_caption("Sonic RPG Legacy")
clock = pygame.time.Clock()

# --- CHARGEMENT DES ASSETS SONORES ---
# On définit les variables par défaut pour éviter le NameError
snd_attack = snd_heal = snd_hit = snd_special = None
music_menu = ""
music_battle = ""

try:
    # Chemins des fichiers
    music_menu = "Projet_Sonic_RPG_Legacy/assets/musics/SA2_menuB.mp3"
    music_battle = "Projet_Sonic_RPG_Legacy/assets/musics/grandia2_battle_theme.mp3"
    
    # Chargement des bruitages
    snd_attack = pygame.mixer.Sound("Projet_Sonic_RPG_Legacy/assets/sounds/heavy_punch.mp3")
    snd_heal = pygame.mixer.Sound("Projet_Sonic_RPG_Legacy/assets/sounds/healing.mp3")
    snd_hit = pygame.mixer.Sound("Projet_Sonic_RPG_Legacy/assets/sounds/attackS.mp3")
    snd_special = pygame.mixer.Sound("Projet_Sonic_RPG_Legacy/assets/sounds/Ding.mp3")
except Exception as e:
    print(f"Note : Certains fichiers audio sont manquants ou introuvables. Erreur : {e}")

# --- CHARGEMENT DES ASSETS IMAGES ---
try:
    background = pygame.image.load("Projet_Sonic_RPG_Legacy/assets/images/c_hill_zone.png").convert()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    bg_negative = negative_surface(background.copy())
except:
    background = pygame.Surface((WIDTH, HEIGHT))
    background.fill((20, 40, 20))
    bg_negative = pygame.Surface((WIDTH, HEIGHT))
    bg_negative.fill((200, 200, 200))

# 2. CRÉATION DES PERSONNAGES
player = Fighter("Sonic", 100, 20, 50, SONIC_SPRITE, 200, 400, frames=1)
boss = Fighter("Eclipse", 120, 15, 50, ENEMY_SPRITE, 900, 400, frames=1)

# --- VARIABLES DE CONTRÔLE ---
game_state = "START_MENU" 
current_music = "" # Pour éviter de relancer la musique en boucle

story_index = 0
story_lines = [
    "Sonic: Eclipse ! Rend-moi l'Emeraude du Chaos tout de suite !",
    "Eclipse: Tu arrives trop tard, hérisson bleu...",
    "Eclipse: La puissance du vide est déjà en moi !",
    "Sonic: On va voir si tu tiens encore debout après ça !"
]

main_menu_options = ["COMMENCER L'AVENTURE", "COMMANDES", "QUITTER"]
main_menu_index = 0

has_hit = False
wait_timer = 0 
menu_index = 0 
options = ["ATTACK", "MAGIC", "SPECIAL"]
winner = None 

magic_options = ["SOIN (10 MP)", "CHAOS BLAST (20 MP)", "RETOUR"]
in_magic_menu = False
magic_index = 0

special_options = ["SUPER DASH (40 MP)", "RETOUR"]
in_special_menu = False
special_index = 0

# --- EFFETS ---
flash_effect_timer = 0
flash_color = (255, 255, 255)
negative_timer = 0  
time_crystals = []  

# Polices
font_interface = pygame.font.SysFont("Arial", 28, bold=True)
font_tour = pygame.font.SysFont("Arial", 40, bold=True)
font_menu = pygame.font.SysFont("Verdana", 26, bold=True)
font_title = pygame.font.SysFont("Impact", 85)

# Fonction pour changer de musique proprement
def change_music(music_file):
    global current_music
    if current_music != music_file:
        try:
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.set_volume(0.4)
            pygame.mixer.music.play(-1)
            current_music = music_file
        except:
            pass

# 3. BOUCLE DE JEU
running = True
while running:
    dt = clock.tick(FPS) / 1000.0 
    current_time = pygame.time.get_ticks()

    # --- GESTION MUSIQUE PAR ÉTAT ---
    if game_state == "START_MENU":
        change_music(music_menu)
    elif game_state == "PLAYER_TURN" or game_state == "STORY":
        change_music(music_battle)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            # --- LOGIQUE MENU PRINCIPAL ---
            if game_state == "START_MENU":
                if event.key == pygame.K_UP:
                    main_menu_index = (main_menu_index - 1) % len(main_menu_options)
                elif event.key == pygame.K_DOWN:
                    main_menu_index = (main_menu_index + 1) % len(main_menu_options)
                elif event.key in [pygame.K_SPACE, pygame.K_RETURN]:
                    if main_menu_index == 0: 
                        game_state = "STORY"
                    elif main_menu_index == 2: 
                        running = False
            
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
                    story_index, winner, wait_timer, has_hit = 0, None, 0, False
                    game_state = "START_MENU"

            # --- LOGIQUE COMBAT ---
            elif game_state == "PLAYER_TURN":
                if not in_magic_menu and not in_special_menu:
                    if event.key == pygame.K_UP: menu_index = (menu_index - 1) % len(options)
                    elif event.key == pygame.K_DOWN: menu_index = (menu_index + 1) % len(options)
                    elif event.key in [pygame.K_SPACE, pygame.K_RETURN]:
                        if menu_index == 0: 
                            player.is_attacking, player.target_x, has_hit = True, boss.x - 100, False 
                            if snd_attack: snd_attack.play()
                            game_state = "PLAYER_ATTACKING"
                        elif menu_index == 1: in_magic_menu = True
                        elif menu_index == 2: in_special_menu = True
                
                elif in_magic_menu:
                    if event.key == pygame.K_UP: magic_index = (magic_index - 1) % len(magic_options)
                    elif event.key == pygame.K_DOWN: magic_index = (magic_index + 1) % len(magic_options)
                    elif event.key in [pygame.K_SPACE, pygame.K_RETURN]:
                        if magic_index == 0 and player.use_energy(10): 
                            game_state = "PREPARE_SOIN"
                        elif magic_index == 1 and player.use_energy(20): 
                            game_state = "PREPARE_ATTAQUE"
                        in_magic_menu = False
                    elif event.key == pygame.K_ESCAPE: in_magic_menu = False

                elif in_special_menu:
                    if event.key == pygame.K_UP: special_index = (special_index - 1) % len(special_options)
                    elif event.key == pygame.K_DOWN: special_index = (special_index + 1) % len(special_options)
                    elif event.key in [pygame.K_SPACE, pygame.K_RETURN]:
                        if special_index == 0 and player.use_energy(40):
                            wait_timer = 0
                            game_state = "PREPARE_SUPER_DASH"
                        in_special_menu = False
                    elif event.key == pygame.K_ESCAPE: in_special_menu = False

    # --- LOGIQUE DE COMBAT ---
    if game_state == "PREPARE_SUPER_DASH":
        wait_timer += dt
        if negative_timer <= 0:
            negative_timer = 1.0
            if snd_special: snd_special.play()
            time_crystals = [{"x": random.randint(50, WIDTH-50), "y": random.randint(50, HEIGHT-150), 
                             "size": random.randint(4, 10), "alpha": random.randint(150, 255)} for _ in range(20)]
        if wait_timer >= 0.8:
            boss.take_damage(80); flash_color = (255, 215, 0); flash_effect_timer = 0.4
            if snd_hit: snd_hit.play()
            wait_timer = 0; game_state = "WAIT_AFTER_MAGIC"; time_crystals = []

    if game_state == "PREPARE_SOIN":
        wait_timer += dt
        if wait_timer >= 0.6:
            player.heal(30); flash_color = (100, 255, 100); flash_effect_timer = 0.2
            if snd_heal: snd_heal.play()
            wait_timer = 0; game_state = "WAIT_AFTER_MAGIC"

    if game_state == "PREPARE_ATTAQUE":
        wait_timer += dt
        if wait_timer >= 0.8:
            boss.take_damage(40); flash_color = (255, 255, 255); flash_effect_timer = 0.3
            if snd_hit: snd_hit.play()
            wait_timer = 0; game_state = "WAIT_AFTER_MAGIC"

    if game_state == "WAIT_AFTER_MAGIC":
        wait_timer += dt
        if wait_timer >= 1.0: game_state = "ENEMY_TURN"; wait_timer = 0

    if game_state == "PLAYER_ATTACKING":
        if not has_hit and player.rect.colliderect(boss.rect):
            boss.take_damage(player.attack); has_hit = True; player.is_attacking = False 
            if snd_hit: snd_hit.play()
        if not player.is_attacking and player.x == player.original_x:
            wait_timer += dt
            if wait_timer >= 0.8: game_state = "ENEMY_TURN"; wait_timer = 0

    if game_state == "ENEMY_TURN":
        wait_timer += dt
        if wait_timer >= 0.7:
            boss.is_attacking, boss.target_x, has_hit = True, player.x + 100, False
            if snd_attack: snd_attack.play()
            game_state = "ENEMY_ATTACKING"; wait_timer = 0

    if game_state == "ENEMY_ATTACKING":
        if not has_hit and boss.rect.colliderect(player.rect):
            player.take_damage(boss.attack); has_hit = True; boss.is_attacking = False 
            if snd_hit: snd_hit.play()
        if not boss.is_attacking and boss.x == boss.original_x:
            wait_timer += dt
            if wait_timer >= 0.8: game_state = "PLAYER_TURN"; wait_timer = 0

    # Vérification mort
    if game_state not in ["START_MENU", "STORY", "GAME_OVER"]:
        if player.hp <= 0: 
            game_state = "GAME_OVER"; winner = "ECLIPSE"
            pygame.mixer.music.fadeout(1000)
        elif boss.hp <= 0: 
            game_state = "GAME_OVER"; winner = "SONIC"
            pygame.mixer.music.fadeout(1000)

    # --- AFFICHAGE ---
    player.update(dt); boss.update(dt)
    
    if negative_timer > 0:
        screen.blit(bg_negative, (0, 0))
        negative_timer -= dt
        for crystal in time_crystals:
            s = crystal["size"]
            surf = pygame.Surface((s*2, s*2), pygame.SRCALPHA)
            pygame.draw.polygon(surf, (255, 255, 255, crystal["alpha"]), [(s, 0), (s*2, s), (s, s*2), (0, s)])
            screen.blit(surf, (crystal["x"], crystal["y"])); crystal["alpha"] = max(0, crystal["alpha"] - (150 * dt))
    else:
        screen.blit(background, (0, 0)) 

    if game_state != "START_MENU":
        player.draw(screen); boss.draw(screen)

    # --- UI MENU PRINCIPAL ---
    if game_state == "START_MENU":
        overlay = pygame.Surface((WIDTH, HEIGHT)); overlay.set_alpha(180); overlay.fill((0, 0, 20)) 
        screen.blit(overlay, (0, 0))
        v_x, v_y = random.randint(-2, 2), random.randint(-2, 2)
        draw_text("SONIC RPG LEGACY", font_title, (20, 20, 20), screen, WIDTH // 2 + 5, HEIGHT // 3 + 5)
        draw_text("SONIC RPG LEGACY", font_title, (0, 100, 255), screen, WIDTH // 2 + v_x, HEIGHT // 3 + v_y)
        draw_text("SONIC RPG LEGACY", font_title, WHITE, screen, WIDTH // 2, HEIGHT // 3)

        for i, opt in enumerate(main_menu_options):
            color = (0, 255, 255) if i == main_menu_index else (100, 100, 100)
            draw_text((">> " if i == main_menu_index else "   ") + opt, font_menu, color, screen, WIDTH // 2, HEIGHT // 2 + 30 + (i * 60))

    # --- UI COMBAT ---
    elif game_state not in ["STORY"]:
        draw_hp_bar(screen, player.x, player.y - 50, player.display_hp, player.max_hp)
        draw_mana_bar(screen, player.x, player.y - 25, player.display_energy, 50)
        draw_hp_bar(screen, boss.x, boss.y - 50, boss.display_hp, boss.max_hp)
        draw_mana_bar(screen, boss.x, boss.y - 25, boss.display_energy, 50)

        if game_state == "PLAYER_TURN":
            pygame.draw.rect(screen, (0, 0, 120), (50, HEIGHT - 200, 280, 160), border_radius=12)
            pygame.draw.rect(screen, WHITE, (50, HEIGHT - 200, 280, 160), 3, border_radius=12)
            
            if in_magic_menu: current_menu, current_idx, title_msg = magic_options, magic_index, "MAGIE DU CHAOS"
            elif in_special_menu: current_menu, current_idx, title_msg = special_options, special_index, "CAPACITÉ SPÉCIALE"
            else: current_menu, current_idx, title_msg = options, menu_index, "CHOISIS TON ACTION"
            
            draw_text(title_msg, font_tour, WHITE, screen, WIDTH // 2, 80)
            for i, opt in enumerate(current_menu):
                txt_color = WHITE if i == current_idx else (150, 150, 150)
                draw_text(("> " if i == current_idx else "  ") + opt, font_menu, txt_color, screen, 190, HEIGHT - 140 + (i * 35))

    if game_state == "STORY":
        pygame.draw.rect(screen, BLACK, (50, HEIGHT - 150, WIDTH - 100, 120))
        pygame.draw.rect(screen, WHITE, (50, HEIGHT - 150, WIDTH - 100, 120), 3)
        draw_text(story_lines[story_index], font_interface, WHITE, screen, WIDTH // 2, HEIGHT - 90)

    elif game_state == "GAME_OVER":
        overlay = pygame.Surface((WIDTH, HEIGHT)); overlay.set_alpha(200); overlay.fill(BLACK); screen.blit(overlay, (0,0))
        draw_text("VICTOIRE !" if winner == "SONIC" else "GAME OVER...", font_title, (0, 255, 100) if winner == "SONIC" else (255, 50, 50), screen, WIDTH // 2, HEIGHT // 2 - 50)
        draw_text("APPUYEZ SUR 'R' POUR REJOUER", font_interface, WHITE, screen, WIDTH // 2, HEIGHT // 2 + 50)

    # Effet de flash
    if flash_effect_timer > 0:
        flash_surf = pygame.Surface((WIDTH, HEIGHT)); flash_surf.fill(flash_color)
        flash_surf.set_alpha(int((flash_effect_timer / 0.5) * 255))
        screen.blit(flash_surf, (0, 0)); flash_effect_timer -= dt

    pygame.display.flip()

pygame.quit()
sys.exit()