import pygame
import random
import sys
import os
from pygame import *

# --- CONFIGURATION DES CHEMINS ---
# On récupère le dossier où se trouve ce fichier .py
CHEMIN_DU_SCRIPT = os.path.dirname(__file__)
# On pointe vers le dossier ressources à l'intérieur de pendue_jeu_test
DOSSIER_RESSOURCES = os.path.join(CHEMIN_DU_SCRIPT, "ressources")

# --- CONFIGURATION ÉCRAN ---
LARGEUR_ECRAN = 800
HAUTEUR_ECRAN = 600
VIES_INITIALES = 11

# --- CLASSES ---

class Lettre(pygame.sprite.Sprite):
    def __init__(self, caractere, x, y, visible_par_defaut=False):
        super().__init__()
        self.caractere = caractere.upper()
        self.decouverte = visible_par_defaut

        # Chargement sécurisé de l'image de cache
        chemin_bloc = os.path.join(DOSSIER_RESSOURCES, "bloc_lettre.png")
        try:
            self.image_cachee = pygame.image.load(chemin_bloc).convert_alpha()
        except Exception as e:
            print(f"Erreur chargement bloc_lettre: {e}")
            self.image_cachee = pygame.Surface((50, 50))
            self.image_cachee.fill((100, 100, 100))

        # Préparation de la lettre révélée
        self.font = pygame.font.SysFont("Comic Sans MS", 50, bold=True)
        self.image_revelée = self.font.render(self.caractere, True, (255, 255, 255))

        self.update_image()
        self.rect = self.image.get_rect(center=(x, y))

    def update_image(self):
        self.image = self.image_revelée if self.decouverte else self.image_cachee

    def reveler(self):
        self.decouverte = True
        self.update_image()

class Potence(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.images_pendu = []

        # Chargement des 11 images
        for i in range(1, 12):
            nom_fichier = f"image_{i}.png"
            chemin_img = os.path.join(DOSSIER_RESSOURCES, nom_fichier)
            try:
                img = pygame.image.load(chemin_img).convert_alpha()
                self.images_pendu.append(img)
            except Exception as e:
                print(f"Erreur critique : Impossible de charger {chemin_img}")
                print(f"Détails : {e}")
                pygame.quit()
                sys.exit()

        self.index_image = 0
        self.image = self.images_pendu[self.index_image]
        self.rect = self.image.get_rect(center=(LARGEUR_ECRAN // 2, 250))

    def erreur_suivante(self):
        if self.index_image < VIES_INITIALES - 1:
            self.index_image += 1
            self.image = self.images_pendu[self.index_image]
            return False
        return True # Game Over

# --- GESTIONNAIRE DE JEU ---

class JeuPendu:
    def __init__(self):
        pygame.init()
        self.ecran = pygame.display.set_mode((LARGEUR_ECRAN, HAUTEUR_ECRAN))
        pygame.display.set_caption("Jeu du Pendu - NSI Edition")
        self.clock = pygame.time.Clock()
        self.mots = ["PYTHON", "RESEAU", "SERVEUR", "ALGORITHME", "BOUCLE", "CONDITION", "FONCTION"]
        self.reinitialiser()

    def reinitialiser(self):
        self.mot_a_deviner = random.choice(self.mots).upper()
        self.tous_sprites = pygame.sprite.Group()
        self.groupe_lettres = pygame.sprite.Group()

        # Potence
        self.potence = Potence()
        self.tous_sprites.add(self.potence)

        # Calcul de la position des lettres
        espacement = 65
        x_depart = (LARGEUR_ECRAN - (len(self.mot_a_deviner) * espacement)) // 2 + (espacement // 2)

        for i, char in enumerate(self.mot_a_deviner):
            # Première et dernière lettre visibles
            est_visible = (i == 0 or i == len(self.mot_a_deviner) - 1)
            l = Lettre(char, x_depart + i * espacement, 520, est_visible)
            self.groupe_lettres.add(l)
            self.tous_sprites.add(l)

    def boucle_principale(self):
        en_cours = True
        while en_cours:
            for event in pygame.event.get():
                if event.type == QUIT:
                    en_cours = False

                if event.type == KEYDOWN:
                    lettre = event.unicode.upper()
                    if lettre.isalpha() and len(lettre) == 1:
                        self.verifier_lettre(lettre)

            self.ecran.fill((40, 40, 60)) # Fond bleu nuit
            self.tous_sprites.draw(self.ecran)
            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()
        sys.exit()

    def verifier_lettre(self, lettre):
        if lettre in self.mot_a_deviner:
            for s in self.groupe_lettres:
                if s.caractere == lettre:
                    s.reveler()

            if all(s.decouverte for s in self.groupe_lettres):
                print("Gagné !")
                pygame.time.delay(1000)
                self.reinitialiser()
        else:
            if self.potence.erreur_suivante():
                print(f"Perdu ! Le mot était : {self.mot_a_deviner}")
                pygame.time.delay(2000)
                self.reinitialiser()

if __name__ == "__main__":
    jeu = JeuPendu()
    jeu.boucle_principale()