#Exercice 6

def afficher_mot_cache(mot, lettres_trouvees):
    resultat = ""
    for lettre in mot:
        if lettre in lettres_trouvees:
            resultat += lettre
        else:
            resultat += "_"
    print(resultat)
    return resultat
"""
mot = "python"
lettres = ["p", "o"]
afficher_mot_cache(mot, lettres)
"""
#Exercice 7

def lettre_dans_mot(mot, lettre):
    if lettre in mot:
        return True
    else:
        return False
"""
print(lettre_dans_mot("python", "p"))  
print(lettre_dans_mot("python", "z")) 
"""
#Exercice 8

def ajouter_lettre(liste, lettre):
    if lettre not in liste:
        liste.append(lettre)
    return liste
"""
lettres = ["p", "o"]
lettres = ajouter_lettre(lettres, "p")
print(lettres)  

lettres = ajouter_lettre(lettres, "y")
print(lettres) 
"""
#Exercice 9

def mot_complet(mot, lettres_trouvees):
    for lettre in mot:
        if lettre not in lettres_trouvees:
            return False
    return True
"""
print(mot_complet("python", ["p", "y", "t", "h", "o", "n"])) 
print(mot_complet("python", ["p", "o"]))                     
"""
#Exercice 10
mot_a_deviner = "python"
lettres_trouvees = []

while not mot_complet(mot_a_deviner, lettres_trouvees):
    choix = input("Lettre ? : ")
    
    lettres_trouvees = ajouter_lettre(lettres_trouvees, choix)
    
    afficher_mot_cache(mot_a_deviner, lettres_trouvees)

print("Félicitations, vous avez trouvé le mot !")