#def bonsoir() :
#    print ("Bonsoir à tous")

#bonsoir()

#def acclamer(prenom):
#    print("Bonjour", prenom)

#acclamer("Jean-Louis")
#acclamer("Jean")
#acclamer("Joshua")
#acclamer("Laurent")

#def somme(a, b):
# resultat = a + b
# print("Résultat :", resultat)
#somme(87, 45)

#def calculer_somme():
# a = int(input("1er nombre : "))
# b = int(input("2ème nombre : "))
# print("Somme =", a + b)
#calculer_somme()

def trier_nombres():
    nombres = []

    for i in range(5):
        n = int(input("Entrez un nombre : "))
        nombres.append(n)

    nombres.sort()

    print("Les nombres du plus petit au plus grand :")
    print(nombres)

trier_nombres()