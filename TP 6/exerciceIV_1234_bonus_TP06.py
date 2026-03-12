#Exercice 1
"""
def authentification():
    essais = 3
    
    while essais > 0:
        mdp = input("Entrez le mot de passe : ")
        
        if mdp == "Kazuya":
            print("Mot de passe correct")
            return
        else:
            essais -= 1
            if essais > 0:
                print("Mot de passe incorrect")
                print("Il reste", essais, "essai(s)")
            else:
                print("Accès refusé")

authentification()
"""

#Exercice 2
"""
from random import randint
x = randint(0, 10)
i = 1
e = int(input("Choisis un nombre entre 0 et 10 : "))
while e != x:
    if e < x:
        print("Trop petit")
    else:
        print("Trop grand")
    
    e = int(input("Essaie encore : "))
    i += 1
print("Bravo ! Tu as gagné en", i, "essai(s) !")
"""
#Exercice 3
"""
def calcul_prix(prix) :
    if int(prix) < 50 :
        print ("Aucune")
    elif int(prix) >= 50 and int(prix) < 100 :
        print ("10%")
    elif int(prix) >= 100 and int(prix) < 200 :
        print ("20%")
    elif int(prix) >= 200 :
        print ("30%")
calcul_prix(30)
calcul_prix(75) 
calcul_prix(150)
calcul_prix(250)
"""
#premier test
"""
def calcul_prix(prix):
    if prix < 50:
        reduction = 0
    elif prix <= 99:
        reduction = 0.10
    elif prix <= 199:
        reduction = 0.20
    else:
        reduction = 0.30

    prix_final = prix * (1 - reduction)
    print(f"Le prix final après réduction est de : {prix_final:.2f} €")

calcul_prix(30)
calcul_prix(75) 
calcul_prix(150)
calcul_prix(250)
"""
#version finale

#Exercice 4
"""
def valide_mdp(mdp):
    # Initialisation des compteurs/indicateurs
    longueur_ok = len(mdp) >= 12
    a_chiffre = False
    a_majuscule = False
    a_special = False
    
    # On parcourt chaque caractère une seule fois pour l'efficacité
    for carac in mdp:
        if carac.isdigit():
            a_chiffre = True
        elif carac.isupper():
            a_majuscule = True
        elif not carac.isalnum(): # Si ce n'est ni lettre ni chiffre, c'est spécial
            a_special = True
            
    # Vérification finale
    if longueur_ok and a_chiffre and a_majuscule and a_special:
        print("Mot de passe robuste")
    else:
        print("Mot de passe trop faible")

valide_mdp("LM82ak04")
valide_mdp("LM82ak04!")
valide_mdp("SIO2027lesmeilleurs:!:")
"""