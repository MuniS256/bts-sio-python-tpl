import pygame
import os

class Fighter:
    def __init__(self, name, hp, attack, energy, image_path, x, y, frames=1):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.display_hp = hp
        self.attack = attack
        self.energy = energy
        
        # Positionnement
        self.x = x
        self.y = y
        self.original_x = x
        self.target_x = x
        
        # --- SYSTÈME D'ANIMATION (PRÊT POUR LES SPRITE SHEETS) ---
        self.frame_list = []
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.animation_speed = 150 # Vitesse en millisecondes
        
        try:
            full_sheet = pygame.image.load(image_path).convert_alpha()
            
            # On calcule la largeur d'une seule image (totale / nombre de frames)
            sheet_width = full_sheet.get_width()
            sheet_height = full_sheet.get_height()
            self.frame_width = sheet_width // frames
            
            # On découpe chaque frame et on la met dans la liste
            for i in range(frames):
                # Création d'une surface vide transparente
                temp_surface = pygame.Surface((self.frame_width, sheet_height), pygame.SRCALPHA)
                # On "capture" le morceau de l'image globale
                temp_surface.blit(full_sheet, (0, 0), (i * self.frame_width, 0, self.frame_width, sheet_height))
                # Redimensionnement (150x150 pour ton jeu)
                scaled_image = pygame.transform.scale(temp_surface, (150, 150))
                self.frame_list.append(scaled_image)
            
            self.image = self.frame_list[self.frame_index]
            
            # Création du Flash Rouge basé sur la première frame
            mask = pygame.mask.from_surface(self.image)
            self.flash_image = mask.to_surface(setcolor=(255, 0, 0), unsetcolor=(0, 0, 0, 0))
            
        except Exception as e:
            print(f"Erreur chargement image {image_path}: {e}")
            self.image = pygame.Surface((150, 150))
            self.image.fill((0, 0, 255))
            self.frame_list = [self.image]
            self.flash_image = pygame.Surface((150, 150))
            self.flash_image.fill((255, 0, 0))

        # États d'animation
        self.is_attacking = False
        self.flash_timer = 0
        self.flash_duration = 0.15 
        
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        
    def use_energy(self, amount):
        if self.energy >= amount:
            self.energy -= amount
            return True
        return False

    def heal(self, amount):
        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def take_damage(self, amount):
        self.hp = max(0, self.hp - amount)
        self.flash_timer = self.flash_duration

    def update(self, dt):
        # 1. GESTION DE L'ANIMATION (Boucle sur les frames)
        if len(self.frame_list) > 1:
            if pygame.time.get_ticks() - self.update_time > self.animation_speed:
                self.update_time = pygame.time.get_ticks()
                self.frame_index = (self.frame_index + 1) % len(self.frame_list)
                self.image = self.frame_list[self.frame_index]

        # 2. Gestion du flash rouge
        if self.flash_timer > 0:
            self.flash_timer -= dt

        # 3. Animation de la barre de vie
        self.display_hp += (self.hp - self.display_hp) * 0.1

        # 4. Logique de mouvement (Dash Attaque)
        if self.is_attacking:
            direction = 1 if self.x < self.target_x else -1
            self.x += 20 * direction
            if (direction == 1 and self.x >= self.target_x) or (direction == -1 and self.x <= self.target_x):
                self.x = self.target_x
        else:
            if abs(self.x - self.original_x) > 5:
                direction_retour = 1 if self.x < self.original_x else -1
                self.x += 8 * direction_retour
            else:
                self.x = self.original_x
        
        self.rect.topleft = (self.x, self.y)

    def draw(self, screen):
        # Si on flashe, on affiche l'image rouge, sinon l'image d'animation actuelle
        if self.flash_timer > 0:
            # On recrée un masque flash pour la frame actuelle si c'est une animation
            mask = pygame.mask.from_surface(self.image)
            flash = mask.to_surface(setcolor=(255, 0, 0), unsetcolor=(0, 0, 0, 0))
            screen.blit(flash, (self.x, self.y))
        else:
            screen.blit(self.image, (self.x, self.y))