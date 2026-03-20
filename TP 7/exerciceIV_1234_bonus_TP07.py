#Exercice 1
"""
def affiche_carre (n):
    for i in range(1, n+1):
        print(i**2)

affiche_carre(13)
"""
#Exercice 2
"""
def dessiner_carre (n):
 
    for i in range(4):
        print("****")

dessiner_carre(1)
"""
#Exercice 3
"""
def plus_grand_nombre():
    a = float(input("Entrez le premier nombre : "))
    b = float(input("Entrez le deuxième nombre : "))
    c = float(input("Entrez le troisième nombre : "))
    
    plus_grand = max(a, b, c)
    
    print("Le plus grand nombre est :", plus_grand)

plus_grand_nombre()
"""
#Exercice 4
def trier_liste(liste):
    n = len(liste)
    
    for i in range(n):
        for j in range(0, n - i - 1):
            
            if liste[j] > liste[j + 1]:
            
                liste[j], liste[j + 1] = liste[j + 1], liste[j]
    

    print("Liste triée :", liste)

ma_liste = [7, 2, 9, 1, 5]
trier_liste(ma_liste)