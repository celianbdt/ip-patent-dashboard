# 🚀 Déploiement en 3 Étapes Simples

## Temps total : 10 minutes ⏱️

---

## Étape 1️⃣ : Créer un compte GitHub (2 min)

1. Allez sur **https://github.com**
2. Cliquez sur **"Sign up"**
3. Créez votre compte (gratuit)
4. Confirmez votre email

✅ **Déjà un compte ?** Connectez-vous et passez à l'étape 2

---

## Étape 2️⃣ : Uploader votre projet sur GitHub (5 min)

### Méthode Automatique (Recommandée) 🤖

Ouvrez un terminal dans le dossier du projet et exécutez :

```bash
cd "/Users/celianbaudet/Desktop/Freelance/Deep IP/TAM"
./init_git.sh celianbdt
```

Remplacez `VOTRE_USERNAME_GITHUB` par votre username GitHub.

Le script va :
- ✅ Initialiser Git
- ✅ Ajouter tous les fichiers
- ✅ Créer le commit
- ✅ Configurer le remote

Ensuite :

1. **Créez le repository sur GitHub** : https://github.com/new
   - Repository name : `ip-patent-dashboard`
   - Visibilité : **Public**
   - ❌ Ne cochez PAS "Add a README file"
   - Cliquez sur **"Create repository"**

2. **Poussez votre code** :
   ```bash
   git push -u origin main
   ```

### Méthode Manuelle (Alternative) 🖱️

1. **Créez un nouveau repository sur GitHub** : https://github.com/new
   - Repository name : `ip-patent-dashboard`
   - Visibilité : **Public**
   - ✅ Cochez "Add a README file"
   - Cliquez sur **"Create repository"**

2. **Uploadez vos fichiers** :
   - Cliquez sur **"Add file"** → **"Upload files"**
   - Glissez-déposez tous les fichiers du dossier TAM :
     - `app.py`
     - `requirements.txt`
     - `TAM Corporations IP Patent Litigation.csv` (si non sensible)
     - Tous les fichiers .md
     - Dossier `.streamlit/`
   - Cliquez sur **"Commit changes"**

---

## Étape 3️⃣ : Déployer sur Streamlit Cloud (3 min)

1. **Allez sur** : https://share.streamlit.io

2. **Cliquez sur "Sign in"** → Connectez-vous avec GitHub

3. **Autorisez Streamlit** à accéder à vos repositories

4. **Cliquez sur "New app"**

5. **Remplissez le formulaire** :
   - **Repository** : `VOTRE_USERNAME/ip-patent-dashboard`
   - **Branch** : `main`
   - **Main file path** : `app.py`

6. **Cliquez sur "Deploy!"**

7. **Attendez 2-3 minutes** ⏳

8. **🎉 C'EST EN LIGNE !**

---

## 🔗 Votre Dashboard

Votre URL sera quelque chose comme :

```
https://votre-username-ip-patent-dashboard-app-xxxxx.streamlit.app
```

**Partagez cette URL avec qui vous voulez !**

---

## 🔄 Mettre à jour plus tard

Pour modifier votre dashboard :

1. Modifiez `app.py` localement
2. Poussez sur GitHub :
   ```bash
   git add .
   git commit -m "Mise à jour"
   git push
   ```
3. **Le dashboard se met à jour automatiquement** en 1-2 minutes !

---

## ⚠️ Si votre CSV contient des données sensibles

**Option 1** : Ne l'uploadez pas sur GitHub (voir `DEPLOY_FACILE.md` pour utiliser Google Drive)

**Option 2** : Utilisez un repository privé (nécessite Streamlit Teams payant)

---

## ❓ Problème ?

Consultez `DEPLOY_FACILE.md` pour plus de détails ou contactez-moi.

---

**C'est tout ! Simple non ? 😊**
