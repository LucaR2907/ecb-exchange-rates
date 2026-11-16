# -*- coding: utf-8 -*-
"""
Séance 1 - C.2 : appeler l'API Frankfurter pour de vrai.
API Frankfurter (taux de référence de la BCE, base euro, sans clé).
    https://api.frankfurter.app  -  doc : https://frankfurter.dev
Devises du groupe : THB (baht thaïlandais) et USD (dollar américain).

1. Taux du jour   : /latest?from=EUR&to=THB
2. Série 01/01/2026 -> 01/09/2026 : /2026-01-01..2026-09-01?from=EUR&to=THB
   -> réponse brute enregistrée dans cache/
   -> version simple en CSV (une ligne par date) dans donnees/
Bibliothèque standard uniquement : urllib.request, json, os.

Lancer avec : python api_frankfurter.py
"""

import json
import os
import urllib.request

# --- Paramètres --------------------------------------------------------------

BASE = "EUR"               # devise de base (paramètre from)
DEVISES = ["THB", "USD"]   # devises du groupe (paramètre to)
DEBUT = "2026-01-01"
FIN = "2026-09-01"

API = "https://api.frankfurter.app"

# Les dossiers cache/ et donnees/ sont à côté du script, quel que soit
# le répertoire depuis lequel on lance le programme.
DOSSIER = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(DOSSIER, "cache")
DONNEES = os.path.join(DOSSIER, "donnees")


def telecharger(url):
    """Appelle l'URL et renvoie (texte_brut, dictionnaire Python)."""
    # Sans en-tête User-Agent, Python se présente comme "Python-urllib" et
    # l'API répond 403 (Forbidden) : on indique donc un nom de client.
    requete = urllib.request.Request(url, headers={"User-Agent": "projet-python-groupe-X"})
    with urllib.request.urlopen(requete) as reponse:
        brut = reponse.read().decode("utf-8")
    return brut, json.loads(brut)


def enregistrer_texte(chemin, texte):
    """Écrit un texte dans un fichier UTF-8."""
    with open(chemin, "w", encoding="utf-8") as fichier:
        fichier.write(texte)


# --- 1) Taux du jour ---------------------------------------------------------

def taux_du_jour(devise):
    url = API + "/latest?from=" + BASE + "&to=" + devise
    print("Appel :", url)

    brut, donnees = telecharger(url)

    # Même forme que le dictionnaire de la partie C.1 :
    # {"amount": 1.0, "base": "EUR", "date": "...", "rates": {"THB": ...}}
    date = donnees["date"]
    taux = donnees["rates"][devise]
    print("Date  :", date)
    print("Taux  : 1 " + BASE + " = " + str(taux) + " " + devise)

    # On garde aussi la réponse brute dans cache/
    enregistrer_texte(os.path.join(CACHE, "latest_" + BASE + "_" + devise + ".json"), brut)
    return date, taux


# --- 2) Série sur une période ------------------------------------------------

def serie(devise):
    url = API + "/" + DEBUT + ".." + FIN + "?from=" + BASE + "&to=" + devise
    print("Appel :", url)

    brut, donnees = telecharger(url)

    # a) réponse brute dans cache/
    nom_cache = "serie_" + BASE + "_" + devise + "_" + DEBUT + "_" + FIN + ".json"
    enregistrer_texte(os.path.join(CACHE, nom_cache), brut)
    print("Réponse brute enregistrée dans : cache/" + nom_cache)

    # b) version simple en CSV dans donnees/ (une ligne par date)
    # Ici "rates" est indexé par date : {"2026-01-02": {"THB": ...}, ...}
    rates = donnees["rates"]
    dates = sorted(rates.keys())   # tri chronologique (format AAAA-MM-JJ)

    lignes = ["date," + devise]
    for d in dates:
        lignes.append(d + "," + str(rates[d][devise]))
    nom_csv = "taux_" + BASE + "_" + devise + ".csv"
    enregistrer_texte(os.path.join(DONNEES, nom_csv), "\n".join(lignes) + "\n")

    print("CSV écrit dans : donnees/" + nom_csv)
    print("Nombre de jours ouvrés :", len(dates))
    print("Premier jour :", dates[0], "->", rates[dates[0]][devise])
    print("Dernier jour :", dates[-1], "->", rates[dates[-1]][devise])
    return dates, rates


# --- Programme principal -----------------------------------------------------

def main():
    # On s'assure que les dossiers existent
    os.makedirs(CACHE, exist_ok=True)
    os.makedirs(DONNEES, exist_ok=True)

    for devise in DEVISES:
        print("=== " + BASE + "/" + devise + " : taux du jour ===")
        taux_du_jour(devise)
        print("=== " + BASE + "/" + devise + " : série du " + DEBUT + " au " + FIN + " ===")
        serie(devise)
        print()


if __name__ == "__main__":
    main()
