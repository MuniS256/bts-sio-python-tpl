# Créé par Ordinateur, le 07/04/2026 en Python 3.7
import pygame
import random
import sys
import os
from pygame import *

# --- CONFIGURATION DES CHEMINS ---
CHEMIN_DU_SCRIPT = os.path.dirname(__file__)
DOSSIER_RESSOURCES = os.path.join(CHEMIN_DU_SCRIPT, "ressources")

# --- CONFIGURATION ÉCRAN ---
LARGEUR_ECRAN = 800
HAUTEUR_ECRAN = 600
VIES_INITIALES = 11

# Couleurs
BLANC = (255, 255, 255)
NOIR_DOUX = (40, 40, 40)
GRIS_CLAIR = (220, 220, 220)
VERT_SOFT = (144, 238, 144)
JAUNE_SOFT = (255, 255, 150)
ROUGE_SOFT = (255, 182, 193)

# --- CLASSE BOUTON ---
class Bouton:
    def __init__(self, texte, x, y, largeur, hauteur, couleur_fond):
        self.rect = pygame.Rect(0, 0, largeur, hauteur)
        self.rect.center = (x, y)
        self.texte = texte
        self.couleur = couleur_fond
        self.font = pygame.font.SysFont("Arial", 22, bold=True)

    def dessiner(self, ecran):
        pygame.draw.rect(ecran, self.couleur, self.rect, border_radius=12)
        pygame.draw.rect(ecran, NOIR_DOUX, self.rect, 2, border_radius=12)
        txt_surf = self.font.render(self.texte, True, NOIR_DOUX)
        txt_rect = txt_surf.get_rect(center=self.rect.center)
        ecran.blit(txt_surf, txt_rect)

    def est_clique(self, pos, clic):
        return self.rect.collidepoint(pos) and clic[0]

# --- CLASSES DU JEU ---
class Lettre(pygame.sprite.Sprite):
    def __init__(self, caractere, x, y, visible=False):
        super().__init__()
        self.caractere = caractere.upper()
        self.decouverte = visible
        self.image = pygame.Surface((50, 60), pygame.SRCALPHA)

        path_bloc = os.path.join(DOSSIER_RESSOURCES, "bloc_lettre.png")
        try:
            temp = pygame.image.load(path_bloc).convert_alpha()
            temp.set_colorkey(BLANC)
            self.img_cachee = pygame.transform.scale(temp, (45, 45))
        except:
            self.img_cachee = pygame.Surface((45, 45), pygame.SRCALPHA)
            pygame.draw.rect(self.img_cachee, (200,200,200), (0,0,45,45), border_radius=8)

        self.font = pygame.font.SysFont("Arial", 45, bold=True)
        self.img_revelée = self.font.render(self.caractere, True, NOIR_DOUX)
        self.update_image()
        self.rect = self.image.get_rect(center=(x, y))

    def update_image(self):
        self.image.fill((0,0,0,0))
        if self.decouverte:
            self.image.blit(self.img_revelée, self.img_revelée.get_rect(center=(25, 30)))
        else:
            self.image.blit(self.img_cachee, self.img_cachee.get_rect(center=(25, 30)))

    def reveler(self):
        self.decouverte = True
        self.update_image()

