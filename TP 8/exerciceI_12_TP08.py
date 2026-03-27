#Exercice 1
"""
s = 0
list = [12, 15, 8, 10, 18]
for notes in list :
    s += notes
moyenne = s / len(list)
print("Les notes de la moyenne sont :", list)
print("La somme des notes de la classe est de : ", s)
print("La moyenne de la classe est de : ", moyenne)
"""
#Exercice 2
nombres = [2, 13, 9, 41, 7, 9, 12, 17, 8, 21, 3, 39]

pairs = []
compteur_superieur_10 = 0
valeur_max = nombres[0]
for n in nombres:
    if n % 2 == 0:
        pairs.append(n)
    
    if n > 10:
        compteur_superieur_10 += 1
        
    if n > valeur_max:
        valeur_max = n

print(f"Nombres pairs : {pairs}")
print(f"Nombre de valeurs supérieures à 10 : {compteur_superieur_10}")
print(f"La valeur maximale est : {valeur_max}")