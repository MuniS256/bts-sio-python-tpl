#Exercice 1
"""
notes = [int(x) for x in ["17","2","10","12","11"]]

print("Les notes sont", notes)

somme = sum(notes)

print("La somme des notes est", somme)

moyenne = sum(notes) / len(notes)

print("La moyenne des notes est :", moyenne)
"""
#Exercice 2
nombres = [2, 13, 9, 41, 7, 9, 12, 17, 8, 21, 3, 39]

# Afficher les nombres pairs uniquement
print("Nombres pairs :")
for nombre in nombres:
    if nombre % 2 == 0:
        print(nombre)

# Compter le nombre de valeurs > 10
compteur = 0
for nombre in nombres:
    if nombre > 10:
        compteur += 1

print("Nombre de valeurs > 10 :", compteur)

# Afficher la valeur maximale
print("Valeur maximale :", max(nombres))