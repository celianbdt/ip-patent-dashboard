# Guide de Démarrage Rapide

## 🚀 Lancer l'application localement

### Prérequis
- Python 3.9 ou plus récent
- Le fichier CSV "TAM Corporations IP Patent Litigation.csv" dans le même dossier

### Installation

1. **Ouvrir un terminal** et naviguer vers le dossier du projet :
   ```bash
   cd "/Users/celianbaudet/Desktop/Freelance/Deep IP/TAM"
   ```

2. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```

3. **Lancer l'application** :
   ```bash
   streamlit run app.py
   ```

4. **Accéder à l'application** :
   - L'application s'ouvrira automatiquement dans votre navigateur
   - Sinon, allez sur : http://localhost:8501

---

## 📊 Utilisation

### Mode Simple
1. Dans la sidebar, sélectionnez "Vue Simple"
2. Utilisez les filtres pour affiner vos données :
   - Région/Continent (NA, EU)
   - Entreprise
   - Industrie
   - Taille d'entreprise
   - Pays
   - Niveau de séniorité
3. Explorez les 3 onglets :
   - **Global & Company Overview** : Vue d'ensemble des industries, tailles et localisations
   - **IP Strategy & Density** : Analyse de la densité IP et des workflows
   - **Talent & Seniority** : Distribution des niveaux de séniorité et job titles

### Mode Comparaison
1. Dans la sidebar, sélectionnez "Mode Comparaison"
2. Choisissez le type de comparaison :
   - Région vs Région (ex: NA vs EU)
   - Entreprise vs Entreprise
   - Pays vs Pays
   - Custom (combinaisons personnalisées)
3. Sélectionnez vos deux groupes
4. Les graphiques afficheront les deux groupes côte à côte pour comparaison

---

## 💡 Fonctionnalités Clés

### KPIs
- Nombre de profils
- Entreprises uniques
- Top industrie
- Pourcentage de seniors

### Graphiques Interactifs
- **Zoom** : Cliquez et faites glisser sur un graphique
- **Pan** : Maintenez Shift + clic et faites glisser
- **Reset** : Double-clic sur le graphique
- **Export** : Utilisez l'icône appareil photo en haut à droite de chaque graphique
- **Hover** : Survolez les points pour voir les détails

### Export de Données
- Bouton "📥 Télécharger en CSV" en bas de page
- Télécharge les données actuellement filtrées

---

## 🔧 Résolution de Problèmes

### L'application ne démarre pas
```bash
# Vérifier que Python est installé
python --version

# Réinstaller les dépendances
pip install --upgrade -r requirements.txt
```

### Erreur "Module not found"
```bash
# Installer le module manquant
pip install nom_du_module
```

### L'application est lente
- Réduisez le nombre de filtres actifs
- Fermez les autres onglets du navigateur
- Redémarrez l'application

### Les graphiques ne s'affichent pas
- Vérifiez votre connexion internet (Plotly nécessite une connexion)
- Effacez le cache du navigateur
- Essayez un autre navigateur

---

## 📚 Ressources

- [Documentation Streamlit](https://docs.streamlit.io)
- [Documentation Plotly](https://plotly.com/python/)
- [Guide de Déploiement](DEPLOYMENT_GUIDE.md)

---

## 🆘 Support

Pour toute question ou problème :
1. Vérifiez le [Guide de Déploiement](DEPLOYMENT_GUIDE.md)
2. Consultez les logs dans le terminal
3. Consultez la documentation Streamlit
