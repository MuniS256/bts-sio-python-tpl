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

class Fighter:
    def __init__(self, name, hp, attack, energy, image_path, x, y):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        
        # Positionnement
        self.x = x
        self.y = y
        self.original_x = x
        self.target_x = x
        
        # État
        self.is_attacking = False
        
        # Image
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (150, 150))

    def update(self):
        # Logique de mouvement fluide (Lerp ou vitesse simple)
        if self.is_attacking:
            if self.x < self.target_x:
                self.x += 15 # Vitesse d'attaque
            else:
                self.is_attacking = False # Il a atteint la cible
        elif self.x > self.original_x:
            self.x -= 5 # Il revient doucement