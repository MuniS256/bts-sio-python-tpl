# fighter_class.py
"""
class Fighter:
    def __init__(self, name, hp, attack, energy):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.attack = attack
        self.energy = energy
        self.is_guarding = False

    def take_damage(self, amount):
        if self.is_guarding:
            amount = int(amount * 0.5)
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0

    def heal(self, amount):
        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp
"""
# main.py
import pygame
import sys
from settings import *
from fighter_class import Fighter
from ui import draw_hp_bar # Assure-toi que le nom correspond

# 1. INITIALISATION
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sonic RPG Legacy")
clock = pygame.time.Clock()

# 2. CRÉATION DES PERSONNAGES
player = Fighter("Sonic", 100, 20, 50, SONIC_SPRITE, 100, 300)
boss = Fighter("Eclipse", 120, 15, 50, ENEMY_SPRITE, 550, 300)

# 3. BOUCLE DE JEU
running = True
while running:
    # --- A. Gestion du Temps ---
    # dt est le temps écoulé en SECONDES (ex: 1/60 = 0.016s)
    dt = clock.tick(FPS) / 1000.0

    # --- B. Gestion des événements ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not player.is_attacking:
                player.is_attacking = True
                player.target_x = boss.x - 50 # Sonic fonce
                
                # --- NOUVEAU : On utilise la méthode take_damage() ---
                # Cela déclenche les dégâts ET le flash rouge !
                boss.take_damage(player.attack)

    # --- C. Mise à jour de la logique (Calculs) ---
    player.update(dt) # On transmet dt
    boss.update(dt)

    # --- D. Affichage (Dessin) ---
    screen.fill(BLACK)
    
    # On utilise les nouvelles méthodes draw() des personnages
    player.draw(screen) # Sonic dessine son image
    boss.draw(screen)   # Eclipse dessine son image... OU son flash rouge !
    
    # Dessiner l'interface par-dessus
    draw_hp_bar(screen, 100, 250, player.hp, player.max_hp)
    draw_hp_bar(screen, 500, 250, boss.hp, boss.max_hp)

    # --- E. Rafraîchissement ---
    pygame.display.flip()

pygame.quit()
sys.exit()