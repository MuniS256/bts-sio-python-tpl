#Exercice 1
"""
age = int(input(" Quel âge avez-vous ? : "))
if age >= 18 :
    print("Majeur")
else :
    print("Mineur")
"""
#Exercice 2
"""
nombre = int(input("Entrez un nombre :"))

if nombre > 0 :
    print ("Positif")
elif nombre < 0 :
    print ("Négatif")
else :
    print ("Egal à 0")
"""
#Exercice 3
"""
mot_de_passe = input("Entrez le mot de passe :")

if mot_de_passe == "pYth0n123*%?" :
    print ("Accès autorisé")
else :
    print ("Accès refusé")
"""
#Exercice 4
"""
note = int(input("Entre la note : "))

if note < 10 :
    print("Ajourné")
elif note > 10 and note < 12 :
    print("Passable")
elif note > 12 and note < 14 :
    print ("Assez Bien")
elif note > 14 and note < 16 :
    print ("Bien")
else :
    print ("Très bien")
"""
#Exercice 5
"""
nombre = int(input("Entrez un nombre :"))

if nombre % 2 == 0 :
    print("Pair")
else :
    print("Impair")
"""

#Exercice 6
"""
age=int(input("Quel est votre âge :"))
taille = int(input("Quel est votre taille :"))

if age >= 12 and taille >=140 :
    print ("Accès autorisé")
else :
    print ("Accès refusé")
"""
#Exercice 7
"""
def verifier_majorite(age):
    if age >= 18 :
        print("Majeur")
    else :
        print("Mineur")

verifier_majorite(20)
verifier_majorite(12)
"""
#Exercice 8
"""
def tarif(age):
    if age < 12 :
        print("Enfant")
    elif age >= 12 and age <= 17 :
        print("Adolescent")
    elif age > 17 and age <= 64 :
        print("Adulte")
    else :
        print("Senior")

tarif(17)
tarif(64)
tarif(65)
tarif(12)
"""
#Exercice 9
"""
nombre1=int(input("Entrez le premier nombre :"))
nombre2=int(input("Entrez le deuxième nombre :"))
opérateur=input("Entrez un opérateur(+,-,*,/) :")

def calculateur(nombre1, nombre2, opérateur):
    nombre1=int(nombre1)
    nombre2=int(nombre2)

    somme = nombre1 + nombre2
    soustraction = nombre1 + nombre2
    multiplication = nombre1 * nombre2
    division = nombre1 / nombre2

    if opérateur == "+":
        print(somme)
    elif opérateur == "-":
        print(soustraction)
    elif opérateur == "*":
        print(multiplication)
    elif opérateur == "/":
        print(division)
    else :
        print("Merci de respecter la consigne :(")

calculateur(nombre1, nombre2, opérateur)
"""
#Exercice 10
"""
login = input("Entrez votre identifiant :")
mdp = input("Entrez votre mot de passe :")

def connexion(login, mdp):
    login = str(login)
    mdp = str(mdp)

    if login == "root" and mdp == "!!_Ca_C_pYthon_**" :
        print("Accès autorisé")
    else :
        print("Identifiant incorrect ou Mot de passe incorrect")

connexion(login, mdp)
"""
#Bonus 1
"""
def verifier_mot_de_passe():
    mot_de_passe_correct = "Python123"
    tentatives = 0
    max_tentatives = 3

    while tentatives < max_tentatives:
        mot_de_passe = input("Entrez le mot de passe : ")
        if mot_de_passe == mot_de_passe_correct:
            print("Connexion réussie ! ✅")
            return  
        else:
            tentatives += 1
            print("Mot de passe incorrect ! ❌")
    
    print("Compte bloqué ! 🔒")

verifier_mot_de_passe()
"""
#Bonus 2
"""
import random

nombre_secret = random.randint(1, 10)
trouve = False

while trouve == False:
    proposition = int(input("Devine le nombre entre 1 et 100 : "))

    if proposition < nombre_secret:
        print("Trop petit !")
    elif proposition > nombre_secret:
        print("Trop grand !")
    else:
        print("Bravo, tu as trouvé !")
        trouve = True
"""
#Bonus 3
"""
prix = int(input("Entrez le nombre :"))
def calcul_prix(prix):
    réduction1= prix * (90/100)
    réduction2= prix * (80/100)
    réduction3= prix * (70/100)

    if prix < 50 :
        print("Aucune réduction")
    elif prix >= 50 and prix <= 99 :
        print(réduction1)
    elif prix >=100 and prix <=199 :
        print(réduction2)
    else :
        print(réduction3)

calcul_prix(prix)
"""
#Bonus 4
"""
mdp = input("Entrez un mot de passe :")
def valide_mdp(mdp):
    special = False
    majuscule = False
    minuscule = False

    for caractere in mdp :
        if caractere.isdigit():
            chiffre = True
        if caractere.isupper():
            majuscule = True
        if caractere.isalnum():
            special = True
        
    if len(mdp) >= 12 and caractere and chiffre and special:
        print("Mot de passe validé par la street")
    else:
        print("Mot de passe trop faible")

valide_mdp(mdp)
"""
