import pygame
import os

class Fighter:
    def __init__(self, name, hp, attack, energy, image_path, x, y):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.attack = attack
        self.energy = energy
        
        # --- 2B : Animation de la barre de vie ---
        # 'display_hp' va rattraper 'hp' doucement pour l'effet visuel
        self.display_hp = hp
        
        # Positionnement
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
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (150, 150))
            
            # Création du Flash Rouge via un Masque
            mask = pygame.mask.from_surface(self.image)
            self.flash_image = mask.to_surface(setcolor=(255, 0, 0), unsetcolor=(0, 0, 0, 0))
            
        except Exception as e:
            print(f"Erreur chargement image {image_path}: {e}")
            self.image = pygame.Surface((150, 150))
            self.image.fill((0, 0, 255))
            self.flash_image = pygame.Surface((150, 150))
            self.flash_image.fill((255, 0, 0))

        # --- CRÉATION DU RECT ---
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

    def take_damage(self, amount):
        """Déclenche les dégâts et le flash visuel"""
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0
        self.flash_timer = self.flash_duration

    def update(self, dt):
        """Gère les mouvements, les timers et l'animation de la barre de vie"""
        
        # 1. Gestion du chrono du flash
        if self.flash_timer > 0:
            self.flash_timer -= dt

        # --- 2B : ANIMATION DE GLISSEMENT ---
        # La barre de vie affichée rattrape la vraie vie petit à petit
        # 0.1 est le facteur de lissage (plus c'est petit, plus c'est lent)
        smoothing_factor = 0.1
        self.display_hp += (self.hp - self.display_hp) * smoothing_factor

        # 2. LOGIQUE DU MOUVEMENT
        if self.is_attacking:
            # --- PHASE D'ATTAQUE (Aller vers la cible) ---
            direction = 1 if self.x < self.target_x else -1
            self.x += 20 * direction

            # Vérification si on a atteint ou dépassé la cible
            if (direction == 1 and self.x >= self.target_x) or (direction == -1 and self.x <= self.target_x):
                self.x = self.target_x
        else:
            # --- PHASE DE REPOS (Retour vers l'origine) ---
            if abs(self.x - self.original_x) > 5:
                direction_retour = 1 if self.x < self.original_x else -1
                self.x += 8 * direction_retour
            else:
                self.x = self.original_x
        
        # 3. Synchronisation du rectangle de collision
        self.rect.topleft = (self.x, self.y)

    def draw(self, screen):
        """Affiche le perso ou son flash rouge"""
        if self.flash_timer > 0:
            screen.blit(self.flash_image, (self.x, self.y))
        else:
            screen.blit(self.image, (self.x, self.y))