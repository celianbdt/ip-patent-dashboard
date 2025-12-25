# Historique des Modifications

## Version 2.0 - 25 Décembre 2024

### 🎨 Améliorations Visuelles
- ✅ **Correction des couleurs** : Le texte est maintenant visible sur fond noir (texte en blanc/gris clair)
- ✅ Headers et titres en blanc pour meilleure lisibilité
- ✅ Texte des paragraphes en gris clair (#e0e0e0)
- ✅ Labels des filtres dans la sidebar restent en noir pour contraste

### 🌍 Correction des Régions
- ✅ **Région corrigée** : Les valeurs "Region" et "Unknown" sont maintenant converties en "NA"
- ✅ Seules deux régions disponibles : **EU** et **NA**
- ✅ Distribution actuelle :
  - EU : 17,697 profils
  - NA : 24,229 profils

### 📊 Nouveau : Système de Tiering
- ✅ **Calcul automatique du tiering** basé sur le nombre de profils IP par entreprise
- ✅ **3 niveaux définis** :
  - **T1** : Entreprises avec >30 profils IP (128 entreprises)
  - **T2** : Entreprises avec 5-30 profils IP (1,135 entreprises)
  - **T3** : Entreprises avec 0-5 profils IP (11,321 entreprises)

### 🔍 Nouveau : Filtre Tiering
- ✅ Filtre multiselect pour sélectionner T1, T2 et/ou T3
- ✅ Tooltip explicatif sur les définitions des tiers
- ✅ Fonctionne en Vue Simple et Mode Comparaison

### 🆚 Nouveau : Comparaison par Tiering
- ✅ **Mode "Tiering vs Tiering"** ajouté dans le Mode Comparaison
- ✅ Permet de comparer T1 vs T2, T1 vs T3, T2 vs T3, etc.
- ✅ Également disponible en mode "Custom"
- ✅ Tous les graphiques supportent la comparaison par tiering

### 📈 Nouveau : Graphique de Distribution du Tiering
- ✅ Graphique 3 dans l'onglet "Global & Company Overview"
- ✅ Affiche le nombre d'entreprises par tier
- ✅ Statistiques détaillées avec pourcentages
- ✅ Support du mode comparaison (graphiques côte à côte)
- ✅ Légende explicative : T1: >30 | T2: 5-30 | T3: 0-5 profils IP

### 🔢 Renumérotation des Graphiques
En raison de l'ajout du graphique de tiering :
- **Graphique 3** : Distribution du Tiering (nouveau)
- **Graphique 4** : Top 10 des Pays (anciennement 3)
- **Graphique 5** : Densité IP (anciennement 4)
- **Graphique 6** : Workflows (anciennement 5)
- **Graphique 7** : Répartition Séniorité (anciennement 6)
- **Graphique 8** : Top Job Titles (anciennement 7)
- **Graphique 9** : Séniorité par Persona (anciennement 8)

### 📚 Documentation
- ✅ README.md mis à jour avec les nouvelles fonctionnalités
- ✅ CHANGELOG.md créé pour suivre les versions
- ✅ Toutes les nouvelles fonctionnalités documentées

---

## Version 1.0 - 25 Décembre 2024

### Fonctionnalités Initiales
- Dashboard interactif avec Streamlit et Plotly
- 2 modes : Vue Simple et Mode Comparaison
- Filtres multiples (Région, Entreprise, Industrie, Pays, Seniority)
- 3 onglets d'analyse
- 8 graphiques interactifs
- Export CSV des données filtrées
- Normalisation des job titles
- Système de comparaison flexible

---

## Statistiques du Dataset

**Total des profils** : 41,926 profils IP

**Répartition par région** :
- NA : 57.8% (24,229 profils)
- EU : 42.2% (17,697 profils)

**Répartition par tiering** :
- T1 (>30 profils) : 128 entreprises (1.0%)
- T2 (5-30 profils) : 1,135 entreprises (9.0%)
- T3 (0-5 profils) : 11,321 entreprises (90.0%)

**Total entreprises** : 12,584 entreprises uniques

**Moyenne de profils IP par entreprise** : 3.33 profils
