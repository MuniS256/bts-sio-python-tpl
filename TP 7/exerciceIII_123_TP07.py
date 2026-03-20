#Exercice 8
"""
def afficher_lettres(mot):
    for lettre in mot:
        print(lettre)
    
afficher_lettres("python")
"""
#Exercice 9
"""
def compter_voyelles(texte):
    voyelles = ["a","e","i","o","u","y","A","E","I","O","U","Y"]
    compteur = 0

    for lettre in texte:
        if lettre in voyelles:
            compteur += 1

    return compteur

print(compter_voyelles("letchi"))
"""
#Exercice 10
"""
def notes_valides(liste_notes):

    liste_final=[]

    for note in liste_notes:
        if note >= 10:
            liste_final.append(note)
    
    return liste_final

print (notes_valides([12, 15, 9, 17, 8, 14]))
"""