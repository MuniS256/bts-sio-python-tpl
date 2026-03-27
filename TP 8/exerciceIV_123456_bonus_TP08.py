#Bonus 1
"""
def gerer_erreur(mot, lettre, vies):
    if lettre not in mot:
        vies -= 1
    return vies

vies_joueur = 5
vies_joueur = gerer_erreur("python", "z", vies_joueur)
print(vies_joueur) 
vies_joueur = gerer_erreur("python", "p", vies_joueur)
print(vies_joueur)
"""
#Bonus 2
"""
def afficher_etat(mot, lettres_trouvees, lettres_testees):
    resultat = ""
    for lettre in mot:
        if lettre in lettres_trouvees:
            resultat += lettre
        else:
            resultat += "_"
    
    print(f"Mot : {resultat}")
    print(f"Lettres testées : {', '.join(lettres_testees)}")

mot = "python"
trouvees = ["p", "o"]
testees = ["p", "o", "z", "a"]

afficher_etat(mot, trouvees, testees)
"""
#Bonus 3
"""
def lettre_deja_proposee(lettre, lettres_testees):
    return lettre in lettres_testees

testees = ["a", "p", "z"]
print(lettre_deja_proposee("p", testees))  
print(lettre_deja_proposee("y", testees)) 
"""
#Bonus 4
"""
import random

def choisir_mot(liste_mots):
    return random.choice(liste_mots)

mots = ["python", "reseau", "serveur"]
mot_choisi = choisir_mot(mots)
print(mot_choisi)  
"""
#Bonus 5
"""
def lettres_restantes(mot, lettres_trouvees):
    compteur = 0
    for lettre in mot:
        if lettre not in lettres_trouvees:
            compteur += 1
    return compteur

mot = "python"
lettres = ["p", "o"]
print(lettres_restantes(mot, lettres)) 
"""
#Bonus 6
import random


def afficher_etat(mot, lettres_trouvees, lettres_testees, vies):
    affichage_mot = ""
    for lettre in mot:
        if lettre in lettres_trouvees:
            affichage_mot += lettre
        else:
            affichage_mot += "_"
    
    print(f"\nMot : {affichage_mot}")
    print(f"Vies restantes : {vies}")
    print(f"Lettres déjà testées : {', '.join(lettres_testees)}")

def mot_complet(mot, lettres_trouvees):
    for lettre in mot:
        if lettre not in lettres_trouvees:
            return False
    return True


mots = ["python", "reseau", "serveur", "code", "instruction", 
        "algorithmie", "boucle", "condition", "fonction", "indentation"]

mot_a_deviner = random.choice(mots)
lettres_trouvees = []
lettres_testees = []
vies = 6  

print("=== BIENVENUE AU JEU DU PENDU ===")


while vies > 0 and not mot_complet(mot_a_deviner, lettres_trouvees):
    afficher_etat(mot_a_deviner, lettres_trouvees, lettres_testees, vies)
    
    proposition = input("Proposez une lettre : ").lower()

   
    if proposition in lettres_testees:
        print(f"-> Vous avez déjà testé la lettre '{proposition}' !")
        continue 
    
    
    lettres_testees.append(proposition)

    
    if proposition in mot_a_deviner:
        print("-> Bien joué !")
        lettres_trouvees.append(proposition)
    else:
        vies -= 1
        print(f"-> Raté ! Il ne vous reste que {vies} vies.")



if mot_complet(mot_a_deviner, lettres_trouvees):
    print(f"\nBRAVO ! Vous avez trouvé le mot : {mot_a_deviner}")
else:
    print(f"\nDOMMAGE... Vous avez perdu. Le mot était : {mot_a_deviner}")