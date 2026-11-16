# -*- coding: utf-8 -*-
"""Séance 4 - Partie C : graphiques matplotlib enregistrés en PNG."""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")   # crée les PNG sans ouvrir de fenêtre
import matplotlib.pyplot as plt

COULEURS = {"THB": "darkorange", "USD": "navy"}


def courbe(serie, dossier):
    """C.1 - Évolution d'une devise sur la période."""
    fig, ax = plt.subplots(figsize=(10, 4.5))
    ax.plot(serie.dates, serie.taux, color=COULEURS.get(serie.devise, "black"), linewidth=1.6)
    ax.set_title(f"Évolution du taux {serie.base}/{serie.devise}")
    ax.set_xlabel("Date")
    ax.set_ylabel(f"{serie.devise} pour 1 {serie.base}")
    ax.grid(alpha=0.3)
    fig.autofmt_xdate()
    chemin = Path(dossier) / f"courbe_EUR_{serie.devise}.png"
    fig.savefig(chemin, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return chemin


def comparaison_et_histogramme(series, dossier):
    """C.2 - Deux graphiques côte à côte : comparaison en base 100 et histogramme."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 4.8))

    # Les unités sont différentes (THB ~ 37, USD ~ 1,16) : on ramène chaque série à 100
    for serie in series:
        indice = [t / serie.taux[0] * 100 for t in serie.taux]
        ax1.plot(serie.dates, indice, label=f"EUR/{serie.devise}", color=COULEURS.get(serie.devise))
    ax1.axhline(100, color="grey", linewidth=0.8, linestyle="--")
    ax1.set_title("Comparaison des deux devises (base 100 au 31/12/2025)")
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Indice")
    ax1.legend()
    ax1.grid(alpha=0.3)

    ax2.hist([s.variations_quotidiennes() for s in series], bins=25,
             label=[f"EUR/{s.devise}" for s in series],
             color=[COULEURS.get(s.devise) for s in series], alpha=0.8)
    ax2.set_title("Distribution des variations quotidiennes")
    ax2.set_xlabel("Variation entre deux publications (%)")
    ax2.set_ylabel("Nombre de jours")
    ax2.legend()
    ax2.grid(alpha=0.3)

    ax1.tick_params(axis="x", labelrotation=30)   # on incline seulement les dates
    chemin = Path(dossier) / "comparaison_et_histogramme.png"
    fig.savefig(chemin, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return chemin


def tracer_tout(series, dossier):
    Path(dossier).mkdir(parents=True, exist_ok=True)
    chemins = [courbe(serie, dossier) for serie in series]
    chemins.append(comparaison_et_histogramme(series, dossier))
    return chemins
