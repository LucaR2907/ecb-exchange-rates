# -*- coding: utf-8 -*-
"""
Séance 4 - Partie D : l'outil en ligne de commande du projet.

Exemples :
    python main.py --help
    python main.py extraire              # met à jour les CSV depuis l'API (séance 2)
    python main.py analyser              # Python idiomatique + classes (séance 4)
    python main.py analyser --devise USD
    python main.py graphiques            # crée les PNG dans figures/
"""

import argparse

from src.graphiques import tracer_tout
from src.idiomatique import analyser
from src.serie import charger_series


def commande_extraire(args):
    import api_securisee   # appel protégé par try/except et journalisé
    api_securisee.main()


def commande_analyser(args):
    series = charger_series()
    # On met la devise choisie en premier
    series.sort(key=lambda s: s.devise != args.devise)
    analyser(series)


def commande_graphiques(args):
    for chemin in tracer_tout(charger_series(), args.dossier):
        print("PNG créé :", chemin)


def main():
    parser = argparse.ArgumentParser(description="Projet Python - taux EUR/THB et EUR/USD (BCE)")
    sous = parser.add_subparsers(dest="commande", required=True)

    p = sous.add_parser("extraire", help="télécharger les séries depuis l'API Frankfurter")
    p.set_defaults(fonction=commande_extraire)

    p = sous.add_parser("analyser", help="statistiques et démonstrations des séances 4 A et B")
    p.add_argument("--devise", choices=["THB", "USD"], default="THB")
    p.set_defaults(fonction=commande_analyser)

    p = sous.add_parser("graphiques", help="créer les graphiques PNG")
    p.add_argument("--dossier", default="figures")
    p.set_defaults(fonction=commande_graphiques)

    args = parser.parse_args()
    args.fonction(args)


if __name__ == "__main__":
    main()
