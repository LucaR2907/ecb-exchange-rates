# -*- coding: utf-8 -*-
"""
Séance 1 - Partie A : types, opérations, conditions et boucles.
Lancer avec : python bases_python.py
"""

# --- A.3 Les types de base ---------------------------------------------------
print("=== A.3 Les types de base ===")

age = 19                                   # entier
taille = 1.83                              # décimal
prenom = "Victor"                          # chaîne de caractères
majeur = True                              # booléen
notes = [12, 15, 18]                       # liste
personne = {"prenom": "Victor", "age": 19}  # dictionnaire

for valeur in [age, taille, prenom, majeur, notes, personne]:
    print(valeur, "->", type(valeur))

# "3" + 4 provoque une erreur : on ne peut pas additionner un str et un int
try:
    print("3" + 4)
except TypeError as erreur:
    print('"3" + 4 donne une erreur :', erreur)
print('int("3") + 4 =', int("3") + 4)
print('"3" + str(4) =', "3" + str(4))


# --- A.4 Les opérations ------------------------------------------------------
print()
print("=== A.4 Les opérations ===")

# Arithmétique
a = 9
b = 2
print("a + b =", a + b)     # addition
print("a - b =", a - b)     # soustraction
print("a * b =", a * b)     # multiplication
print("a / b =", a / b)     # division (résultat décimal)
print("a // b =", a // b)   # division euclidienne (quotient entier)
print("a % b =", a % b)     # reste de la division euclidienne
print("a ** b =", a ** b)   # puissance

# Chaînes de caractères
texte = "Bonjour"
suite = " je m'appelle Victor"
phrase = texte + suite                     # concaténation
print(phrase)
print(phrase.upper())                      # tout en majuscules
print(phrase.split())                      # découpe en liste de mots
print(phrase.replace("Victor", "Luca"))    # remplace un mot

# Listes
taux = [1.08, 1.10]
taux.append(1.12)                          # ajout d'un élément à la fin
print("Liste :", taux)
print("Longueur :", len(taux))
print("Élément d'indice 0 :", taux[0])     # le premier élément est à l'indice 0

# Dictionnaires
ages = {"Luca": 20, "Victor": 19}
print("Âge de Luca :", ages["Luca"])       # accès à une valeur
ages["Paul"] = 21                          # ajout d'une clé
print("Dictionnaire :", ages)

# Comparaisons : elles renvoient un booléen
x = 1
y = 2
print("x == y :", x == y)
print("x != y :", x != y)
print("x < y :", x < y)
print("x > y :", x > y)
print("x <= y :", x <= y)
print("x >= y :", x >= y)

# Opérateurs booléens
age = 20
permis = True
print("age >= 18 and permis :", age >= 18 and permis)  # vrai si les deux sont vrais
print("age < 18 or permis :", age < 18 or permis)      # vrai si au moins un est vrai
print("not permis :", not permis)                      # inverse le booléen


# --- A.5 Les conditions ------------------------------------------------------
print()
print("=== A.5 Les conditions ===")

# On teste plusieurs valeurs de taux (des décimaux, pas des entiers)
for taux_test in [1.08, 1.0, 0.95]:
    if taux_test > 1:
        message = "au-dessus de 1"
    elif taux_test == 1:
        message = "égal à 1"
    else:
        message = "en-dessous de 1"
    print("taux =", taux_test, "->", message)


# --- A.6 Les boucles ---------------------------------------------------------
print()
print("=== A.6 Les boucles ===")

# Quelques taux EUR/THB réels (début janvier 2026)
liste_taux = [36.792, 36.596, 36.608, 36.606, 36.823]

# Boucle for : on connaît la liste à parcourir
somme = 0
for t in liste_taux:
    print("taux :", t)
    somme = somme + t
print("Somme avec for :", round(somme, 3))

# Boucle while : on répète tant qu'une condition est vraie
somme = 0
i = 0
while i < len(liste_taux):
    somme = somme + liste_taux[i]
    i = i + 1
print("Somme avec while :", round(somme, 3))
