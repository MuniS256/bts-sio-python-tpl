#Exercice 1
"""
vente= int(input("Entrez votre nombre de vente :"))
salaire= 300000
supplémentaire = 10000
bonus = (vente - 14) * 10000

def nombre_de_vente(vente):
    vente1 = salaire + (salaire * 10/100)
    vente2 = salaire + (salaire * 10/100) + bonus

    if vente < 10:
        print("300 000 Frs, Tu y es presque ! plus que quelques ventes pour toucher la prime le mois prochain !")
    elif vente >= 10 and vente < 15:
        print(f"Bien joué, {vente1}")
    else:
        print(f"Félicitation, {vente2}")

nombre_de_vente(vente)
"""
#Exercice 2
"""
def compter_voyelles(mot):
    voyelles = "aeiouy"
    compteur = 0

    for lettre in mot.lower():
        if lettre in voyelles:
            compteur += 1

    print(compteur, "voyelles")

compter_voyelles("python")    
"""