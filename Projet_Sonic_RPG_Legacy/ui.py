import pygame

def draw_hp_bar(surface, x, y, display_hp, max_hp):
    """
    Dessine une barre de vie dynamique avec chiffres :
    - Fond gris foncé
    - Dégradé (Vert -> Jaune -> Rouge)
    - Affichage du texte "HP / MAX"
    """
    width = 150 
    height = 15 
    
    # 1. Fond de la barre
    pygame.draw.rect(surface, (40, 40, 40), (x, y, width, height))

    # 2. Calcul du ratio
    ratio = max(0, display_hp / max_hp)
    
    # 3. Calcul de la couleur (Vert -> Jaune -> Rouge)
    base_green = 210 
    if ratio > 0.5:
        r = int(255 * (1 - ratio) * 2)
        g = base_green
    else:
        r = 255
        g = int(base_green * ratio * 2)
    
    current_color = (max(0, min(255, r)), max(0, min(255, g)), 0)

    # 4. Dessin du remplissage
    current_width = width * ratio
    if current_width > 0:
        pygame.draw.rect(surface, current_color, (x, y, current_width, height))

    # 5. Bordure blanche
    pygame.draw.rect(surface, (255, 255, 255), (x, y, width, height), 2)

    # --- AJOUT : Affichage des chiffres HP ---
    font_stats = pygame.font.SysFont("Arial", 14, bold=True)
    hp_text = f"{int(display_hp)} / {max_hp}"
    # On affiche le texte juste à droite de la barre
    draw_text(hp_text, font_stats, (255, 255, 255), surface, x + width + 40, y + height//2)

def draw_mana_bar(surface, x, y, current_mp, max_mp):
    """
    Dessine une barre de mana bleue sous la barre de vie.
    """
    width = 120 # Un peu plus courte que la barre de vie
    height = 10
    
    # 1. Fond
    pygame.draw.rect(surface, (20, 20, 40), (x, y, width, height))
    
    # 2. Remplissage Bleu
    ratio = max(0, current_mp / max_mp)
    pygame.draw.rect(surface, (0, 150, 255), (x, y, width * ratio, height))
    
    # 3. Bordure
    pygame.draw.rect(surface, (200, 200, 255), (x, y, width, height), 1)
    
    # --- AJOUT : Affichage des chiffres MP ---
    font_stats = pygame.font.SysFont("Arial", 12, bold=True)
    mp_text = f"{int(current_mp)} MP"
    draw_text(mp_text, font_stats, (0, 200, 255), surface, x + width + 25, y + height//2)

def draw_text(text, font, color, surface, x, y, outline_color=(0, 0, 0), thickness=2):
    """
    Affiche un texte avec un contour pour une meilleure lisibilité.
    """
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))

    # Dessin du contour (4 directions)
    for dx, dy in [(-thickness, 0), (thickness, 0), (0, -thickness), (0, thickness)]:
        outline_obj = font.render(text, True, outline_color)
        outline_rect = outline_obj.get_rect(center=(x + dx, y + dy))
        surface.blit(outline_obj, outline_rect)

    # Dessin du texte principal
    surface.blit(text_obj, text_rect)

# Dans ui.py

def grayscale_surface(surface):
    """Prend une surface et la retourne en niveaux de gris."""
    # On crée une copie pour ne pas modifier l'original
    arr = pygame.surfarray.pixels3d(surface)
    # Formule standard de luminance pour le gris
    # Gris = 0.3*R + 0.59*G + 0.11*B
    mean = (arr[..., 0] * 0.3 + arr[..., 1] * 0.59 + arr[..., 2] * 0.11).astype(arr.dtype)
    arr[..., 0] = mean
    arr[..., 1] = mean
    arr[..., 2] = mean
    # On libère le tableau pour appliquer les changements
    del arr 
    return surface