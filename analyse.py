# -*- coding: utf-8 -*-
"""
Séance 3 : pandas, jointures, numpy et aperçu de polars.
Données : les CSV de la séance 1 dans donnees/ (EUR/THB et EUR/USD).

Installer : pip install -r requirements.txt
Lancer    : python analyse.py
"""

import os
from time import perf_counter

import numpy as np
import pandas as pd

from fonctions import minimum_maximum, moyenne   # fonctions de la séance 2

DOSSIER = os.path.dirname(os.path.abspath(__file__))
DONNEES = os.path.join(DOSSIER, "donnees")


def charger(devise):
    """Charge le CSV d'une devise dans un DataFrame avec les colonnes date et taux."""
    chemin = os.path.join(DONNEES, "taux_EUR_" + devise + ".csv")
    df = pd.read_csv(chemin, parse_dates=["date"])
    return df.rename(columns={devise: "taux"})


def partie_a(df):
    """A.1 et A.2 : inspecter, sélectionner, filtrer, comparer avec la séance 2."""
    print("=== A.1 Inspection du DataFrame EUR/THB ===")
    print(df.head())
    print(df.describe())
    print(df.dtypes)

    print("\n=== A.2 Sélection et filtre ===")
    serie = df["taux"]                       # une colonne = une Series
    seuil = 38
    au_dessus = df[df["taux"] > seuil]       # filtre sur les lignes
    print(f"Jours où 1 EUR vaut plus de {seuil} THB : {len(au_dessus)}")
    print(au_dessus.head(3))

    mini_boucle, maxi_boucle = minimum_maximum(serie.tolist())
    print("Moyenne  pandas / séance 2 :", serie.mean(), "/", moyenne(serie.tolist()))
    print("Minimum  pandas / séance 2 :", serie.min(), "/", mini_boucle)
    print("Maximum  pandas / séance 2 :", serie.max(), "/", maxi_boucle)


def partie_b(df):
    """B.1 forward-fill sur un calendrier de jours ouvrés, B.2 analyses."""
    print("\n=== B.1 Combler les trous (forward-fill) ===")
    par_date = df.set_index("date")
    # freq="B" = business days : tous les jours du lundi au vendredi
    calendrier = pd.date_range(par_date.index.min(), par_date.index.max(), freq="B")
    complet = par_date.reindex(calendrier)
    manquants = complet["taux"].isna()
    print("Jours ouvrés sans publication :", manquants.sum())
    print("Dates concernées :", [d.date().isoformat() for d in complet.index[manquants]])
    complet = complet.ffill()                # recopie le dernier taux connu
    print("Valeurs encore manquantes après ffill :", complet["taux"].isna().sum())
    print("Nombre de jours ouvrés au total :", len(complet))

    print("\n=== B.2 Analyser ===")
    premier = complet["taux"].iloc[0]
    dernier = complet["taux"].iloc[-1]
    variation = (dernier / premier - 1) * 100
    print(f"Variation sur la période : {premier} -> {dernier} THB, soit {variation:+.2f} %")

    moyenne_mobile = complet["taux"].rolling(window=5).mean()   # 5 jours ouvrés = 1 semaine
    print("Moyenne mobile 5 jours (5 dernières valeurs) :")
    print(moyenne_mobile.tail())

    mensuel = complet["taux"].resample("MS").mean()             # MS = début de mois
    print("Moyennes mensuelles :")
    print(mensuel.round(3))
    return complet


def partie_c(df_thb, df_usd):
    """C.1 jointure des deux devises, C.2 types de jointure, C.3 merge/join/concat."""
    print("\n=== C.1 Réunir les deux devises ===")
    gauche = df_thb.rename(columns={"taux": "EUR_THB"})
    droite = df_usd.rename(columns={"taux": "EUR_USD"})
    print("Doublons de dates :", gauche["date"].duplicated().sum(), droite["date"].duplicated().sum())
    deux_devises = pd.merge(gauche, droite, on="date", how="inner").set_index("date")
    print("Lignes THB, USD, après jointure :", len(gauche), len(droite), len(deux_devises))
    print(deux_devises.head())

    print("\n=== C.2 Les quatre types de jointure ===")
    table_gauche = pd.DataFrame({"cle": [1, 2], "gauche": ["A", "B"]})
    table_droite = pd.DataFrame({"cle": [2, 3], "droite": ["X", "Y"]})
    for how in ["inner", "left", "right", "outer"]:
        print(f"--- how='{how}'")
        print(pd.merge(table_gauche, table_droite, on="cle", how=how))

    print("\n=== C.3 merge, join ou concat ===")
    avec_join = gauche.set_index("date").join(droite.set_index("date"))   # joint sur l'index
    print("join :", avec_join.shape)
    cote_a_cote = pd.concat([gauche.set_index("date"), droite.set_index("date")], axis=1)
    print("concat axis=1 (côte à côte, aligné sur l'index) :", cote_a_cote.shape)
    empile = pd.concat([table_gauche, table_droite], axis=0, ignore_index=True)
    print("concat axis=0 (empilé, sans apparier de clé) :")
    print(empile)
    return deux_devises


def partie_d(df):
    """D.1/D.2 numpy, D.3 aperçu de polars."""
    print("\n=== D.1 Calculs numpy ===")
    valeurs = df["taux"].to_numpy()
    print("Moyenne :", np.mean(valeurs))
    print("Écart-type :", np.std(valeurs))          # numpy divise par N (pandas par N - 1)
    variations = np.diff(valeurs) / valeurs[:-1] * 100
    print("3 premières variations jour à jour (%) :", variations[:3].round(3))

    print("\n=== D.2 dtype et broadcasting ===")
    print("dtype :", valeurs.dtype)
    print("taux * 100 (broadcasting) :", (valeurs * 100)[:3])

    print("\n=== D.3 Aperçu de polars ===")
    try:
        import polars as pl
    except ImportError:
        print("polars n'est pas installé : pip install polars")
        return

    chemin = os.path.join(DONNEES, "taux_EUR_THB.csv")
    df_pl = pl.read_csv(chemin, try_parse_dates=True).rename({"THB": "taux"})
    resultat = df_pl.select(
        pl.col("taux").mean().alias("moyenne"),
        ((pl.col("taux").last() / pl.col("taux").first() - 1) * 100).alias("variation_pct"),
    )
    print(resultat)
    mensuel = df_pl.sort("date").group_by_dynamic("date", every="1mo").agg(pl.col("taux").mean())
    print(mensuel)

    # Même calcul répété 500 fois avec les deux bibliothèques
    repetitions = 500
    debut = perf_counter()
    for _ in range(repetitions):
        df["taux"].mean()
        (df["taux"].iloc[-1] / df["taux"].iloc[0] - 1) * 100
    temps_pandas = perf_counter() - debut

    debut = perf_counter()
    for _ in range(repetitions):
        df_pl.select(
            pl.col("taux").mean(),
            ((pl.col("taux").last() / pl.col("taux").first() - 1) * 100).alias("variation"),
        )
    temps_polars = perf_counter() - debut
    print(f"Temps pour {repetitions} répétitions : pandas {temps_pandas:.4f} s ; polars {temps_polars:.4f} s")


def main():
    df_thb = charger("THB")
    df_usd = charger("USD")
    partie_a(df_thb)
    partie_b(df_thb)
    partie_c(df_thb, df_usd)
    partie_d(df_thb)


if __name__ == "__main__":
    main()
