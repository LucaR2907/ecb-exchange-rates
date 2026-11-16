# Notes — Séance 3

Fichier : `analyse.py` (`python analyse.py`). Données : les CSV de la séance 1 (`donnees/taux_EUR_THB.csv` et `donnees/taux_EUR_USD.csv`), 171 jours ouvrés du 31/12/2025 au 01/09/2026. Un taux = nombre de THB (ou d'USD) pour 1 EUR.

## Comparatif avec la séance 2

| EUR/THB | Fonctions séance 2 (boucles) | pandas |
|---|---:|---:|
| Moyenne | 37.652070175438595 | 37.652070175438595 |
| Minimum | 36.353 | 36.353 |
| Maximum | 38.570 | 38.570 |

Les résultats sont identiques. La différence est dans l'écriture : en séance 2, il fallait une fonction avec une boucle pour chaque statistique (`moyenne`, `minimum_maximum`) ; avec pandas, `serie.mean()`, `serie.min()`, `serie.max()` ou `df.describe()` font le travail en une ligne. `analyse.py` importe directement les fonctions de `fonctions.py` pour faire la comparaison.

## Partie A — Découvrir pandas

À 38 THB pour 1 EUR, le filtre `df[df["taux"] > 38]` garde 54 jours sur 171, tous à partir de fin avril 2026.

**1. Qu'est-ce qu'un DataFrame ? Une Series ?**

Un DataFrame est un tableau à deux dimensions avec des lignes et des colonnes nommées, comme une feuille Excel. Une Series est une seule colonne de valeurs avec un index. Ici `df` est un DataFrame (colonnes `date` et `taux`) et `df["taux"]` est une Series.

**2. Pourquoi pandas plutôt que des boucles et le module csv ? Que signifie « vectorisation » ?**

pandas charge un CSV, filtre, calcule et regroupe en quelques lignes lisibles, et gère directement les dates et les valeurs manquantes. La vectorisation consiste à appliquer une opération à une colonne entière d'un coup (`serie * 100`, `serie.mean()`) au lieu de parcourir les valeurs une par une avec une boucle Python. Ces opérations s'exécutent dans du code compilé, donc beaucoup plus vite.

**3. Pourquoi déconseille-t-on `iterrows()` ?**

`iterrows()` crée un objet Series pour chaque ligne et repasse par une boucle Python : c'est lent, et cela peut changer le type des valeurs (un entier peut devenir un décimal dans la ligne). On préfère les opérations sur des colonnes entières ; si une boucle est vraiment nécessaire, `itertuples()` est plus rapide.

**4. Comment pandas représente-t-il les valeurs manquantes ? Conséquences sur les moyennes ?**

Par `NaN` (« Not a Number ») pour les nombres, et `NaT` pour les dates. Par défaut, `mean()` ignore les `NaN` : la moyenne est calculée seulement sur les valeurs présentes. Il faut donc vérifier combien de valeurs manquent (`isna().sum()`), sinon une moyenne peut porter sur moins de jours que prévu sans qu'on s'en rende compte.

## Partie B — Nettoyer, consolider et analyser

**Choix du forward-fill (B.1).** En réindexant sur un calendrier continu de jours ouvrés (`freq="B"`, lundi au vendredi), 4 jours apparaissent sans taux : le 1er janvier, le 3 et le 6 avril (Vendredi saint et lundi de Pâques) et le 1er mai 2026, jours fériés où la BCE ne publie pas. On recopie pour ces jours le dernier taux publié : c'est le taux de référence qui reste en vigueur tant qu'aucun nouveau n'est publié, et on n'invente pas d'évolution entre deux publications. On passe de 171 à 175 jours ouvrés.

**Résultats (B.2) sur EUR/THB :**

- variation sur la période : 37,218 → 38,554 THB, soit **+3,59 %** (l'euro s'est apprécié face au baht) ;
- moyenne mobile sur 5 jours ouvrés (une semaine) : 38,37 au 1er septembre ;
- moyennes mensuelles : de 36,76 en janvier à 38,27 en août, avec une hausse presque continue.

| Mois | Moyenne EUR/THB |
|---|---:|
| janvier 2026 | 36.757 |
| février | 36.960 |
| mars | 37.298 |
| avril | 37.782 |
| mai | 37.957 |
| juin | 37.874 |
| juillet | 38.259 |
| août | 38.270 |

(Décembre 2025 et septembre 2026 ne contiennent qu'un seul jour chacun.)

**1. C'est quoi le forward-fill ? Quelle hypothèse fait-on ?**

Le forward-fill (`ffill()`) remplace chaque valeur manquante par la dernière valeur connue avant elle. On suppose que la valeur n'a pas changé tant qu'aucune nouvelle observation n'a été publiée. C'est raisonnable pour un taux de référence un jour férié, mais ce n'est pas un vrai taux observé.

**2. À quoi sert `resample` ? Que signifie une moyenne mobile ?**

`resample` change la fréquence d'une série indexée par des dates : `resample("MS").mean()` regroupe les taux par mois et calcule la moyenne de chaque mois. Une moyenne mobile calcule la moyenne sur une fenêtre qui glisse dans le temps : `rolling(5).mean()` donne pour chaque jour la moyenne des 5 derniers jours ouvrés, ce qui lisse les variations quotidiennes. Les 4 premiers jours donnent `NaN` car la fenêtre n'est pas encore pleine.

## Partie C — Les jointures

`pd.merge(thb, usd, on="date", how="inner")` donne 171 lignes : les deux séries ont exactement les mêmes dates et aucune date en double, la jointure est complète. Sur les petites tables de C.2 (clés {1, 2} et {2, 3}), on retrouve bien : inner → {2}, left → {1, 2}, right → {2, 3}, outer → {1, 2, 3}, avec des `NaN` là où il manque une correspondance.

**1. Les quatre types de jointure : que garde chacune ?**

`inner` garde seulement les clés présentes dans les deux tables ; `left` garde toutes les lignes de gauche ; `right` toutes celles de droite ; `outer` toutes les clés des deux tables. Les colonnes sans correspondance prennent la valeur `NaN`.

**2. Sur quelle colonne joint-on ? Que devient une ligne sans correspondance ?**

Sur la clé commune, ici la colonne `date`. Une ligne sans correspondance disparaît avec `inner` ; avec `left`, `right` ou `outer`, elle est gardée si son côté est conservé, avec `NaN` dans les colonnes de l'autre table. Si une clé est en double, toutes les combinaisons sont créées : il faut vérifier le nombre de lignes après un `merge`.

**3. Pour réunir deux séries de taux sur la même période, quelle jointure ?**

`inner` : les deux séries BCE ont les mêmes dates de publication, donc on ne perd aucune ligne et chaque date a ses deux taux. Si les dates différaient, `outer` permettrait de repérer les dates manquantes d'un côté ou de l'autre.

**4. Différence entre `merge` et `concat` ?**

`merge` associe les lignes de deux tables selon une clé (comme `RECHERCHEV` dans Excel). `concat` colle des tables sans chercher de clé : les unes sous les autres (`axis=0`, pour ajouter des lignes de même structure) ou côte à côte (`axis=1`, en alignant les index). `join` est un `merge` qui se fait sur l'index. On utilise `merge` pour réunir les deux devises par date, `concat` pour empiler deux tableaux de même forme.

## Partie D — numpy et polars

Avec numpy : moyenne 37,652, écart-type 0,597 (numpy divise par N, alors que `describe()` de pandas divise par N − 1 et donne 0,599), et variations jour à jour calculées sans boucle avec `np.diff`.

**1. Liste Python ou tableau numpy ? dtype ? broadcasting ?**

Une liste peut contenir des objets de types différents, stockés un par un. Un tableau numpy (`ndarray`) contient des éléments d'un seul type, rangés côte à côte en mémoire, ce qui permet des calculs rapides. Le `dtype` est ce type commun, ici `float64`. Le broadcasting permet d'opérer entre un tableau et un nombre (ou deux tableaux de formes compatibles) : `valeurs * 100` multiplie chaque taux par 100 sans boucle.

**2. Pourquoi numpy est-il plus rapide que des boucles Python ?**

Les boucles de numpy sont écrites en C et compilées, et travaillent sur des données de même type rangées de façon continue en mémoire. Une boucle Python doit, à chaque tour, interpréter l'instruction et vérifier le type de chaque élément, ce qui est bien plus lent.

**3. pandas ou polars ?**

pandas est écrit en Python (avec du C via numpy), exécute chaque opération immédiatement et travaille surtout sur un seul cœur du processeur. polars est écrit en Rust, utilise plusieurs cœurs en parallèle, et propose une évaluation paresseuse (`lazy()`) : il prépare toute la chaîne d'opérations, l'optimise, puis l'exécute d'un coup avec `collect()`. pandas convient aux petits et moyens jeux de données et dispose d'un énorme écosystème ; polars devient intéressant pour de gros fichiers ou des traitements longs. Sur nos 171 lignes, les deux donnent la même moyenne et la même variation, et la mesure de temps affichée par `analyse.py` ne permet pas de conclure en général : le jeu de données est trop petit.
