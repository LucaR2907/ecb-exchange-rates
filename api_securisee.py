# -*- coding: utf-8 -*-
"""
Séance 2 - Partie B : l'appel à l'API de la séance 1, protégé par try/except
et journalisé avec logging (fichier logs/api.log).

Lancer avec : python api_securisee.py
Si l'appel échoue (pas de réseau, erreur HTTP comme le 403, réponse illisible),
le programme affiche un message clair, l'écrit dans le log et garde les données
déjà présentes dans donnees/.
"""

import json
import logging
import os
import urllib.request
from urllib.error import HTTPError, URLError

BASE = "EUR"
DEVISES = ["THB", "USD"]
DEBUT = "2026-01-01"
FIN = "2026-09-01"
API = "https://api.frankfurter.app"

DOSSIER = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(DOSSIER, "cache")
DONNEES = os.path.join(DOSSIER, "donnees")
LOGS = os.path.join(DOSSIER, "logs")

logger = logging.getLogger("api")


def configurer_logs():
    """Envoie les messages de niveau INFO et plus dans logs/api.log."""
    os.makedirs(LOGS, exist_ok=True)
    logging.basicConfig(
        filename=os.path.join(LOGS, "api.log"),
        encoding="utf-8",
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )


def appeler_api(url):
    """Appelle l'URL et renvoie (texte_brut, dictionnaire), ou None en cas d'erreur."""
    logger.info("Appel de %s", url)
    # Sans User-Agent, l'API répond 403 aux requêtes "Python-urllib"
    requete = urllib.request.Request(url, headers={"User-Agent": "projet-python-groupe-X"})
    try:
        with urllib.request.urlopen(requete, timeout=10) as reponse:
            brut = reponse.read().decode("utf-8")
        donnees = json.loads(brut)
    except HTTPError as erreur:
        # HTTPError est un cas particulier de URLError : on la traite en premier
        logger.error("Erreur HTTP %s pour %s", erreur.code, url)
        print("Erreur : l'API a répondu avec le code HTTP", erreur.code)
        return None
    except URLError as erreur:
        logger.error("Erreur réseau : %s", erreur.reason)
        print("Erreur : connexion impossible (vérifier internet).")
        return None
    except TimeoutError:
        logger.error("Délai dépassé pour %s", url)
        print("Erreur : l'API met trop de temps à répondre.")
        return None
    except json.JSONDecodeError:
        logger.error("Réponse illisible (pas du JSON) pour %s", url)
        print("Erreur : la réponse de l'API n'est pas du JSON valide.")
        return None
    else:
        # else : exécuté seulement si aucune exception n'a eu lieu
        logger.info("Réponse reçue et décodée")
        return brut, donnees


def recuperer_serie(devise):
    """Télécharge la série d'une devise, l'enregistre dans cache/ et donnees/.
    Renvoie True si tout s'est bien passé, False sinon."""
    url = API + "/" + DEBUT + ".." + FIN + "?from=" + BASE + "&to=" + devise
    resultat = appeler_api(url)
    if resultat is None:
        logger.warning("Série %s non mise à jour, on garde les données locales", devise)
        return False

    brut, donnees = resultat
    rates = donnees.get("rates", {})
    if len(rates) == 0:
        logger.warning("Réponse vide pour %s : rien n'est enregistré", devise)
        return False

    os.makedirs(CACHE, exist_ok=True)
    os.makedirs(DONNEES, exist_ok=True)
    nom_cache = "serie_" + BASE + "_" + devise + "_" + DEBUT + "_" + FIN + ".json"
    with open(os.path.join(CACHE, nom_cache), "w", encoding="utf-8") as fichier:
        fichier.write(brut)

    with open(os.path.join(DONNEES, "taux_EUR_" + devise + ".csv"), "w", encoding="utf-8") as fichier:
        fichier.write("date," + devise + "\n")
        for date in sorted(rates):
            fichier.write(date + "," + str(rates[date][devise]) + "\n")

    logger.info("Série %s enregistrée : %d dates", devise, len(rates))
    return True


def main():
    configurer_logs()
    for devise in DEVISES:
        if recuperer_serie(devise):
            print("EUR/" + devise + " : série mise à jour.")
        else:
            print("EUR/" + devise + " : échec, les données locales sont conservées.")
    print("Détails dans logs/api.log")


if __name__ == "__main__":
    main()
