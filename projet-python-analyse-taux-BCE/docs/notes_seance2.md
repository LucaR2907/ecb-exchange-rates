# Notes — Séance 2

Fichiers : `fonctions.py` (partie A), `api_securisee.py` (partie B), `recursivite.py` (partie C).
Les calculs portent sur les CSV de la séance 1 : `donnees/taux_EUR_THB.csv` et `donnees/taux_EUR_USD.csv` (171 jours ouvrés, du 31/12/2025 au 01/09/2026).

## Partie A — Les fonctions

### Résultats (`python fonctions.py`)

| Série | Nb de taux | Moyenne (notre fonction) | Moyenne (`statistics.mean`) | Min | Max |
|---|---:|---:|---:|---:|---:|
| EUR/THB | 171 | 37.652070175438595 | 37.652070175438595 | 36.353 | 38.570 |
| EUR/USD | 171 | 1.1623684210526313 | 1.1623684210526315 | 1.1340 | 1.1974 |

Les deux moyennes sont identiques à 2·10⁻¹⁶ près pour l'USD : `statistics.mean` calcule de façon plus précise que notre simple somme, et les nombres décimaux en machine (flottants) ont de petites erreurs d'arrondi. Pour comparer deux flottants, il vaut mieux utiliser `math.isclose` plutôt que `==`.

**1. Pourquoi découper le code en fonctions ? Trois bénéfices concrets.**

