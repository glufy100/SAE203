# 🧾 GUIDE CRUD — Django Drive

## Configuration

L'application Django est maintenant configurée avec les modèles et les vues CRUD pour la gestion de :
- **Catégories** 📂
- **Produits** 📦
- **Clients** 👤
- **Commandes** 🧾
- **Lignes de Commande** 🧮

---

## 🚀 Démarrage rapide

### 1️⃣ Activer l'environnement (déjà fait)
```bash
source venv/bin/activate
```

### 2️⃣ Créer un superuser (administrateur Django)
```bash
python manage.py createsuperuser
```
Remplissez les champs demandés (username, email, password).

### 3️⃣ Lancer le serveur de développement
```bash
python manage.py runserver
```

Le serveur sera accessible sur http://127.0.0.1:8000/

---

## 🌐 Accès aux interfaces

| URL | Description |
|-----|-------------|
| http://127.0.0.1:8000/admin/ | **Admin Django** (gérer les modèles) |
| http://127.0.0.1:8000/drive/categories/ | Liste des catégories |
| http://127.0.0.1:8000/drive/produits/ | Liste des produits |
| http://127.0.0.1:8000/drive/clients/ | Liste des clients |
| http://127.0.0.1:8000/drive/commandes/ | Liste des commandes |

---

## 📋 Opérations CRUD disponibles

### 🧩 CATÉGORIES
- **CREATE** : `/drive/categories/create/` → Créer une catégorie
- **READ** : `/drive/categories/` → Lister toutes les catégories
- **UPDATE** : `/drive/categories/<id>/edit/` → Modifier une catégorie
- **DELETE** : `/drive/categories/<id>/delete/` → Supprimer une catégorie

### 📦 PRODUITS
- **CREATE** : `/drive/produits/create/` → Créer un produit
- **READ** : `/drive/produits/` → Lister tous les produits
- **UPDATE** : `/drive/produits/<id>/edit/` → Modifier un produit
- **DELETE** : `/drive/produits/<id>/delete/` → Supprimer un produit

### 👤 CLIENTS
- **CREATE** : `/drive/clients/create/` → Créer un client
- **READ** : `/drive/clients/` → Lister tous les clients
- **UPDATE** : `/drive/clients/<numero_client>/edit/` → Modifier un client
- **DELETE** : `/drive/clients/<numero_client>/delete/` → Supprimer un client

### 🧾 COMMANDES
- **CREATE** : `/drive/commandes/create/` → Créer une commande
- **READ** : `/drive/commandes/` → Lister toutes les commandes
- **DETAIL** : `/drive/commandes/<numero_commande>/` → Voir les détails d'une commande
- **DELETE** : `/drive/commandes/<numero_commande>/delete/` → Supprimer une commande

### 🧮 LIGNES DE COMMANDE
- **CREATE** : `/drive/commandes/<numero_commande>/ajouter-produit/` → Ajouter un produit à une commande
- **UPDATE** : `/drive/lignes/<id>/edit/` → Modifier la quantité
- **DELETE** : `/drive/lignes/<id>/delete/` → Supprimer un produit d'une commande

---

## 🎯 Exemple d'utilisation

### Créer une commande complète :

1. **Créer une catégorie** (si nécessaire)
   - Aller sur `/drive/categories/create/`
   - Remplir le formulaire (Nom, Descriptif)

2. **Créer un produit**
   - Aller sur `/drive/produits/create/`
   - Sélectionner la catégorie
   - Remplir nom, prix, marque, etc.

3. **Créer un client**
   - Aller sur `/drive/clients/create/`
   - Remplir les informations (Nom, Prénom, Date, Adresse)

4. **Créer une commande**
   - Aller sur `/drive/commandes/create/`
   - Sélectionner le client
   - Cliquer sur "Créer la commande"

5. **Ajouter des produits à la commande**
   - Cliquer sur "Détails" de la commande
   - Cliquer sur "➕ Ajouter un produit"
   - Sélectionner un produit et la quantité
   - Valider

6. **Voir le montant total**
   - Les totaux de lignes et montant global s'affichent automatiquement

---

## 🐍 Accès via Python Shell

Pour tester les modèles directement :

```bash
python manage.py shell
```

```python
from drive.models import Categorie, Produit, Client, Commande, LigneCommande

# Créer une catégorie
cat = Categorie.objects.create(nom="Boissons", descriptif="Boissons fraîches")

# Lister toutes les catégories
Categorie.objects.all()

# Créer un produit
prod = Produit.objects.create(nom="Coca", prix=2.50, categorie=cat, marque="Coca Cola")

# Chercher un produit par prix
Produit.objects.filter(prix__gt=2.00)

# Lister les produits avec leur catégorie
Produit.objects.select_related('categorie')
```

---

## 📁 Structure des fichiers

```
drive/
├── templates/drive/          # Templates HTML
│   ├── base.html             # Template de base
│   ├── categorie_list.html
│   ├── categorie_form.html
│   ├── produit_list.html
│   ├── produit_form.html
│   ├── client_list.html
│   ├── client_form.html
│   ├── commande_list.html
│   ├── commande_detail.html
│   └── ligne_form.html
├── models.py                 # Modèles Django
├── views.py                  # Vues CRUD
├── urls.py                   # Routes
├── admin.py                  # Configuration Admin
└── ...
```

---

## ⚠️ Notes importantes

- **Sauvegardes** : Les données sont sauvegardées dans la base MySQL `drive`
- **Suppression** : Les suppressions en cascade sont activées (supprimer un client supprime ses commandes)
- **Permissions** : L'admin Django gère les permissions utilisateurs
- **Validation** : Les champs obligatoires sont validés à la création/modification

---

## 🆘 Dépannage

### Le serveur ne démarre pas ?
```bash
# Vérifier les migrations
python manage.py migrate

# Créer les migrations si nécessaire
python manage.py makemigrations
```

### Erreur de connexion MySQL ?
```bash
# Vérifier les paramètres dans project/settings.py
# DATABASE = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'drive',
#         'USER': 'root',
#         'PASSWORD': '',
#         'HOST': 'localhost',
#     }
# }
```

### Template non trouvé ?
```bash
# S'assurer que 'django.template.loaders.app_directories.Loader' est configuré
# et que le dossier templates/drive/ existe
```

---

✅ **C'est prêt !** Vous pouvez maintenant utiliser l'interface web pour gérer vos catégories, produits, clients et commandes.
