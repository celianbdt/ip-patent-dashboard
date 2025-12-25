# Guide de Déploiement du Dashboard IP Patent Litigation

Ce guide vous explique comment déployer votre dashboard Streamlit **gratuitement** pour le partager avec vos collaborateurs.

## Options de Déploiement Gratuites

### Option 1 : Streamlit Community Cloud (RECOMMANDÉ) ⭐

**Avantages :**
- Gratuit et illimité
- Intégration facile avec GitHub
- Mises à jour automatiques
- URL personnalisée gratuite
- Pas de configuration serveur nécessaire

**Étapes :**

1. **Créer un compte GitHub** (si vous n'en avez pas)
   - Aller sur https://github.com
   - Créer un compte gratuit

2. **Créer un repository GitHub**
   - Cliquer sur "New repository"
   - Nom: `ip-patent-dashboard` (ou autre nom)
   - Choisir "Public" (obligatoire pour le plan gratuit)
   - Cliquer sur "Create repository"

3. **Uploader vos fichiers sur GitHub**
   - Télécharger GitHub Desktop ou utiliser la ligne de commande
   - Ajouter les fichiers suivants:
     - `app.py`
     - `requirements.txt`
     - `TAM Corporations IP Patent Litigation.csv`
     - `README.md`

   **Via ligne de commande :**
   ```bash
   cd "/Users/celianbaudet/Desktop/Freelance/Deep IP/TAM"
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/VOTRE_USERNAME/ip-patent-dashboard.git
   git push -u origin main
   ```

4. **Déployer sur Streamlit Community Cloud**
   - Aller sur https://share.streamlit.io
   - Se connecter avec votre compte GitHub
   - Cliquer sur "New app"
   - Sélectionner votre repository `ip-patent-dashboard`
   - Sélectionner la branche `main`
   - Fichier principal: `app.py`
   - Cliquer sur "Deploy!"

5. **Partager l'URL**
   - Votre app sera disponible à: `https://VOTRE_USERNAME-ip-patent-dashboard-app-xxxxx.streamlit.app`
   - Partagez cette URL avec vos collaborateurs

**Important :**
- Si votre fichier CSV contient des données sensibles, considérez l'Option 2 (repository privé avec authentification)

---

### Option 2 : Hugging Face Spaces

**Avantages :**
- Gratuit
- Bonne performance
- Support de fichiers volumineux
- Peut être privé

**Étapes :**

1. **Créer un compte Hugging Face**
   - Aller sur https://huggingface.co
   - Créer un compte gratuit

2. **Créer un Space**
   - Cliquer sur votre profil → "Spaces" → "Create new Space"
   - Nom: `ip-patent-dashboard`
   - License: Apache 2.0
   - SDK: Streamlit
   - Choisir "Public" ou "Private"
   - Cliquer sur "Create Space"

3. **Uploader vos fichiers**
   - Dans l'interface du Space, cliquer sur "Files"
   - Uploader `app.py`, `requirements.txt`, `TAM Corporations IP Patent Litigation.csv`

4. **Accéder à votre app**
   - L'URL sera: `https://huggingface.co/spaces/VOTRE_USERNAME/ip-patent-dashboard`

---

### Option 3 : Render (avec limitations)

**Avantages :**
- Gratuit
- Facile à configurer
- Support Docker

**Limitations :**
- Se met en veille après 15 minutes d'inactivité
- Temps de démarrage de ~30 secondes après inactivité

**Étapes :**

1. **Créer un compte sur Render**
   - Aller sur https://render.com
   - S'inscrire gratuitement

2. **Connecter votre repository GitHub**
   - Suivre les étapes 1-3 de l'Option 1 pour créer un repo GitHub

3. **Créer un Web Service**
   - Dans Render, cliquer sur "New" → "Web Service"
   - Connecter votre repository GitHub
   - Configuration:
     - Environment: Python 3
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`
   - Cliquer sur "Create Web Service"

4. **Accéder à votre app**
   - L'URL sera: `https://ip-patent-dashboard.onrender.com`

---

## Sécurisation de votre Dashboard

### Ajouter une authentification simple

Pour protéger votre dashboard avec un mot de passe, ajoutez ce code au début de `app.py`:

```python
import streamlit as st
import hashlib

def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hashlib.sha256(st.session_state["password"].encode()).hexdigest() == "votre_hash_mot_de_passe":
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store password
        else:
            st.session_state["password_correct"] = False

    if st.session_state.get("password_correct", False):
        return True

    st.text_input(
        "Mot de passe", type="password", on_change=password_entered, key="password"
    )
    if "password_correct" in st.session_state:
        st.error("😕 Mot de passe incorrect")
    return False

if not check_password():
    st.stop()
```

Pour générer le hash de votre mot de passe:
```python
import hashlib
password = "votre_mot_de_passe"
print(hashlib.sha256(password.encode()).hexdigest())
```

---

## Gestion des Données Sensibles

Si votre fichier CSV contient des données sensibles:

1. **Ne pas le mettre sur GitHub public**
   - Utilisez un repository privé
   - Ou excluez le CSV du repository avec `.gitignore`

2. **Utiliser un stockage externe**
   - Stockez le CSV sur Google Drive, Dropbox, ou AWS S3
   - Modifiez `app.py` pour charger depuis l'URL

Exemple avec Google Drive:
```python
import pandas as pd
import gdown

# ID du fichier Google Drive (obtenu depuis le lien de partage)
file_id = "VOTRE_FILE_ID"
url = f"https://drive.google.com/uc?id={file_id}"

@st.cache_data
def load_data():
    output = "temp.csv"
    gdown.download(url, output, quiet=False)
    df = pd.read_csv(output, low_memory=False)
    # ... reste du code
    return df
```

Ajoutez `gdown` à votre `requirements.txt`:
```
gdown==4.7.1
```

---

## Maintenance et Mises à Jour

### Mettre à jour votre dashboard

1. **Modifier vos fichiers localement**
2. **Pousser les changements sur GitHub:**
   ```bash
   git add .
   git commit -m "Mise à jour du dashboard"
   git push
   ```
3. **Streamlit Cloud redéploiera automatiquement**

### Surveiller l'utilisation

- Streamlit Community Cloud offre des analytics basiques
- Vous pouvez voir le nombre de visiteurs et les erreurs

---

## Recommandation Finale

**Pour un déploiement rapide et facile : Streamlit Community Cloud**

C'est la solution la plus simple et la plus adaptée pour un dashboard d'analyse comme le vôtre. Vos collaborateurs auront juste besoin de l'URL pour accéder au dashboard.

**URL de votre futur dashboard :**
`https://VOTRE_USERNAME-ip-patent-dashboard-app-xxxxx.streamlit.app`

---

## Support

En cas de problème:
- Documentation Streamlit: https://docs.streamlit.io/streamlit-community-cloud
- Forum Streamlit: https://discuss.streamlit.io
- GitHub Issues: https://github.com/streamlit/streamlit/issues
