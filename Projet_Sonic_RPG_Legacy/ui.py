import pygame

def draw_hp_bar(surface, x, y, hp, max_hp):
    # Dessine le fond de la barre (Rouge/Vide)
    pygame.draw.rect(surface, (100, 0, 0), (x, y, 150, 15))
    # Dessine la vie actuelle (Vert)
    fill = (hp / max_hp) * 150
    if fill > 0:
        pygame.draw.rect(surface, (0, 255, 0), (x, y, fill, 15))
    # Bordure blanche
    pygame.draw.rect(surface, (255, 255, 255), (x, y, 150, 15), 2)

def draw_text(text, font, color, surface, x, y, outline_color=(0, 0, 0), thickness=2):
    """
    Cette fonction dessine le texte avec un contour noir (outline)
    """
    # 1. Rendre le texte principal pour obtenir sa taille (rect)
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))

    # 2. DESSINER LE CONTOUR
    # On dessine le même texte en noir avec un léger décalage dans les 4 directions
    for dx, dy in [(-thickness, 0), (thickness, 0), (0, -thickness), (0, thickness)]:
        outline_obj = font.render(text, True, outline_color)
        outline_rect = outline_obj.get_rect(center=(x + dx, y + dy))
        surface.blit(outline_obj, outline_rect)

    # 3. DESSINER LE TEXTE ORIGINAL PAR-DESSUS
    surface.blit(text_obj, text_rect)