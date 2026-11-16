# Notes — Séance 1

Groupe X : Luca Radu, Victor Mavre-Gigot, Théophile Le Metter, Léopold Santamaria.
Devises du groupe : THB (baht thaïlandais) et USD (dollar américain), en base EUR.

## Partie A — Premiers pas en Python

### A.1 / A.2 — Installer Python, premier programme

**1. C'est quoi Python ? À quoi sert ce langage ? Est-il compilé ou interprété ?**

Python est un langage de programmation généraliste, simple à lire et à écrire. Il sert au développement web, à l'analyse de données, à l'automatisation de tâches, à l'intelligence artificielle, etc. C'est un langage interprété : le code est exécuté par un interpréteur, sans étape préalable de compilation en un exécutable comme en C. (Techniquement, Python traduit d'abord le code en *bytecode*, les fichiers `.pyc`, puis l'interpréteur exécute ce bytecode.)

**2. Comment installe-t-on Python ? Comment vérifie-t-on qu'il est bien installé et quelle version on utilise ?**

On télécharge l'installeur officiel sur python.org puis on suit l'assistant (sous Windows, cocher « Add Python to PATH »). Pour vérifier l'installation et connaître la version, on tape dans un terminal `python --version` ou `python3 --version`. Le projet demande Python 3.11 ou plus récent.

**3. Citez les différentes façons de lancer du code Python et un cas d'usage de chacune.**

- Le terminal interactif (REPL, en tapant `python`) : pour tester rapidement une instruction.
- Un script exécuté depuis le terminal (`python hello_world.py`) : pour un programme complet et réutilisable.
- Un notebook Jupyter : cellules exécutées une à une, utile pour explorer des données et voir les résultats au fur et à mesure.
- Un éditeur/IDE comme VS Code avec un bouton « Run » : pour écrire et déboguer un projet de plusieurs fichiers.

### A.3 — Les types de base

**1. Quels sont les types de base en Python ? Que signifie « typage dynamique » ? Que donne `"3" + 4` et pourquoi ?**

Les types de base sont : `int` (entier), `float` (décimal), `str` (chaîne de caractères), `bool` (booléen), `list` (liste) et `dict` (dictionnaire). Le typage dynamique signifie qu'on n'indique jamais le type d'une variable à l'avance : Python le déduit de la valeur, et une même variable peut changer de type en cours de route. `"3" + 4` provoque une `TypeError`, car Python n'additionne pas automatiquement une chaîne et un entier : il faut convertir explicitement, par exemple `int("3") + 4` (= 7) ou `"3" + str(4)` (= `"34"`).

### A.4 — Les opérations

**1. Quelle est la différence entre un opérateur booléen et un opérateur logique ?**

En Python, les deux expressions désignent la même chose : `and`, `or`, `not` sont appelés indifféremment opérateurs booléens ou logiques. Ils combinent des valeurs `True`/`False`. Ce qu'il faut surtout distinguer, ce sont les opérateurs de comparaison (`==`, `!=`, `<`, `>`, `<=`, `>=`) : ils comparent deux valeurs et produisent un booléen, alors que `and`/`or`/`not` combinent des booléens existants pour en produire un nouveau.

### A.6 — Les boucles

**1. Quand utilise-t-on une boucle for et quand une boucle while ?**

On utilise `for` quand on connaît à l'avance ce qu'on doit parcourir (une liste, une chaîne, un dictionnaire) ou le nombre d'itérations. On utilise `while` quand on répète tant qu'une condition reste vraie, sans savoir à l'avance combien de tours seront nécessaires (par exemple : répéter jusqu'à ce qu'une valeur dépasse un seuil).

## Partie B — Git et GitHub

**1. C'est quoi Git ? C'est quoi GitHub ? Quelle est la différence entre les deux ?**

