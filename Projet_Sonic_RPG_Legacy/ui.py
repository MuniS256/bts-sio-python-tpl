# ui.py
import pygame

def draw_hp_bar(surface, x, y, display_hp, max_hp):
    """
    Dessine une barre de vie dynamique :
    - Fond gris foncé (pour le "vide")
    - Dégradé progressif (Vert moyen -> Jaune -> Rouge vif)
    - Bordure blanche stylée
    On utilise 'display_hp' pour l'animation de glissement.
    """
    width = 150 # Largeur totale de la barre
    height = 15 # Hauteur de la barre
    
    # 1. Dessin du fond (gris foncé pour le "vide")
    # Cela permet de bien voir la vie perdue, comme dans Sonic RPG
    pygame.draw.rect(surface, (40, 40, 40), (x, y, width, height))

    # 2. Calcul du ratio d'affichage (0.0 à 1.0)
    # Important : On utilise max(0, ...) pour ne pas avoir de barre négative si hp < 0
    ratio = max(0, display_hp / max_hp)
    
    # 3. Dynamique des couleurs (Vert -> Jaune -> Rouge)
    # Plus le ratio est petit, plus la couleur tend vers le rouge vif.
    
    # On commence avec un vert "moyen/juste milieu" équilibré
    base_green = 210 # Pas trop flashy (255) ni trop sombre
    
    if ratio > 0.5:
        # Entre 100% et 50% : Transition de Vert moyen vers Jaune
        # Le Rouge augmente
        r = int(255 * (1 - ratio) * 2)
        g = base_green # Reste sur le vert de base
    else:
        # Entre 50% et 0% : Transition de Jaune vers Rouge vif
        # Le Vert diminue et le Rouge devient éclatant (255)
        r = 255
        # Le vert diminue proportionnellement, mais part de base_green
        g = int(base_green * ratio * 2)
    
    # Couleur finale calculée (r, g, b=0)
    current_color = (r, g, 0)

    # 4. Dessin de la barre de vie actuelle
    current_width = width * ratio
    if current_width > 0:
        pygame.draw.rect(surface, current_color, (x, y, current_width, height))

    # 5. Bordure blanche stylée (2px d'épaisseur)
    pygame.draw.rect(surface, (255, 255, 255), (x, y, width, height), 2)

def draw_text(text, font, color, surface, x, y, outline_color=(0, 0, 0), thickness=2):
    """
    (Ton code draw_text reste le même, il est très bien)
    """
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))

    for dx, dy in [(-thickness, 0), (thickness, 0), (0, -thickness), (0, thickness)]:
        outline_obj = font.render(text, True, outline_color)
        outline_rect = outline_obj.get_rect(center=(x + dx, y + dy))
        surface.blit(outline_obj, outline_rect)

    surface.blit(text_obj, text_rect)