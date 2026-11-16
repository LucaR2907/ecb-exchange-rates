# -*- coding: utf-8 -*-
"""
Séance 1 - C.1 : explorer un dictionnaire (avant tout appel réseau).
Lancer avec : python explorer_dictionnaire.py
"""

import copy

reponse = {
    "amount": 1.0,
    "base": "EUR",
    "date": "2024-01-02",
    "rates": {"USD": 1.0956},
}

# 1. Afficher une valeur à partir de sa clé
print("1. Date :", reponse["date"])
print("1. Taux USD :", reponse["rates"]["USD"])

# 2. Affecter une valeur à une clé qui existe déjà
reponse["date"] = "2099-01-01"
print("2.", reponse)
# -> la nouvelle valeur remplace l'ancienne : une clé est unique

# 3a. Copie superficielle, modification d'une clé de premier niveau
copie = reponse.copy()
copie["amount"] = 1.5
print("3a. copie    :", copie)
print("3a. original :", reponse)
# -> l'original n'est pas modifié

# 3b. Copie superficielle, modification de la partie imbriquée rates
copie["rates"]["USD"] = 1.20
print("3b. copie    :", copie)
print("3b. original :", reponse)
# -> l'original EST modifié : copie et original partagent le même
#    sous-dictionnaire rates

# 4. Copie profonde : les parties imbriquées sont aussi copiées
copie_profonde = copy.deepcopy(reponse)
copie_profonde["rates"]["USD"] = 1.30
print("4. copie profonde :", copie_profonde)
print("4. original       :", reponse)
# -> l'original n'est plus affecté
