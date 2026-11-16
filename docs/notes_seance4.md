# Notes — Séance 4

Fichiers : `src/idiomatique.py` (partie A), `src/serie.py` (partie B), `src/graphiques.py` (partie C), `main.py`, `README.md`, `requirements.txt`, `.gitignore` et `rapport_final.md` (partie D).

## Partie A — Python plus idiomatique

En séance 2, on aurait calculé les variations quotidiennes avec une boucle et `append()`. Dans `SerieTaux.variations_quotidiennes()`, la même liste tient en une compréhension :

```python
[(t[i] / t[i - 1] - 1) * 100 for i in range(1, len(t))]
```

**1. C'est quoi une compréhension de liste ? Quel avantage par rapport à une boucle `for` ?**

C'est une façon de construire une liste en une seule expression, par exemple `[x * 2 for x in nombres]`, éventuellement avec une condition (`[x for x in taux if x > 38]`). C'est plus court, on voit directement quelle liste on obtient, et c'est généralement un peu plus rapide. Une boucle classique reste préférable si le traitement est long ou compliqué. Il existe aussi des compréhensions de dictionnaire : `{jour: valeur for jour, valeur in lignes}`.

**2. À quoi servent `enumerate` et `zip` ?**

`enumerate(liste, start=1)` donne à chaque tour le rang et la valeur, sans gérer un compteur à la main. `zip(dates, taux)` parcourt deux listes en même temps et associe les éléments de même position. `zip` s'arrête à la liste la plus courte, il faut donc vérifier que les listes ont la même longueur.

**3. Comment trier une liste selon un critère ?**

Avec `sorted(liste, key=...)` : `key` est une fonction qui donne, pour chaque élément, la valeur à comparer. `sorted(lignes, key=lambda ligne: ligne[1], reverse=True)` trie les couples (date, taux) du taux le plus haut au plus bas. `sorted` renvoie une nouvelle liste et ne modifie pas l'originale (contrairement à `liste.sort()`).

**4. C'est quoi une f-string ? Comment afficher un nombre à deux décimales ?**

C'est une chaîne précédée de `f` dans laquelle on insère des valeurs entre accolades : `f"1 EUR = {taux} THB"`. Pour deux décimales : `f"{taux:.2f}"`. Cela arrondit seulement l'affichage, pas la valeur stockée. On peut aussi formater une date : `f"{jour:%d/%m/%Y}"`.

**5. C'est quoi une fonction `lambda` ?**

Une petite fonction sans nom, écrite en une expression : `lambda x: x * 2`. Elle sert pour un critère court passé à `sorted`, `map` ou `filter`. Exemple dans le projet : `filter(lambda t: t > moyenne, serie.taux)` garde les taux au-dessus de la moyenne (111 jours sur 171 pour le THB). Pour un traitement plus long, on écrit une fonction avec `def`.

## Partie B — La programmation orientée objet

`SerieTaux` regroupe les données (la devise et ses couples date/taux) et les méthodes `moyenne()`, `variation()`, `taux_a_date()` et `variations_quotidiennes()`. `charger_series()` crée deux instances : une pour THB, une pour USD.

**1. C'est quoi une classe ? Un objet ? Une instance ? À quoi sert `self` ?**

Une classe est un modèle qui décrit des données (attributs) et des actions (méthodes). Un objet est un élément créé à partir de ce modèle ; on dit que c'est une instance de la classe. Ici, la série THB et la série USD sont deux instances de `SerieTaux`. Dans une méthode, `self` désigne l'objet sur lequel on appelle la méthode : dans `serie_thb.moyenne()`, `self` est `serie_thb`.

**2. À quoi sert `__init__` ?**

C'est la méthode appelée automatiquement à la création d'un objet, par exemple `SerieTaux("THB", lignes)`. Elle initialise ses attributs : `self.devise` et `self.lignes`. Elle ne renvoie rien.

**3. Différence entre un attribut de classe et un attribut d'instance ?**

Un attribut de classe est défini dans la classe, hors de toute méthode, et partagé par toutes les instances : `base = "EUR"`. Un attribut d'instance est défini dans `__init__` avec `self.` et propre à chaque objet : `self.devise` vaut `"THB"` pour l'un et `"USD"` pour l'autre. Piège : une liste en attribut de classe serait partagée par tous les objets (comme le sous-dictionnaire `rates` partagé après `.copy()` en séance 1). C'est pourquoi chaque série reçoit sa propre liste dans `__init__` ; le programme vérifie que `usd.lignes is not thb.lignes`.

