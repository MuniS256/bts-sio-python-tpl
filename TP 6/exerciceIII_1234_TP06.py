#Exercice 1
"""
def verifier_majorite(age) :
    if int(age) > 18 :
        print ("Vous êtes majeur")
    else :
        print ("Vous êtes mineur")

verifier_majorite(21)
verifier_majorite(28)
verifier_majorite(12)
"""
#Exercice 2
"""
def tarif(age):
    if int(age)<=12:
        print("Enfant")
    elif int(age)>12 and int(age)<17:
        print("Adolescent")
    elif int(age)>17 and int(age)<=64:
        print("Adulte")
    else :
        print("Senior")

tarif(64)
tarif(13)
tarif(10)
tarif(78)
"""

#Exercice 3
"""
def calculateur(nombre1, nombre2, opérateur) :
    nombre1 = input("Quel est le premier nombre ?")
    nombre2 = input("Quel est le deuxième nombre ?")
    opérateur = input("Quel est l'opérateur ?")
    if opérateur == "+" :
        print (int(nombre1) + int(nombre2))
    elif opérateur == "-" :
        print (int(nombre1) - int(nombre2))
    elif opérateur == "*" :
        print (int(nombre1) * int(nombre2))
    elif opérateur == "/" :
        print (int(nombre1) / int(nombre2))
calculateur(0,0,"+")
calculateur(0,0,"-")
calculateur(0,0,"*")
calculateur(0,0,"/")
stop = input("Stop") 
"""

#Exercice 4

"""
def connexion(login, mdp) :  
    if str(login) == "root" and str(mdp) == "!!_Ca_C_pYthon_**" :
        print ("Connexion réussie")
    elif str(login) != "root":
        print ("Identifiant incorrect")
    elif str(mdp) != "!!_Ca_C_pYthon_**" :
        print ("Mot de passe incorrect")
    
connexion("root","sio")
"""