# projet-python-taux-BCE

Projet Python BFA1 en groupe (2026-2027) — Analyse des taux de change de référence de la BCE, **EUR/THB** et **EUR/USD**, du 1er janvier au 1er septembre 2026, via l'API Frankfurter.

Groupe : Luca Radu, Victor Mavre-Gigault, Théophile Le Metter, Léopold Santamaria 

## Installation

Python 3.11 ou plus récent.

```bash
git clone https://github.com/LucaR2907/ecb-exchange-rates.git
cd ecb-exchange-rates
python -m venv .venv
source .venv/bin/activate        # Windows : .venv\Scripts\activate
pip install -r requirements.txt
```

Les séances 1 et 2 n'utilisent que la bibliothèque standard ; `pandas`, `numpy`, `polars` (séance 3) et `matplotlib` (séance 4) sont dans `requirements.txt`.

## Utilisation

Outil en ligne de commande (séance 4) :

```bash
python main.py --help
python main.py extraire              # télécharge les séries depuis l'API (avec gestion d'erreurs + logs/api.log)
python main.py analyser              # Python idiomatique + classes, sur EUR/THB
python main.py analyser --devise USD
python main.py graphiques            # crée les PNG dans figures/
```

Scripts de chaque séance :

```bash
# Séance 1
python hello_world.py
python bases_python.py
python explorer_dictionnaire.py
python api_frankfurter.py            # appel API -> cache/ et donnees/

# Séance 2
python fonctions.py                  # lecture CSV, moyenne, min/max
python api_securisee.py              # API avec try/except et logging
python recursivite.py                # factorielle, Fibonacci, mesures

# Séance 3
python analyse.py                    # pandas, forward-fill, jointures, numpy, polars
```

## Organisation du dépôt

```
├── README.md, requirements.txt, .gitignore
├── rapport_final.md            # démarche, résultats, graphiques
├── main.py                     # CLI argparse (séance 4)
├── hello_world.py, bases_python.py, explorer_dictionnaire.py, api_frankfurter.py   # séance 1
├── fonctions.py, api_securisee.py, recursivite.py                                   # séance 2
├── analyse.py                                                                       # séance 3
├── src/                        # package (séance 4)
│   ├── serie.py                # classe SerieTaux + dataclass Resume
│   ├── idiomatique.py          # compréhensions, enumerate, zip, sorted, lambda...
│   └── graphiques.py           # graphiques matplotlib
├── cache/                      # réponses brutes de l'API (JSON)
├── donnees/                    # taux_EUR_THB.csv, taux_EUR_USD.csv
├── figures/                    # graphiques PNG
└── docs/                       # notes_seance1.md à notes_seance4.md (réponses aux questions)
```

## Données

Source : taux de référence de la BCE via l'API Frankfurter (`https://api.frankfurter.app`). 171 jours ouvrés par devise, du 31/12/2025 au 01/09/2026 : le 1er janvier étant férié, l'API commence au dernier taux publié avant cette date. Un taux = nombre de THB (ou d'USD) pour 1 EUR. Les réponses brutes de l'API sont gardées dans `cache/` pour ne pas rappeler l'API à chaque exécution.

## Principaux résultats

| Série | Moyenne | Min | Max | Variation 31/12/2025 → 01/09/2026 |
|---|---:|---:|---:|---:|
| EUR/THB | 37.652 | 36.353 | 38.570 | +3.59 % |
| EUR/USD | 1.1624 | 1.1340 | 1.1974 | −1.36 % |

Détails et graphiques dans [`rapport_final.md`](rapport_final.md).
