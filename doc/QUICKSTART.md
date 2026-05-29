# ⚡ Quick Start - Démarrage rapide

## 🚀 En 5 minutes

### 1. Activer l'environnement

```bash
cd /Users/louis/Documents/IUT/SAE203
source venv/bin/activate  # macOS/Linux
# ou
venv\Scripts\activate     # Windows
```

### 2. Démarrer le serveur

```bash
python manage.py runserver
```

Vous devriez voir:
```
Starting development server at http://127.0.0.1:8000/
```

### 3. Ouvrir l'application

```
http://127.0.0.1:8000/drive/
```

### 4. Créer des données (optionnel)

1. Allez à **Admin** (http://127.0.0.1:8000/admin/)
2. Créez des produits, clients, catégories
3. Allez à **Commandes**
4. Créez une commande
5. Testez l'**autocomplete** ✨

---

## 📚 Documentation complète

- **INSTALL.md** - Installation détaillée
- **FEATURES.md** - Fonctionnalités
- **TEST_AUTOCOMPLETE.md** - Tester l'autocomplete
- **TROUBLESHOOTING.md** - Dépannage
- **SUMMARY.md** - Résumé des modifications

---

## 🎯 Fonctionnalités principales

### 🔥 Autocomplete Produits (NEW!)

**Où:** Commandes → Ajouter un produit → Rechercher un produit

**Comment:**
1. Tapez le nom d'un produit
2. Les suggestions apparaissent
3. Cliquez pour sélectionner
4. Entrez la quantité
5. Cliquez "Ajouter" ✅

### 📖 Gestion complète CRUD

- **Catégories** - Créer, Lister, Modifier, Supprimer
- **Produits** - Créer, Lister, Modifier, Supprimer
- **Clients** - Créer, Lister, Voir, Modifier, Supprimer
- **Commandes** - Créer, Lister, Détails, Ajouter produits, Gérer quantités

---

## 🎨 URLs principales

| Page | URL |
|------|-----|
| Accueil | `/drive/` |
| Catégories | `/drive/categories/` |
| Produits | `/drive/produits/` |
| Clients | `/drive/clients/` |
| Commandes | `/drive/commandes/` |
| Admin | `/admin/` |
| API Autocomplete | `/drive/api/produits/search/?q=terme` |

---

## 💻 Commandes utiles

### Démarrer le serveur
```bash
python manage.py runserver
```

### Arrêter le serveur
```bash
Ctrl + C
```

### Vérifier la configuration
```bash
python manage.py check
```

### Exécuter les migrations
```bash
python manage.py migrate
```

### Créer un utilisateur admin
```bash
python manage.py createsuperuser
```

### Accéder à la base de données
```bash
python manage.py dbshell
```

---

## 🧪 Tester l'API Autocomplete

### Depuis le terminal

```bash
# Terminal 1: Démarrer le serveur
python manage.py runserver

# Terminal 2: Tester l'API
curl "http://127.0.0.1:8000/drive/api/produits/search/?q=pom"
```

### Depuis le navigateur

```
http://127.0.0.1:8000/drive/api/produits/search/?q=pommes
```

Vous devriez voir le JSON:
```json
{
  "produits": [
    {
      "id": 1,
      "nom": "Pommes",
      "prix": 2.5,
      "categorie": "Fruits",
      "marque": "Local"
    }
  ]
}
```

---

## 🐛 Debugging

### Voir les logs du serveur

Les messages d'erreur s'affichent dans le terminal où vous avez lancé `runserver`.

**Exemple:**
```
[30/May/2026 10:30:45] "GET /drive/produits/ HTTP/1.1" 200 5234
[30/May/2026 10:30:46] "GET /drive/api/produits/search/?q=pom HTTP/1.1" 200 456
```

### Voir les logs JavaScript

1. Ouvrir F12 dans le navigateur
2. Allez à l'onglet **Console**
3. Tapez dans le champ de recherche
4. Vous devriez voir:

```javascript
✅ Autocomplete activé
API URL: /drive/api/produits/search/
🔍 Recherche: p
📡 Requête API: /drive/api/produits/search/?q=p
📦 Résultats API: 3
✅ Produit sélectionné: Pommes
```

---

## 🚨 Erreurs courantes

### "Address already in use"
```bash
python manage.py runserver 8001
```

### "No module named 'django'"
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### L'autocomplete ne fonctionne pas
- Voir **TROUBLESHOOTING.md**

---

## 📁 Structure du projet

```
SAE203/
├── manage.py                    # Commandes Django
├── requirements.txt             # Dépendances
├── db.sqlite3                   # Base de données
├── drive/
│   ├── models.py               # Modèles
│   ├── views.py                # Vues (+ API)
│   ├── urls.py                 # Routes
│   ├── admin.py                # Admin Django
│   ├── static/
│   │   └── drive/
│   │       ├── style.css       # Styles
│   │       └── autocomplete.js # Autocomplete
│   └── templates/
│       └── drive/
│           ├── base.html
│           ├── commande_detail.html (autocomplete ici!)
│           └── ... (autres templates)
└── project/
    ├── settings.py
    ├── urls.py
    └── wsgi.py
```

---

## ✨ Résumé des améliorations

- ✅ Code simplifié (-49% de lignes)
- ✅ Autocomplete pour les produits 🔥
- ✅ Responsive design
- ✅ API REST pour la recherche
- ✅ Documentation complète
- ✅ Debugging facile

---

## 🎓 Apprendre plus

- Django: https://docs.djangoproject.com/
- JavaScript Fetch: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API
- CSS Variables: https://developer.mozilla.org/en-US/docs/Web/CSS/--*

---

**Prêt à démarrer?** 🚀

```bash
source venv/bin/activate  # macOS/Linux
python manage.py runserver
# Ouvrir http://127.0.0.1:8000/drive/
```

Bon développement! 😊

