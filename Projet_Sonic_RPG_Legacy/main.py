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
from ui import draw_hp_bar # Assure-toi que le nom correspond à ton fichier ui.py

# 1. INITIALISATION
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sonic RPG Legacy")
clock = pygame.time.Clock()

# 2. CRÉATION DES PERSONNAGES
# Note : On ajoute x=100, y=300 pour la position de départ
player = Fighter("Sonic", 100, 20, 50, SONIC_SPRITE, 100, 300)
boss = Fighter("Eclipse", 120, 15, 50, ENEMY_SPRITE, 550, 300)

# 3. BOUCLE DE JEU
running = True
has_hit = False
while running:
    dt = clock.tick(FPS) / 1000.0  # Delta time in seconds
    # Dans la boucle while
player.update(dt)
boss.update(dt)

# Vérification du contact
if player.is_attacking and player.rect.colliderect(boss.rect):
    if not has_hit: # Sécurité pour ne frapper qu'une fois
        boss.take_damage(player.attack)
        has_hit = True
        # Optionnel : On peut faire reculer Sonic un peu pour l'effet d'impact
        player.is_attacking = False
        
    # --- A. Gestion des événements (Entrées utilisateur) ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            # Si on appuie sur ESPACE et que Sonic n'est pas déjà en train de bouger
            if event.key == pygame.K_SPACE and not player.is_attacking:
                player.is_attacking = True
                player.target_x = boss.x - 50 # Sonic fonce devant l'ennemi
                boss.hp -= player.attack      # On retire les PV direct
                if boss.hp < 0: boss.hp = 0

    # --- B. Mise à jour de la logique (Calculs) ---
    player.update(dt) # Gère le mouvement de Sonic
    boss.update(dt)   # Gère le mouvement de l'ennemi (si besoin)

    # --- NOUVEAU : Détection de l'impact ---
    # Si Sonic est en train d'attaquer ET qu'il touche le boss
    if player.is_attacking and player.rect.colliderect(boss.rect):
        boss.take_damage(player.attack) # Le flash et les dégâts arrivent ICI !
        player.is_attacking = False    # Sonic s'arrête et commence à revenir
        has_hit = True # On marque que le coup a été porté pour cette attaque

    # --- C. Affichage (Dessin) ---
    screen.fill(BLACK) # On efface l'écran précédent
    
    # ✅ NOUVEAU (À UTILISER) :
    # On laisse l'objet décider s'il doit dessiner l'image normale ou le flash rouge
    player.draw(screen)
    boss.draw(screen)
    
    # On dessine l'interface par-dessus
    draw_hp_bar(screen, 100, 250, player.hp, player.max_hp)
    draw_hp_bar(screen, 500, 250, boss.hp, boss.max_hp)

    # --- D. Rafraîchissement ---
    pygame.display.flip()

pygame.quit()
sys.exit()