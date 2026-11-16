# -*- coding: utf-8 -*-
"""Séance 4 - Partie B : la classe SerieTaux et une dataclass."""

import csv
from dataclasses import dataclass
from datetime import date
from pathlib import Path

DONNEES = Path(__file__).resolve().parent.parent / "donnees"


def lire_taux(devise, dossier=DONNEES):
    """Lit donnees/taux_EUR_<devise>.csv et renvoie une liste de couples (date, taux)."""
    chemin = Path(dossier) / f"taux_EUR_{devise}.csv"
    with chemin.open(encoding="utf-8") as fichier:
        return [(date.fromisoformat(ligne["date"]), float(ligne[devise]))
                for ligne in csv.DictReader(fichier)]


class SerieTaux:
    """B.1 - Les taux d'une devise (données) et les calculs sur ces taux (méthodes)."""

    base = "EUR"   # attribut de classe : commun à toutes les séries

    def __init__(self, devise, lignes):
        self.devise = devise                              # attribut d'instance
        self.lignes = sorted(lignes, key=lambda l: l[0])  # nouvelle liste, propre à l'objet
        if not self.lignes:
            raise ValueError("Une série de taux ne peut pas être vide.")

    def __repr__(self):
        return f"SerieTaux({self.base}/{self.devise}, {len(self.lignes)} taux)"

    @property
    def dates(self):
        return [jour for jour, _ in self.lignes]

    @property
    def taux(self):
        return [valeur for _, valeur in self.lignes]

    def moyenne(self):
        return sum(self.taux) / len(self.taux)

    def variation(self):
        """Variation entre le premier et le dernier taux, en %."""
        return (self.taux[-1] / self.taux[0] - 1) * 100

    def taux_a_date(self, jour):
        """Renvoie le taux publié ce jour-là, ou None s'il n'y en a pas."""
        return dict(self.lignes).get(jour)

    def variations_quotidiennes(self):
        """A.1 - Compréhension de liste : variation en % entre deux publications."""
        t = self.taux
        return [(t[i] / t[i - 1] - 1) * 100 for i in range(1, len(t))]


@dataclass
class Resume:
    """B.3 - Une dataclass : __init__ et __repr__ sont écrits automatiquement."""

    devise: str
    observations: int
    moyenne: float
    variation_pct: float


def charger_series(devises=("THB", "USD")):
    """B.2 - Une instance de SerieTaux par devise."""
    return [SerieTaux(devise, lire_taux(devise)) for devise in devises]
