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
        self.rect = self.image.get_rect()

        # Positionnement
        self.x = x
        self.y = y
        self.original_x = x
        self.target_x = x
        
        # États d'animation
        self.is_attacking = False
        
        # Gestion du Flash Rouge (Damage Feedback)
        self.flash_timer = 0
        self.flash_duration = 0.15  # Le flash dure 150 millisecondes
        
        # Chargement de l'image
        try:
            # On charge l'image originale
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (150, 150))

            self.rect = self.image.get_rect() # Crée un rectangle de la taille de l'image
            self.rect.topleft = (x, y)       # Place le rectangle au bon endroit
            
            # Création de la version "Flash Rouge"
            # On crée une surface de la même taille remplie de rouge
            self.flash_image = pygame.Surface(self.image.get_size()).convert_alpha()
            self.flash_image.fill((255, 0, 0)) # Rouge pur
            
            # On utilise un masque pour que le rouge ne s'affiche que sur le perso (pas le vide)
            mask = pygame.mask.from_surface(self.image)
            self.flash_image = mask.to_surface(setcolor=(255, 0, 0), unsetcolor=(0, 0, 0, 0))
            
        except Exception as e:
            print(f"Erreur chargement image {image_path}: {e}")
            # Carré de secours si l'image est manquante
            self.image = pygame.Surface((150, 150))
            self.image.fill((0, 0, 255))
            self.flash_image = self.image.copy()
            self.flash_image.fill((255, 0, 0))

    def take_damage(self, amount):
        """Appelée quand le perso reçoit un coup"""
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0
        # On déclenche le chrono du flash
        self.flash_timer = self.flash_duration

    def update(self, dt):
        """Gère les mouvements et les timers"""
        # 1. Gestion du chrono du flash
        if self.flash_timer > 0:
            self.flash_timer -= dt

        # 2. Logique du mouvement d'attaque (Dash)
        if self.is_attacking:
            # On fonce vers la cible
            if self.x < self.target_x:
                self.x += 20  # Vitesse d'aller
            else:
                # Une fois arrivé, on arrête l'attaque
                self.is_attacking = False
        else:
            # Retour à la position d'origine
            if self.x > self.original_x:
                self.x -= 8  # Vitesse de retour (plus lent pour le style)
            if self.x < self.original_x:
                self.x = self.original_x
        
        self.rect.topleft = (self.x, self.y)

    def draw(self, screen):
        """Affiche le perso ou son flash rouge"""
        if self.flash_timer > 0:
            screen.blit(self.flash_image, (self.x, self.y))
        else:
            screen.blit(self.image, (self.x, self.y))