On réutilise un traitement sans le recopier (ici `moyenne` sert pour le THB et pour l'USD) ; on peut tester chaque morceau séparément ; le programme est plus lisible et plus facile à corriger (on peut changer la lecture du CSV sans toucher au calcul de la moyenne).

**2. Quelle différence entre un paramètre et la valeur de retour ? Que renvoie une fonction sans `return` ?**

Un paramètre est une donnée que la fonction reçoit en entrée : dans `moyenne(taux)`, `taux` est le paramètre. La valeur de retour est le résultat que la fonction renvoie à celui qui l'a appelée avec `return`. Une fonction sans `return` renvoie `None`. Attention : afficher une valeur avec `print` n'est pas la renvoyer.

**3. Qu'est-ce qu'une docstring et où la place-t-on ?**

C'est une chaîne entre triples guillemets qui décrit ce que fait la fonction. On la place juste en dessous de la ligne `def`. On peut l'afficher avec `help(moyenne)`.

**4. Variable locale ou globale ?**

Une variable locale est créée dans une fonction et n'existe que pendant l'appel : `total` dans `moyenne` n'est pas accessible en dehors. Une variable globale est définie au niveau du fichier (comme `DONNEES`) et peut être lue partout. Pour la modifier depuis une fonction, il faudrait le mot-clé `global`, ce qu'on évite : on préfère passer les données en paramètres.

## Partie B — Gérer les erreurs et journaliser

`api_securisee.py` reprend l'appel de la séance 1 dans un `try/except` qui distingue : erreur HTTP (comme le 403 rencontré), absence de connexion, délai dépassé et réponse qui n'est pas du JSON. Dans chaque cas, un message clair s'affiche et les données locales sont conservées. Le suivi est écrit dans `logs/api.log` : `INFO` pour le déroulement normal, `WARNING` quand une série n'est pas mise à jour ou que la réponse est vide, `ERROR` pour une erreur.

Exemple réel de log (lancé sur un réseau qui bloque l'API) :

```
INFO Appel de https://api.frankfurter.app/2026-01-01..2026-09-01?from=EUR&to=THB
ERROR Erreur réseau : Tunnel connection failed: 403 Forbidden
WARNING Série THB non mise à jour, on garde les données locales
```

**1. Pourquoi gérer les erreurs avec `try/except` ? Que se passe-t-il si une exception n'est pas gérée ? À quoi servent `else` et `finally` ?**

Un programme qui dépend du réseau peut échouer pour des raisons extérieures. `try` contient le code risqué, `except` traite l'erreur prévue et permet d'afficher un message compréhensible au lieu d'un plantage. Une exception non gérée remonte jusqu'en haut du programme, l'arrête et affiche une trace d'erreur (traceback). `else` s'exécute seulement si aucune exception n'a eu lieu dans le `try` (ici : on écrit « Réponse reçue » dans le log). `finally` s'exécute dans tous les cas, erreur ou non, et sert au nettoyage (fermer un fichier, une connexion).

**2. Pourquoi un `except:` nu est-il déconseillé ?**

Il attrape toutes les erreurs, y compris celles qu'on n'attendait pas (une faute de frappe dans le code) et même l'interruption Ctrl+C. Le bug est alors caché et difficile à trouver. Il vaut mieux préciser le type d'erreur attendu, comme `HTTPError` ou `URLError`. Comme `HTTPError` est un cas particulier de `URLError`, on la traite en premier.

**3. C'est quoi `logging` ? Pourquoi le préférer à `print` ? Les niveaux et un usage de chacun.**

`logging` est le module standard pour enregistrer ce qui se passe pendant l'exécution, avec la date, l'heure et un niveau de gravité. Contrairement à `print`, on peut écrire dans un fichier, garder un historique et filtrer selon l'importance.

| Niveau | Exemple d'usage |
|---|---|
| DEBUG | détail pour chercher un bug (valeur d'une variable intermédiaire) |
| INFO | déroulement normal : début d'un appel, série enregistrée |
| WARNING | cas suspect mais pas bloquant : réponse vide, données non mises à jour |
| ERROR | une opération a échoué : erreur HTTP, pas de connexion |
| CRITICAL | erreur grave qui empêche le programme entier de fonctionner |

Le seuil choisi est `INFO`, donc les messages `DEBUG` ne sont pas enregistrés.

## Partie C — Récursivité et complexité

### Tableau des mesures (`python recursivite.py`)

Temps : médiane de 5 appels mesurés avec `time.perf_counter`, cache de la version mémoïsée vidé avant chaque appel. Mémoire : pic suivi par `tracemalloc` pendant un appel. Python 3.13, Linux.

| n | Version | F(n) | Temps médian (ms) | Pic mémoire (octets) |
|---|---|---|---|---|
| 10 | fibonacci_naif | 55 | 0.0057 | 0 |
| 10 | fibonacci_memo | 55 | 0.0015 | 856 |
| 10 | fibonacci_iteratif | 55 | 0.0003 | 88 |
| 20 | fibonacci_naif | 6765 | 0.7382 | 160 |
| 20 | fibonacci_memo | 6765 | 0.0033 | 856 |
| 20 | fibonacci_iteratif | 6765 | 0.0007 | 136 |
| 25 | fibonacci_naif | 75025 | 7.9235 | 224 |
| 25 | fibonacci_memo | 75025 | 0.0034 | 1928 |
| 25 | fibonacci_iteratif | 75025 | 0.0007 | 136 |
| 30 | fibonacci_naif | 832040 | 92.1647 | 320 |
| 30 | fibonacci_memo | 832040 | 0.0037 | 1928 |
| 30 | fibonacci_iteratif | 832040 | 0.0007 | 136 |

**Lecture.** Le temps du naïf est multiplié par environ 11 à chaque fois que n augmente de 5 (0,74 → 7,9 → 92 ms) : c'est la croissance exponentielle. La version mémoïsée et la version itérative restent sous la centième de milliseconde. En mémoire, la mémoïsation utilise le plus (le cache garde toutes les valeurs F(0) à F(n)), l'itérative le moins (deux variables). Les chiffres exacts dépendent de la machine ; `tracemalloc` ne suit que les allocations Python, pas la pile d'appels, d'où le 0 pour le naïf à n = 10.

En dépassant la limite de récursion (1000 par défaut), `factorielle(1100)` lève bien une `RecursionError`, interceptée par le programme.

**1. C'est quoi la récursivité ? Cas de base et cas récursif ? Que se passe-t-il sans cas de base ?**

Une fonction récursive s'appelle elle-même sur un problème plus petit. Le cas de base arrête la récursion : pour `factorielle`, `n == 0` renvoie 1. Le cas récursif est l'appel à soi-même : `n * factorielle(n - 1)`. Sans cas de base, les appels ne s'arrêtent jamais et Python finit par lever une `RecursionError`.

**2. Pourquoi utiliser la récursivité ? Est-ce toujours le meilleur choix ? Contre-exemple.**

Elle exprime naturellement les problèmes qui se décomposent en sous-problèmes identiques (factorielle, parcours d'un arbre de dossiers). Ce n'est pas toujours le meilleur choix : Fibonacci naïf recalcule énormément de fois les mêmes valeurs (pour F(5), F(3) est calculé 2 fois, F(2) 3 fois...). Le tableau montre 92 ms pour n = 30 contre 0,0007 ms pour la boucle, qui donne le même résultat.

**3. C'est quoi la complexité temporelle ? Spatiale ? Que signifient O(n), O(n²), O(2ⁿ) ?**

La complexité temporelle mesure comment le nombre d'opérations augmente avec la taille n de l'entrée ; la complexité spatiale, comment augmente la mémoire supplémentaire utilisée. O(n) : le travail est proportionnel à n (une boucle simple, comme Fibonacci itératif). O(n²) : deux boucles imbriquées de n tours. O(2ⁿ) : le travail double environ à chaque fois que n augmente de 1 (Fibonacci naïf).

| Version | Temps | Mémoire |
|---|---|---|
| Fibonacci naïf | O(2ⁿ) | O(n) : profondeur de la pile d'appels |
| Fibonacci mémoïsé | O(n) | O(n) : le cache + la pile d'appels |
| Fibonacci itératif | O(n) | O(1) : deux variables |

**4. C'est quoi la mémoïsation ? Que fait `functools.lru_cache` ? Pourquoi Python limite-t-il la profondeur de récursion ?**

La mémoïsation consiste à garder en mémoire le résultat d'un calcul déjà fait pour ne pas le refaire. `@lru_cache(maxsize=None)` fait cela automatiquement : il associe chaque argument à son résultat ; si on rappelle la fonction avec le même argument, le résultat est lu dans le cache. Python limite la profondeur de récursion (1000 par défaut, voir `sys.getrecursionlimit()`) car chaque appel occupe de la place dans la pile ; sans limite, une récursion trop profonde ferait planter l'interpréteur.
