# 🚀 Guide de démarrage - Projet Drive

## 📋 Prérequis

- Python 3.8+
- pip (gestionnaire de paquets Python)
- Un terminal/console

## ⚙️ Installation

### 1. Cloner le projet (ou ouvrir le dossier)

```bash
cd /Users/louis/Documents/IUT/SAE203
```

### 2. Créer l'environnement virtuel

```bash
python -m venv venv
```

### 3. Activer l'environnement virtuel

**Sur macOS/Linux:**
```bash
source venv/bin/activate
```

**Sur Windows:**
```bash
venv\Scripts\activate
```

### 4. Installer les dépendances

```bash
pip install -r requirements.txt
```

Fichier `requirements.txt`:
```
asgiref==3.11.1
Django==5.2.14
PyMySQL==1.1.3
sqlparse==0.5.5
```

### 5. Vérifier l'installation

```bash
python manage.py check
```

Résultat attendu:
```
System check identified no issues (0 silenced).
```

## 🗄️ Base de données

### 1. Effectuer les migrations

```bash
python manage.py migrate
```

### 2. Créer un utilisateur admin (optionnel)

```bash
python manage.py createsuperuser
```

Suivez les instructions pour créer un login administrateur.

### 3. Importer des données (optionnel)

Si vous avez un dump SQL:
```bash
python manage.py populate_db
```

## 🚀 Démarrer le serveur

```bash
python manage.py runserver
```

Vous devriez voir:
```
Django version 5.2.14, using settings 'project.settings'
...
Starting development server at http://127.0.0.1:8000/
```

## 🌐 Accéder à l'application

### URL Principale
```
http://127.0.0.1:8000/drive/
```

### URL Admin
```
http://127.0.0.1:8000/admin/
```

## 📊 Structure

```
SAE203/
├── db.sqlite3                  # Base de données
├── manage.py                   # Commandes Django
├── requirements.txt            # Dépendances
├── drive/                      # Application principale
│   ├── models.py              # Modèles (Produit, Client, etc.)
│   ├── views.py               # Vues (logique métier)
│   ├── urls.py                # Routage
│   ├── admin.py               # Configuration admin
│   ├── static/
│   │   └── drive/
│   │       ├── style.css      # Styles CSS
│   │       └── autocomplete.js # Autocomplete JavaScript
│   └── templates/
│       └── drive/
│           ├── base.html       # Template de base
│           ├── commande_detail.html
│           ├── produit_list.html
│           └── ... (autres templates)
└── project/                    # Configuration Django
    ├── settings.py             # Paramètres
    ├── urls.py                 # Routes principales
    └── wsgi.py                 # Serveur WSGI
```

## 🎯 Fonctionnalités principales

### Catégories
- ✅ Créer une catégorie
- ✅ Lister les catégories
- ✅ Modifier une catégorie
- ✅ Supprimer une catégorie

### Produits
- ✅ Créer un produit
- ✅ Lister les produits
- ✅ Modifier un produit
- ✅ Supprimer un produit
- ✅ **Autocomplete** lors de l'ajout à une commande

### Clients
- ✅ Créer un client
- ✅ Lister les clients
- ✅ Voir les détails d'un client
- ✅ Historique des commandes
- ✅ Modifier un client
- ✅ Supprimer un client

### Commandes
- ✅ Créer une commande
- ✅ Lister les commandes
- ✅ Voir les détails d'une commande
- ✅ **Ajouter un produit** (avec autocomplete 🔥)
- ✅ Modifier la quantité d'un produit
- ✅ Retirer un produit de la commande
- ✅ Supprimer une commande

## 🧪 Tester

Voir le fichier `TEST_AUTOCOMPLETE.md` pour tester l'autocomplete.

## 📖 Documentation

- `README.md` - Vue d'ensemble
- `FEATURES.md` - Fonctionnalités détaillées
- `TEST_AUTOCOMPLETE.md` - Guide de test
- `CRUD_GUIDE.md` - Guide CRUD (si existant)

## 🐛 Dépannage

### Erreur: "Le module n'est pas trouvé"
```
ModuleNotFoundError: No module named 'django'
```

**Solution:** Activez l'environnement virtuel:
```bash
source venv/bin/activate  # macOS/Linux
```

### Erreur: "Port 8000 déjà utilisé"
```
Error: That port is already in use.
```

**Solution:** Utilisez un autre port:
```bash
python manage.py runserver 8001
```

### Erreur: "Base de données verrouillée"
```
sqlite3.OperationalError: database is locked
```

**Solution:** Arrêtez le serveur et redémarrez-le.

### L'autocomplete ne fonctionne pas?

Voir `TEST_AUTOCOMPLETE.md` - Section "Dépannage".

## 📞 Support

Pour toute question, consultez:
- La console (F12) pour les erreurs JavaScript
- Les logs Django dans le terminal
- Les fichiers de documentation

---

**Bon développement!** ✨

