#Exercice 3
"""
def ajouter_note(liste, note):
   

    liste.append(note)
    return liste

mes_notes = [12, 15, 8]
nouvelle_note = 18

mes_notes = ajouter_note(mes_notes, nouvelle_note)

print(f"Ma nouvelle liste de notes : {mes_notes}")
"""
#Exercice 4
"""
def ajouter_note(liste, note):
    liste.append(note)
    return liste

def compter_sup(liste, seuil):
    compteur = 0
    for element in liste:
        if element > seuil:
            compteur += 1
    return compteur

mes_notes = [12, 15, 8, 10, 18, 5, 14]
limite = 10

resultat = compter_sup(mes_notes, limite)
print(f"Il y a {resultat} notes strictement supérieures à {limite}.")
"""
#Exercice 5
"""
def multiplier_liste(liste, facteur):
    nouvelle_liste = []
    for element in liste:
        nouvelle_liste.append(element * facteur)
    return nouvelle_liste

notes = [10, 15, 8]
resultat = multiplier_liste(notes, 2)
print(resultat) 
"""