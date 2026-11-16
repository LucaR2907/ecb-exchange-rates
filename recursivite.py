# -*- coding: utf-8 -*-
"""
Séance 2 - Partie C : récursivité et complexité.
Lancer avec : python recursivite.py
Affiche le tableau des mesures (temps et mémoire) recopié dans docs/notes_seance2.md.
"""

import sys
import tracemalloc
from functools import lru_cache
from statistics import median
from time import perf_counter


# --- C.1 Fonctions récursives simples ---------------------------------------

def factorielle(n):
    """Calcule n! de façon récursive."""
    if n == 0:                       # cas de base : 0! = 1
        return 1
    return n * factorielle(n - 1)    # cas récursif


def somme_liste(liste):
    """Calcule la somme des éléments d'une liste de façon récursive."""
    if len(liste) == 0:              # cas de base : liste vide
        return 0
    return liste[0] + somme_liste(liste[1:])   # premier élément + somme du reste


# --- C.2 Trois versions de Fibonacci ----------------------------------------

def fibonacci_naif(n):
    """Fibonacci récursif naïf : recalcule plusieurs fois les mêmes valeurs."""
    if n < 2:
        return n
    return fibonacci_naif(n - 1) + fibonacci_naif(n - 2)


@lru_cache(maxsize=None)
def fibonacci_memo(n):
    """Fibonacci récursif avec mémoïsation : chaque F(k) n'est calculé qu'une fois."""
    if n < 2:
        return n
    return fibonacci_memo(n - 1) + fibonacci_memo(n - 2)


def fibonacci_iteratif(n):
    """Fibonacci avec une boucle : on garde seulement les deux derniers termes."""
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


# --- C.3 Mesures ---------------------------------------------------------------

def mesurer_temps(fonction, n, repetitions=5):
    """Renvoie le temps médian (en ms) de plusieurs appels, cache vidé avant chacun."""
    temps = []
    for _ in range(repetitions):
        fibonacci_memo.cache_clear()     # pour mesurer un vrai premier calcul
        debut = perf_counter()
        fonction(n)
        temps.append((perf_counter() - debut) * 1000)
    return median(temps)


def mesurer_memoire(fonction, n):
    """Renvoie le pic de mémoire (en octets) suivi par tracemalloc pendant un appel."""
    fibonacci_memo.cache_clear()
    tracemalloc.start()
    fonction(n)
    _, pic = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return pic


def main():
    print("factorielle(5) =", factorielle(5))
    print("somme_liste([1.1, 2.2, 3.3]) =", round(somme_liste([1.1, 2.2, 3.3]), 2))
    print()

    print("| n | Version | F(n) | Temps médian (ms) | Pic mémoire (octets) |")
    print("|---|---|---|---|---|")
    for n in [10, 20, 25, 30]:
        for fonction in [fibonacci_naif, fibonacci_memo, fibonacci_iteratif]:
            fibonacci_memo.cache_clear()
            resultat = fonction(n)
            temps = mesurer_temps(fonction, n)
            memoire = mesurer_memoire(fonction, n)
            print(f"| {n} | {fonction.__name__} | {resultat} | {temps:.4f} | {memoire} |")
    print()

    # RecursionError : on dépasse volontairement la profondeur maximale
    limite = sys.getrecursionlimit()
    print("Limite de récursion :", limite)
    try:
        factorielle(limite + 100)
    except RecursionError:
        print("RecursionError : profondeur de récursion maximale dépassée.")


if __name__ == "__main__":
    main()
