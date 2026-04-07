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


import pygame
import os

class Fighter:
    def __init__(self, name, hp, attack, energy, image_path, x, y):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.attack = attack
        self.energy = energy
        
        # Positionnement (On définit x et y AVANT le reste)
        self.x = x
        self.y = y
        self.original_x = x
        self.target_x = x
        
        # États d'animation
        self.is_attacking = False
        self.flash_timer = 0
        self.flash_duration = 0.15 

        # --- CHARGEMENT DE L'IMAGE ---
        try:
            # On charge l'image
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (150, 150))
            
            # Création du Flash Rouge (Masque)
            mask = pygame.mask.from_surface(self.image)
            self.flash_image = mask.to_surface(setcolor=(255, 0, 0), unsetcolor=(0, 0, 0, 0))
            
        except Exception as e:
            print(f"Erreur chargement image {image_path}: {e}")
            # Image de secours (Surface bleue)
            self.image = pygame.Surface((150, 150))
            self.image.fill((0, 0, 255))
            self.flash_image = pygame.Surface((150, 150))
            self.flash_image.fill((255, 0, 0))

        # --- CRÉATION DU RECT (Après que l'image soit définie) ---
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

    def take_damage(self, amount):
        """Déclenche les dégâts et le flash visuel"""
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0
        self.flash_timer = self.flash_duration

    def update(self, dt):
        """Gère les mouvements et les timers"""
        # 1. Gestion du chrono du flash
        if self.flash_timer > 0:
            self.flash_timer -= dt

        # 2. Logique du mouvement d'attaque (Dash)
        if self.is_attacking:
            # Calcul de la direction (1 si droite, -1 si gauche)
            direction = 1 if self.x < self.target_x else -1
            self.x += 20 * direction

            # Vérification de l'arrivée (si on a dépassé ou atteint la cible)
            if (direction == 1 and self.x >= self.target_x) or (direction == -1 and self.x <= self.target_x):
                self.x = self.target_x
                self.is_attacking = False
        else:
            # Retour progressif
            if abs(self.x - self.original_x) > 5:
                direction_retour = 1 if self.x < self.original_x else -1
                self.x += 8 * direction_retour
            else:
                self.x = self.original_x
        
        # IMPORTANT : On met à jour le rectangle de collision
        self.rect.topleft = (self.x, self.y)

            # Si on est à gauche de la cible (cas de Sonic), on augmente X
        if self.x < self.target_x:
                self.x += 20
                if self.x >= self.target_x: # On est arrivé
                    self.x = self.target_x
                    self.is_attacking = False

            # Si on est à droite de la cible (cas d'Eclipse), on diminue X
        elif self.x > self.target_x:
                self.x -= 20
                if self.x <= self.target_x: # On est arrivé
                    self.x = self.target_x
                    self.is_attacking = False

        else:
            # Retour à la position d'origine
            if self.x < self.original_x:
                self.x += 8 # Revient vers la droite
            elif self.x > self.original_x:
                self.x -= 8 # Revient vers la gauche

            # Correction finale pour éviter de trembler sur place
            if abs(self.x - self.original_x) < 8:
                self.x = self.original_x
        
        # 3. Synchronisation du rectangle de collision avec la position visuelle
        self.rect.topleft = (self.x, self.y)

    def draw(self, screen):
        """Affiche le perso ou son flash rouge"""
        if self.flash_timer > 0:
            screen.blit(self.flash_image, (self.x, self.y))
        else:
            screen.blit(self.image, (self.x, self.y))