# Oracle Paris 2024 - Prédictions Olympiques

**[Voir la Présentation (Canva)](https://www.canva.com/design/DAG-lLUaYxM/pqSHDViuAFMNM5sQ_dwUKQ/edit?utm_content=DAG-lLUaYxM&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton)**

## Description
Une application web **Django** avancée conçue pour explorer les données historiques olympiques, démystifier les idées reçues et prédire les résultats des Jeux Olympiques de Paris 2024 à l'aide du **Machine Learning (XGBoost)**.

![Aperçu du Dashboard](docs/dashboard_preview.png)

## Fonctionnalités

### 1. Tableau de Bord Interactif & Explorateur
-   **KPI de Haut Niveau** : Statistiques en temps réel sur les médailles, athlètes et jeux.
-   **Graphiques Interactifs** : 
    -   Carte choroplèthe mondiale (Plotly) montrant la distribution des médailles.
    -   Analyse des pays hôtes (principaux organisateurs).
    -   Analyses approfondies par pays (Focus France : Évolution des médailles, performances saisonnières).

### 2. Prédictions IA (Oracle Paris 2024)
-   **Prévisions Algorithmiques** : Utilise un **XGBoost Regressor** entraîné sur 120 ans d'historique pour prédire le nombre de médailles à Paris 2024.
-   **Feature Engineering** : Prend en compte l'avantage du pays hôte, la taille de la délégation et les performances historiques.
-   **Visualisations** :
    -   **Podium** : Cartes dynamiques en "Glassmorphisme" pour le Top 3 des favoris.
    -   **Classement** : Prédictions complètes avec recherche et filtrage.
    -   **Carte Dorée** : Focus spécifique sur la performance prédite de la France (+Comparaisons).

### 3. Mythes & Vérification des Faits
-   Cartes interactives vérifiant les mythes olympiques courants (ex : "Les femmes ont-elles participé en 1900 ?").
-   Verdicts basés sur les données (Vrai/Faux) avec aperçu historique.

### 4. Comparaison Réel vs IA
-   **Mode Simulation** : Une page dédiée comparant les prédictions de l'IA avec les résultats "officiels" (simulés).
-   **Métriques de Performance** : Indicateurs visuels de la précision de l'IA (Précision, Sur/Sous-performance).

---

## Stack Technologique

-   **Backend** : Python 3.10+, Django 5.x
-   **Base de Données** : PostgreSQL (via Supabase)
-   **Data Science** : Pandas, NumPy, XGBoost, Scikit-Learn
-   **Frontend** : HTML5, Bootstrap 5, Thème Dark Mode
-   **Visualisation** : Plotly.js (Rendu côté client pour l'interactivité)

---

## Installation & Configuration

### 1. Cloner le Dépôt
```bash
git clone https://github.com/youcisla/Challenge-Big-Data.git
cd Challenge-Big-Data
```

### 2. Installer les Dépendances
```powershell
pip install -r requirements.txt
```
Ou utiliser le Makefile :
```powershell
make install
```

### 3. Configuration de l'Environnement
Créez un fichier `.env` à la racine du projet avec vos identifiants de base de données :
```ini
user=postgres.your_project_ref
password=your_database_password
host=aws-0-eu-central-1.pooler.supabase.com
port=6543
dbname=postgres
SECRET_KEY=your_django_secret_key
DEBUG=True
```

Un fichier `.env.example` est fourni comme modèle.

### 4. Configuration de la Base de Données
Exécutez le script d'importation pour remplir la table `olympic_stats` depuis le dataset CSV :
```powershell
python import_data.py
```

Si nécessaire, vous pouvez également appliquer le schéma SQL :
```powershell
python apply_schema.py
```

### 5. Lancer l'Application
Vous pouvez utiliser le script helper (Windows) :
```powershell
./make run
```
Ou utiliser le Makefile :
```bash
make run
```
Ou encore la commande Django standard :
```powershell
python manage.py runserver
```

Ouvrez votre navigateur à l'adresse **http://127.0.0.1:8000** pour accéder à l'Oracle.

---

## Commandes Disponibles

Le projet inclut un **Makefile** pour simplifier les tâches courantes :

-   `make install` : Installe toutes les dépendances Python
-   `make run` : Lance le serveur de développement Django
-   `make clean` : Nettoie les fichiers cache Python (`*.pyc`, `__pycache__`)

---

## Structure du Projet

```
Challenge-Big-Data/
├── config/              # Configuration Django et routage des URLs
├── core/                # Logique de l'application
│   ├── views.py         # Contrôle du flux de données et du rendu
│   ├── models.py        # Définition du schéma de base de données
│   └── ml_service.py    # Service singleton gérant le modèle XGBoost
├── ml_models/           # Modèles ML entraînés (.pkl)
├── templates/           # Templates HTML avec Bootstrap
│   ├── base.html        # Template de base
│   └── core/            # Templates de l'application
│       ├── home.html           # Page d'accueil
│       ├── explorer.html       # Explorateur de données
│       ├── predictions.html    # Prédictions IA
│       ├── myths.html          # Mythes olympiques
│       └── comparison.html     # Comparaison Réel vs IA
├── static/              # CSS, Images et JS
├── data/                # Datasets CSV bruts
├── notebooks/           # Notebooks Jupyter pour l'analyse
├── requirements.txt     # Dépendances Python
├── Makefile             # Commandes de développement
└── manage.py            # Point d'entrée Django
```

---

## Pages de l'Application

1. **Accueil** (`/`) : Vue d'ensemble avec KPIs et introduction
2. **Explorateur** (`/explorer`) : Visualisations interactives des données historiques
3. **Prédictions** (`/predictions`) : Prédictions IA pour Paris 2024 avec podium et classement
4. **Mythes** (`/myths`) : Vérification des mythes olympiques
5. **Comparaison** (`/comparison`) : Comparaison entre prédictions IA et résultats simulés

---

## Données

-   **Source** : Données historiques olympiques (1896-2024)
-   **Format** : CSV stocké dans le dossier `data/`
-   **Stockage** : PostgreSQL (Supabase) pour les requêtes performantes

---

## Licence

Ce projet a été développé dans le cadre d'un challenge Big Data.
