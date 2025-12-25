# Dashboard d'Analyse de Propriété Intellectuelle

Ce tableau de bord interactif permet d'analyser les données de propriété intellectuelle à partir du fichier CSV "TAM Corporations IP Patent Litigation.csv".

## Fonctionnalités

### Modes de visualisation
- **Vue Simple** : Analysez vos données avec des filtres multiples
- **Mode Comparaison** : Comparez deux groupes
  - Région vs Région (ex: NA vs EU)
  - Entreprise vs Entreprise
  - Pays vs Pays (ex: France vs USA)
  - **Tiering vs Tiering** (ex: T1 vs T2) - Nouveau ! 🆕
  - Custom (combinaisons personnalisées)

### Filtres dynamiques
- **Région/Continent** (NA, EU)
- **Entreprise**
- **Industrie** (Top 10 + Other)
- **Taille d'entreprise**
- **Pays**
- **Niveau de séniorité**
- **Tiering** (T1, T2, T3) - Nouveau ! 🆕
  - T1 : Entreprises avec >30 profils IP
  - T2 : Entreprises avec 5-30 profils IP
  - T3 : Entreprises avec 0-5 profils IP

### Analyses avancées
- **KPIs clés** : Visualisez rapidement les métriques importantes (nombre de profils, entreprises uniques, etc.)
- **Vue d'ensemble globale** : Analysez la distribution des industries, tailles d'entreprises et localisations
- **Analyse de densité IP** : Examinez le rapport entre le nombre de profils IP et la taille des entreprises
- **Workflows** : Analysez la répartition entre Patent Litigation, Patent Preparation & Prosecution, et Both
- **Analyse des talents** : Explorez la distribution des niveaux de séniorité et des rôles avec regroupement intelligent des job titles
- **Export de données** : Téléchargez les données filtrées en CSV

### Améliorations visuelles
- Interface moderne avec thème bleu
- **Texte optimisé** : Couleurs adaptées pour une meilleure lisibilité sur fond sombre
- Graphiques interactifs avec Plotly
- Pourcentages affichés directement sur les graphiques
- Comparaisons côte à côte en mode comparaison
- **Graphique de distribution du tiering** dans l'onglet Global & Company Overview

## Installation

1. Clonez ce dépôt ou téléchargez les fichiers
2. Installez les dépendances:

```
pip install -r requirements.txt
```

3. Placez le fichier CSV "TAM Corporations IP Patent Litigation.csv" dans le même répertoire que l'application.

## Lancement de l'application

```
streamlit run app.py
```

L'application sera accessible dans votre navigateur à l'adresse http://localhost:8501.

## Structure des onglets

1. **Global & Company Overview** : Vue d'ensemble sur les industries, tailles d'entreprises et localisations.
2. **IP Strategy & Density** : Analyse de la densité IP et des types de workflows.
3. **Talent & Seniority** : Analyse des niveaux de séniorité et des rôles.

## Prérequis

- Python 3.9+
- Streamlit
- Pandas
- Plotly
- NumPy
