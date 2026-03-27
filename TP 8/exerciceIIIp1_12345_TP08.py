#Exercice 6
"""
def filtrer_pairs(liste):
    pairs = []
    for n in liste:
        if n % 2 == 0:
            pairs.append(n)
    return pairs

nombres = [1, 2, 3, 4, 5, 6]
resultat = filtrer_pairs(nombres)
print(resultat)
"""
#Exercice 7
"""
def inverser_liste(liste):
    liste_inversee = []
    for i in range(len(liste) - 1, -1, -1):
        liste_inversee.append(liste[i])
    return liste_inversee

nombres = [1, 2, 3, 4, 5]
resultat = inverser_liste(nombres)
print(resultat)  # Affiche [5, 4, 3, 2, 1]
"""
#Exercice 8
"""
def somme_indices_pairs(liste):
    somme = 0
    for i in range(0, len(liste), 2):
        somme += liste[i]
    return somme

nombres = [10, 5, 20, 3, 30]
resultat = somme_indices_pairs(nombres)
print(resultat) 
"""
#Exercice 9
"""
def supprimer_doublons(liste):
    sans_doublons = []
    for element in liste:
        if element not in sans_doublons:
            sans_doublons.append(element)
    return sans_doublons

nombres = [1, 2, 2, 3, 4, 4, 5]
resultat = supprimer_doublons(nombres)
print(resultat)
"""
#Exercice 10
"""
def deux_plus_grands(liste):
    if len(liste) < 2:
        return liste
    
    max1 = float('-inf')
    max2 = float('-inf')
    
    for n in liste:
        if n > max1:
            max2 = max1
            max1 = n
        elif n > max2:
            max2 = n
            
    return max1, max2

nombres = [12, 5, 19,10, 18, 7]
resultat = deux_plus_grands(nombres)
print(resultat)  
"""