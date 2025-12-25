#!/bin/bash

# Script d'initialisation Git pour déploiement facile
# Usage: ./init_git.sh VOTRE_USERNAME_GITHUB

echo "🚀 Script d'initialisation Git pour déploiement Streamlit"
echo "=========================================================="
echo ""

# Vérifier si un username est fourni
if [ -z "$1" ]; then
    echo "❌ Erreur: Vous devez fournir votre username GitHub"
    echo ""
    echo "Usage: ./init_git.sh VOTRE_USERNAME_GITHUB"
    echo "Exemple: ./init_git.sh celianbaudet"
    echo ""
    exit 1
fi

GITHUB_USERNAME=$1
REPO_NAME="ip-patent-dashboard"

echo "👤 Username GitHub: $GITHUB_USERNAME"
echo "📦 Nom du repository: $REPO_NAME"
echo ""

# Vérifier si git est installé
if ! command -v git &> /dev/null; then
    echo "❌ Git n'est pas installé. Installez-le depuis https://git-scm.com"
    exit 1
fi

echo "✅ Git est installé"
echo ""

# Initialiser git si pas déjà fait
if [ ! -d ".git" ]; then
    echo "📝 Initialisation du repository Git..."
    git init
    echo "✅ Repository Git initialisé"
else
    echo "✅ Repository Git déjà initialisé"
fi

echo ""
echo "📋 Ajout des fichiers au repository..."

# Ajouter les fichiers essentiels
git add app.py
git add requirements.txt
git add README.md
git add QUICKSTART.md
git add DEPLOYMENT_GUIDE.md
git add DEPLOY_FACILE.md
git add CHANGELOG.md
git add .gitignore
git add .streamlit/config.toml

echo "✅ Fichiers ajoutés"
echo ""

# Demander si on doit ajouter le CSV
echo "⚠️  IMPORTANT: Votre fichier CSV contient-il des données sensibles ?"
echo "   Si OUI → Ne l'ajoutez PAS à GitHub"
echo "   Si NON → Vous pouvez l'ajouter"
echo ""
read -p "Voulez-vous ajouter le CSV au repository ? (o/N): " add_csv

if [[ $add_csv =~ ^[Oo]$ ]]; then
    echo "📄 Ajout du CSV..."
    git add "TAM Corporations IP Patent Litigation.csv"
    echo "✅ CSV ajouté"
else
    echo "⏭️  CSV non ajouté (recommandé si données sensibles)"
fi

echo ""
echo "💾 Création du commit initial..."
git commit -m "Initial commit - Dashboard IP Patent Litigation v2.0"

if [ $? -eq 0 ]; then
    echo "✅ Commit créé avec succès"
else
    echo "⚠️  Aucun changement à commiter ou commit déjà effectué"
fi

echo ""
echo "🌿 Configuration de la branche principale..."
git branch -M main
echo "✅ Branche 'main' configurée"

echo ""
echo "🔗 Configuration du remote GitHub..."
REMOTE_URL="https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"
git remote remove origin 2>/dev/null
git remote add origin $REMOTE_URL
echo "✅ Remote configuré: $REMOTE_URL"

echo ""
echo "=========================================================="
echo "✅ Configuration Git terminée !"
echo "=========================================================="
echo ""
echo "📋 PROCHAINES ÉTAPES:"
echo ""
echo "1. Créez le repository sur GitHub:"
echo "   👉 https://github.com/new"
echo "   - Repository name: $REPO_NAME"
echo "   - Visibilité: Public (obligatoire pour Streamlit gratuit)"
echo "   - ❌ Ne cochez PAS 'Add a README file'"
echo ""
echo "2. Une fois le repository créé, exécutez:"
echo "   git push -u origin main"
echo ""
echo "3. Déployez sur Streamlit Cloud:"
echo "   👉 https://share.streamlit.io"
echo "   - Connectez-vous avec GitHub"
echo "   - Cliquez sur 'New app'"
echo "   - Repository: $GITHUB_USERNAME/$REPO_NAME"
echo "   - Branch: main"
echo "   - Main file: app.py"
echo "   - Cliquez sur 'Deploy!'"
echo ""
echo "🎉 Votre dashboard sera accessible à:"
echo "   https://$GITHUB_USERNAME-$REPO_NAME-app-xxxxx.streamlit.app"
echo ""
echo "📖 Plus de détails dans DEPLOY_FACILE.md"
echo ""
