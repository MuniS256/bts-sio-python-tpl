mot = input("Entrez un mot : ")
def compter_voyelles(mot):
    voyelles=["a","e","i","o","u","y","A","E","I","O","U","Y"]
    compteur = 0

    for lettre in mot:
        if lettre in voyelles:
            compteur += 1

    print(f"Le nombre de voyelles est : {compteur}")

compter_voyelles(mot)
    
