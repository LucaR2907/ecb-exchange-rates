# -*- coding: utf-8 -*-
"""Séance 4 - Parties A et B : Python idiomatique et utilisation des classes."""

from .serie import Resume, SerieTaux


def demo_idiomatique(serie):
    """A.1 à A.3 sur une série de taux."""
    print(f"=== A. Python idiomatique sur EUR/{serie.devise} ===")

    # A.1 - Séance 2 : une boucle avec append() remplissait la liste des variations.
    # Ici, la même liste en une compréhension :
    variations = serie.variations_quotidiennes()
    print("A.1 - 3 premières variations (%) :", [round(v, 3) for v in variations[:3]])
    # Compréhension de dictionnaire : date -> taux
    taux_par_date = {jour: valeur for jour, valeur in serie.lignes}
    premier_jour = serie.dates[0]
    print(f"A.1 - Dictionnaire : {premier_jour} -> {taux_par_date[premier_jour]}")

    # A.2 - enumerate (rang + valeur) et zip (associe dates et taux)
    print("A.2 - Les 3 premiers jours :")
    for rang, (jour, valeur) in enumerate(zip(serie.dates[:3], serie.taux[:3]), start=1):
        print(f"   {rang}. {jour} : {valeur}")
    plus_hauts = sorted(serie.lignes, key=lambda ligne: ligne[1], reverse=True)[:3]
    print("A.2 - Les 3 taux les plus hauts :",
          [(jour.isoformat(), valeur) for jour, valeur in plus_hauts])

    # A.3 - f-strings, lambda, map et filter
    print(f"A.3 - Le {premier_jour:%d/%m/%Y}, 1 EUR = {serie.taux[0]:.2f} {serie.devise}")
    en_centimes = list(map(lambda t: round(t * 100, 1), serie.taux[:3]))
    print("A.3 - map (x100) :", en_centimes)
    moyenne = serie.moyenne()
    au_dessus = list(filter(lambda t: t > moyenne, serie.taux))
    print(f"A.3 - filter : {len(au_dessus)} jours au-dessus de la moyenne ({moyenne:.3f})")


def demo_classes(series):
    """B.1 à B.3 : plusieurs objets de la même classe, attribut de classe, dataclass."""
    print("\n=== B. Programmation orientée objet ===")
    print("B.2 - Attribut de classe partagé : SerieTaux.base =", SerieTaux.base)
    for serie in series:
        print(f"B.1 - {serie} : moyenne {serie.moyenne():.4f}, "
              f"variation {serie.variation():+.2f} %, "
              f"taux au {serie.dates[-1]} = {serie.taux_a_date(serie.dates[-1])}")
    print("B.2 - Chaque objet a sa propre liste :", series[0].lignes is not series[1].lignes)

    resumes = [Resume(s.devise, len(s.lignes), round(s.moyenne(), 4), round(s.variation(), 2))
               for s in series]
    for resume in resumes:
        print("B.3 - Dataclass :", resume)


def analyser(series):
    demo_idiomatique(series[0])
    demo_classes(series)