**4. Qu'apporte une `dataclass` ?**

Avec `@dataclass`, il suffit de déclarer les champs et leur type ; Python écrit automatiquement `__init__`, `__repr__` (un affichage lisible) et `__eq__` (comparaison par valeur). C'est idéal pour une classe qui sert surtout à stocker des données, comme `Resume(devise, observations, moyenne, variation_pct)`. Une classe écrite à la main reste utile quand on veut contrôler l'initialisation ou ajouter beaucoup de méthodes, comme `SerieTaux`.

## Partie C — Visualiser avec matplotlib

Graphiques produits par `python main.py graphiques` dans `figures/` : une courbe par devise (C.1), puis une figure à deux graphiques côte à côte (C.2) : la comparaison des deux devises en base 100 et l'histogramme des variations quotidiennes.

**1. Différence entre la figure et les axes ? Pourquoi `fig, ax = plt.subplots()` ?**

La figure (`fig`) est la feuille entière qu'on enregistre ; les axes (`ax`) sont une zone de graphique à l'intérieur, avec ses courbes, son titre et ses étiquettes. Une figure peut contenir plusieurs axes. Avec `fig, ax = plt.subplots()`, on garde une référence explicite à chaque graphique et on sait toujours lequel on modifie, ce qui est indispensable avec plusieurs graphiques côte à côte. L'usage direct de `plt.plot()` agit sur le graphique « courant », ce qui devient vite ambigu.

**2. Quel type de graphique pour quel type de donnée ?**

Une série temporelle se représente par une courbe (date → taux). Une distribution par un histogramme (combien de jours ont eu telle variation). Une comparaison de séries par plusieurs courbes sur les mêmes axes ; comme le THB (~37) et l'USD (~1,16) n'ont pas la même unité, on les ramène à un indice 100 au premier jour pour comparer leurs évolutions. Pour comparer des catégories, on utiliserait un diagramme en barres.

**3. Comment sauvegarder une figure en PNG ?**

`fig.savefig("figures/courbe_EUR_THB.png", dpi=150, bbox_inches="tight")` : `dpi` règle la résolution et `bbox_inches="tight"` évite de couper les titres. On ferme ensuite la figure avec `plt.close(fig)` pour libérer la mémoire.

## Partie D — Assembler et finaliser

**1. À quoi sert `argparse` ? Pourquoi une ligne de commande plutôt que des `input()` ?**

`argparse` lit les arguments donnés au lancement (`python main.py analyser --devise USD`), vérifie qu'ils sont valides et génère automatiquement l'aide (`--help`). Avec une ligne de commande, on relance exactement le même traitement sans répondre à des questions : c'est reproductible, automatisable dans un script, et plus rapide qu'une suite de `input()`.

**2. Que fait exactement `if __name__ == "__main__"` ?**

Quand on lance un fichier directement (`python fonctions.py`), Python donne à la variable `__name__` la valeur `"__main__"`, et le bloc s'exécute. Quand le fichier est importé par un autre (`analyse.py` fait `from fonctions import moyenne`), `__name__` vaut `"fonctions"` et le bloc ne s'exécute pas : on récupère les fonctions sans lancer tout le programme.

**3. C'est quoi un module ? Un package ?**

Un module est un fichier `.py` qu'on peut importer (`fonctions.py`). Un package est un dossier qui regroupe plusieurs modules, avec un fichier `__init__.py` : ici `src/` contient `serie.py`, `idiomatique.py` et `graphiques.py`, et `main.py` les importe avec `from src.serie import charger_series`.

**4. Que doit contenir un bon README ? À quoi servent `requirements.txt` et `.gitignore` ?**

Un README présente le projet et les auteurs, explique l'installation, donne des exemples de commandes, décrit les données, l'organisation des fichiers et les principaux résultats. `requirements.txt` liste les bibliothèques externes et leurs versions, pour réinstaller le même environnement avec `pip install -r requirements.txt`. `.gitignore` indique à Git les fichiers à ne pas suivre (`__pycache__/`, `.venv/`, `logs/`) ; il n'a pas d'effet sur les fichiers déjà commités, qu'il faut retirer avec `git rm --cached`.
