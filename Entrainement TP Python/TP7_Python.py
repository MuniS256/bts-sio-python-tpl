#Exercice 1
"""
i = 0

while i <= 10:
    print (i)
    i = i + 1
"""
#Exercice 2
"""
i=10
while i >= 0 :
    print (i)
    i = i - 1
"""
#Exercice 3
"""
nombre = int(input("Entrez un nombre : "))
i = 1
somme = 0

while i <= nombre:
    somme = somme + i
    i = i + 1

print("Résultat :", somme)
"""
#Exercice 4
"""
mot_de_passe = input("Entrez le mot de passe :")

while mot_de_passe != "python":
    mot_de_passe = input("Mot de passe incorrect, réessayez : ")

print("Accès autorisé")
"""
#Exercice 5
"""
def afficher_nombres(n):
    i = 0
    for i in range(0, 6):
        print (i)
        i= i + 1

afficher_nombres(0)
"""
#Exercice 6
"""
nombre=int(input("Entrez un nombre : "))
def table_mult(nombre):

    for i in range (1,11):
        multiplication = nombre * i 
        print (multiplication)

table_mult(nombre)
"""
#Exercice 7
"""
def somme_nombres(n):
    somme = 0

    for i in range(1, n + 1):
        somme += i

    return somme

print(somme_nombres(10))
"""
#Exercice 8
"""
mot=input("Entrez un mot: ")
def afficher_lettres(mot):

    for lettre in mot:
        print (lettre)

afficher_lettres(mot)
"""
#Exercice 9
"""
texte = input("Entrez un mot :")
def compter_voyelles(texte):
    voyelles=["a","e","i","o","u","y","A","E","I","O","U","Y"]
    compteur = 0

    for lettre in texte:
        if lettre in voyelles:
            compteur += 1

    print(f"Le nombre de voyelle est : {compteur}")

compter_voyelles(texte)
"""
#Exercice 10
"""
liste_notes = []

def notes_valides(liste_notes):
    liste_notes = []
    
    while True:
        note = input("Entrez une note ('stop' pour arrêter) : ")

        if note.lower() == "stop":
            break

        note = float(note)   # transforme le texte en nombre

        if note >= 10:
            liste_notes.append(note)
    
    return liste_notes

print(notes_valides(liste_notes))
"""