Git est un logiciel de gestion de versions installé en local : il suit l'historique des modifications d'un projet, permet de créer des branches et de revenir en arrière. GitHub est une plateforme en ligne qui héberge des dépôts Git et ajoute des fonctionnalités collaboratives (pull requests, issues, gestion des droits d'accès). En résumé : Git est l'outil, GitHub est un service en ligne qui l'utilise.

**2. Pourquoi utiliser Git et GitHub ?**

Cela permet de garder un historique complet des modifications (qui a changé quoi, et quand), de revenir facilement à une version antérieure en cas d'erreur, de travailler à plusieurs sur le même projet sans écraser le travail des autres grâce aux branches et aux fusions, et de faire relire son code avant de l'intégrer via les pull requests.

## Partie C — Découvrir les données, puis appeler l'API

### C.1 — Explorer un dictionnaire (`explorer_dictionnaire.py`)

**1. Quand on affecte une valeur à une clé qui existe déjà, que se passe-t-il ? Un dictionnaire peut-il contenir deux fois la même clé ?**

La nouvelle valeur remplace l'ancienne : la clé garde sa place, seule sa valeur change. Un dictionnaire ne peut pas contenir deux fois la même clé, chaque clé est unique. Si on écrit deux fois la même clé dans un dictionnaire littéral, seule la dernière valeur est conservée.

**2. Après `.copy()` et modification de la copie, l'original est-il modifié ? Et si l'on modifie `rates` ?**

Si on modifie une clé de premier niveau de la copie (par exemple `amount`), l'original ne change pas : `.copy()` crée un nouveau dictionnaire pour le premier niveau. En revanche, si on modifie la partie imbriquée `rates`, l'original change aussi : `.copy()` est une copie superficielle, la copie et l'original pointent vers le même sous-dictionnaire en mémoire.

**3. C'est quoi la mutabilité ? Copie superficielle ou profonde ? Comment faire une copie profonde ?**

La mutabilité est la capacité d'un objet à être modifié après sa création sans changer d'identité en mémoire. Une copie superficielle (`.copy()`) ne duplique que le premier niveau : les objets imbriqués restent partagés. Une copie profonde duplique tous les niveaux, elle est donc totalement indépendante de l'original. On la fait avec `copy.deepcopy()` du module `copy`.

**4. Quels types sont mutables ? Lesquels sont immuables ?**

Mutables : `list`, `dict`, `set` (par exemple `ma_liste.append(1)` modifie la liste). Immuables : `int`, `float`, `str`, `bool`, `tuple` : toute « modification » crée un nouvel objet, par exemple `"abc".upper()` renvoie une nouvelle chaîne sans modifier l'originale.

### C.2 — Appeler l'API pour de vrai (`api_frankfurter.py`)

Le script appelle `/latest` puis la série du 1er janvier au 1er septembre 2026 pour EUR/THB et EUR/USD. La réponse brute est enregistrée dans `cache/` et une version CSV (`date,THB` ou `date,USD`) dans `donnees/`.

Remarque : la série renvoyée commence le **31 décembre 2025**. Le 1er janvier est férié, donc la BCE ne publie pas de taux ce jour-là ; l'API renvoie alors le dernier taux publié avant la date demandée. On obtient 171 jours ouvrés, du 31/12/2025 au 01/09/2026.

**1. Qu'est-ce qu'une API ? Que signifie « envoyer une requête » ? Qu'est-ce que le JSON et en quels types Python se traduit-il ?**

Une API (interface de programmation) est un point d'accès qui permet à un programme de demander des données ou des services à un autre programme, sans connaître son fonctionnement interne. Envoyer une requête, c'est contacter l'adresse (URL) du serveur via internet pour lui demander une information ; le serveur répond avec les données. Le JSON est un format texte standard d'échange de données structurées. En Python, un objet JSON devient un `dict`, un tableau une `list`, une chaîne un `str`, un nombre un `int` ou `float`, `true`/`false` un `bool` et `null` devient `None`.

**2. Pourquoi enregistrer la réponse dans `cache/` plutôt que rappeler l'API à chaque exécution ?**

Cela évite de solliciter le serveur à chaque exécution (plus rapide, fonctionne sans connexion), réduit le risque d'être bloqué pour trop de requêtes, et garantit qu'on retravaille toujours sur les mêmes données, donc des résultats reproductibles, même si l'API est temporairement indisponible.