class Potence(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.images = []
        for i in range(1, 12):
            img = pygame.image.load(os.path.join(DOSSIER_RESSOURCES, f"image_{i}.png")).convert_alpha()
            img.set_colorkey(BLANC)
            self.images.append(img)
        self.index = 0
        self.image = self.images[0]
        self.rect = self.image.get_rect(center=(LARGEUR_ECRAN // 2, 200))

    def erreur(self):
        if self.index < 10:
            self.index += 1
            self.image = self.images[self.index]
            return False
        return True

# --- GESTIONNAIRE DE JEU ---
class JeuPendu:
    def __init__(self):
        pygame.init()
        self.ecran = pygame.display.set_mode((LARGEUR_ECRAN, HAUTEUR_ECRAN))
        pygame.display.set_caption("Le Pendu")
        self.clock = pygame.time.Clock()
        self.etat = "MENU"

        self.mots_difficulte = {
    "FACILE": [
        "CHAT", "FEU", "SOLEIL", "POMME", "LUNE",
        "AVION", "BALLON", "FORÊT", "JARDIN", "LIVRE",
        "PORTE", "RADIO", "SABLE", "TRAIN", "ZÈBRE"
    ],
    "MOYEN": [
        "PYTHON", "SERVEUR", "BOUCLE", "RESEAU", "CLAVIER",
        "LOGICIEL", "AFFICHAGE", "CONSOLE", "DONNEES", "FICHIER",
        "MEMOIRE", "MOTEUR", "PIXELS", "SOURIS", "SYSTEME"
    ],
    "DIFFICILE": [
        "ALGORITHME", "INDENTATION", "CRYPTOGRAPHIE", "PROCESSEUR", "RECURSIVITE",
        "ABSTRACTION", "ASYNCHRONE", "COMPILATEUR", "DICTIONNAIRE", "HERITAGE",
        "INTERFACE", "ITERATION", "PARADIGME", "PROTOCOLE", "VARIABLE"
    ]
}

        # Boutons Menu Principal
        self.btn_facile = Bouton("FACILE", LARGEUR_ECRAN//2, 220, 220, 50, VERT_SOFT)
        self.btn_moyen = Bouton("MOYEN", LARGEUR_ECRAN//2, 290, 220, 50, JAUNE_SOFT)
        self.btn_difficile = Bouton("DIFFICILE", LARGEUR_ECRAN//2, 360, 220, 50, ROUGE_SOFT)
        self.btn_quitter_jeu = Bouton("QUITTER LE JEU", LARGEUR_ECRAN//2, 500, 220, 45, GRIS_CLAIR)

        # Boutons de Fin
        self.btn_rejouer = Bouton("REJOUER", LARGEUR_ECRAN//2 - 120, 450, 180, 55, VERT_SOFT)
        self.btn_retour_menu = Bouton("MENU PRINCIPAL", LARGEUR_ECRAN//2 + 120, 450, 180, 55, GRIS_CLAIR)

    def lancer_partie(self, niveau):
        self.etat = "EN_COURS"
        self.niveau_actuel = niveau
        self.mot = random.choice(self.mots_difficulte[niveau]).upper()
        self.tous_sprites = pygame.sprite.Group()
        self.groupe_lettres = pygame.sprite.Group()
        self.potence = Potence()
        self.tous_sprites.add(self.potence)

        espacement = 80
        x_start = (LARGEUR_ECRAN - (len(self.mot) * espacement)) // 2 + (espacement // 2)
        for i, char in enumerate(self.mot):
            visible = (i == 0 or i == len(self.mot)-1)
            l = Lettre(char, x_start + i * espacement, 520, visible)
            self.groupe_lettres.add(l)
            self.tous_sprites.add(l)

    def boucle(self):
        while True:
            pos_souris = pygame.mouse.get_pos()
            clic = pygame.mouse.get_pressed()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit(); sys.exit()

                if self.etat == "EN_COURS" and event.type == KEYDOWN:
                    lettre = event.unicode.upper()
                    if lettre.isalpha(): self.gestion_tentative(lettre)

            self.ecran.fill(BLANC)

            if self.etat == "MENU":
                titre = pygame.font.SysFont("Arial", 45, bold=True).render("LE PENDU", True, NOIR_DOUX)
                self.ecran.blit(titre, titre.get_rect(center=(LARGEUR_ECRAN//2, 120)))

                self.btn_facile.dessiner(self.ecran)
                self.btn_moyen.dessiner(self.ecran)
                self.btn_difficile.dessiner(self.ecran)
                self.btn_quitter_jeu.dessiner(self.ecran)

                if self.btn_facile.est_clique(pos_souris, clic): self.lancer_partie("FACILE")
                if self.btn_moyen.est_clique(pos_souris, clic): self.lancer_partie("MOYEN")
                if self.btn_difficile.est_clique(pos_souris, clic): self.lancer_partie("DIFFICILE")
                if self.btn_quitter_jeu.est_clique(pos_souris, clic): pygame.quit(); sys.exit()

            elif self.etat == "EN_COURS":
                for s in self.groupe_lettres:
                    pygame.draw.line(self.ecran, NOIR_DOUX, (s.rect.centerx-20, s.rect.bottom-5), (s.rect.centerx+20, s.rect.bottom-5), 2)
                self.tous_sprites.draw(self.ecran)

            elif self.etat == "GAME_OVER" or self.etat == "VICTOIRE":
                self.tous_sprites.draw(self.ecran)

                # Message différent selon l'état
                if self.etat == "GAME_OVER":
                    txt = f"PERDU ! LE MOT ÉTAIT : {self.mot}"
                    couleur_txt = NOIR_DOUX
                else:
                    txt = "BRAVO ! TU AS TROUVÉ !"
                    couleur_txt = (50, 150, 50)

                msg = pygame.font.SysFont("Arial", 35, bold=True).render(txt, True, couleur_txt)
                self.ecran.blit(msg, msg.get_rect(center=(LARGEUR_ECRAN//2, 380)))

                self.btn_rejouer.dessiner(self.ecran)
                self.btn_retour_menu.dessiner(self.ecran)

                if self.btn_rejouer.est_clique(pos_souris, clic):
                    self.lancer_partie(self.niveau_actuel)
                    pygame.time.delay(200) # Délai anti-rebond

                if self.btn_retour_menu.est_clique(pos_souris, clic):
                    self.etat = "MENU"
                    pygame.time.delay(250) # Délai plus long pour le retour menu

            pygame.display.flip()
            self.clock.tick(30)

    def gestion_tentative(self, lettre):
        trouve = False
        for s in self.groupe_lettres:
            if s.caractere == lettre and not s.decouverte:
                s.reveler()
                trouve = True

        if not trouve:
            if self.potence.erreur():
                self.etat = "GAME_OVER"

        if all(s.decouverte for s in self.groupe_lettres):
            self.etat = "VICTOIRE"

if __name__ == "__main__":
    JeuPendu().boucle()
