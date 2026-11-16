# -*- coding: utf-8 -*-
"""
Séance 2 - Partie A : découper le traitement des taux en fonctions.
Lancer avec : python fonctions.py
"""

import csv
import os
from statistics import mean

DOSSIER = os.path.dirname(os.path.abspath(__file__))
DONNEES = os.path.join(DOSSIER, "donnees")


def lire_csv(chemin, devise):
    """Lit le CSV des taux (colonnes date,<devise>) et renvoie une liste de couples (date, taux)."""
    couples = []
    with open(chemin, encoding="utf-8") as fichier:
        lecteur = csv.DictReader(fichier)
        for ligne in lecteur:
            couples.append((ligne["date"], float(ligne[devise])))
    return couples


def moyenne(taux):
    """Calcule la moyenne d'une liste de taux avec une boucle."""
    if len(taux) == 0:
        raise ValueError("Impossible de calculer la moyenne d'une liste vide.")
    total = 0
    for t in taux:
        total = total + t
    return total / len(taux)


def minimum_maximum(taux):
    """Renvoie le couple (minimum, maximum) d'une liste de taux non vide."""
    if len(taux) == 0:
        raise ValueError("Une liste vide n'a ni minimum ni maximum.")
    minimum = taux[0]
    maximum = taux[0]
    for t in taux:
        if t < minimum:
            minimum = t
        if t > maximum:
            maximum = t
    return minimum, maximum


def main():
    for devise in ["THB", "USD"]:
        chemin = os.path.join(DONNEES, "taux_EUR_" + devise + ".csv")
        couples = lire_csv(chemin, devise)
        taux = [t for _, t in couples]

        ma_moyenne = moyenne(taux)
        moyenne_stat = mean(taux)          # A.2 : fonction de la bibliothèque standard
        mini, maxi = minimum_maximum(taux)

        print("=== EUR/" + devise + " ===")
        print("Nombre de taux :", len(taux), "(du", couples[0][0], "au", couples[-1][0] + ")")
        print("Moyenne (notre fonction)     :", ma_moyenne)
        print("Moyenne (statistics.mean)    :", moyenne_stat)
        print("Écart entre les deux         :", abs(ma_moyenne - moyenne_stat))
        print("Minimum :", mini, "- Maximum :", maxi)
        print()


if __name__ == "__main__":
    main()
