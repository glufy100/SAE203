# Explication complète du projet SAE203 — "Drive"

---

## 1. C'est quoi ce projet ?

C'est une **application web Django** qui simule la gestion d'un **drive de supermarché** (type Leclerc Drive, Carrefour Drive). Elle permet de gérer les catégories de produits, les produits, les clients, et leurs commandes. Le tout avec une vraie base de données, une interface web complète, et un déploiement sur deux machines virtuelles.

---

## 2. Les technologies utilisées

Fichier `requirements.txt` :

| Librairie | Version | Rôle |
|-----------|---------|------|
| **Django** | 5.2.14 | Framework web Python — le cœur du projet |
| **PyMySQL** | 1.1.3 | Connecteur Python → MariaDB/MySQL |
| **asgiref** | 3.11.1 | Dépendance interne Django (gestion async) |
| **sqlparse** | 0.5.5 | Dépendance interne Django (formatage SQL) |

Côté front : **HTML**, **CSS pur** (pas de Bootstrap), **JavaScript vanille** (pas de jQuery).

---

## 3. L'architecture du projet — deux dossiers principaux

```
SAE203/
├── project/          ← Configuration globale Django
│   ├── settings.py   ← Paramètres (base de données, apps installées...)
│   ├── urls.py       ← Routage principal
│   └── wsgi.py       ← Point d'entrée serveur web
│
└── drive/            ← L'application métier
    ├── models.py     ← Les 5 tables de la base de données
    ├── views.py      ← Toute la logique (21 fonctions)
    ├── urls.py       ← Les 17 URLs de l'app
    ├── admin.py      ← Interface d'administration Django
    ├── apps.py       ← Déclaration de l'app
    ├── migrations/   ← Historique des modifications de BDD
    ├── templates/    ← 14 fichiers HTML organisés par entité
    └── static/       ← CSS + JavaScript
```

Django suit le pattern **MVT (Model - View - Template)** :
- **Model** → les données en base
- **View** → la logique Python
- **Template** → la page HTML rendue

---

## 4. La base de données — models.py + database.sql

### Schéma relationnel complet

```
Categorie ←──(FK CASCADE)── Produit ←──(FK CASCADE)── LigneCommande ──(FK CASCADE)──→ Commande ──(FK CASCADE)──→ Client
```

### Table `categories`

```python
class Categorie(models.Model):
    nom        = CharField(max_length=100)
    descriptif = TextField(blank=True)
    # table SQL : "categories"
```

- Sert de **référentiel** pour classer les produits
- Exemples : "Fruits", "Boissons", "Surgelés"...

### Table `produits`

```python
class Produit(models.Model):
    nom             = CharField(max_length=150)
    date_peremption = DateField(null=True)         # optionnel
    photo           = CharField(max_length=255)    # nom du fichier image
    marque          = CharField(max_length=100)    # optionnel
    prix            = DecimalField(>= 0)
    categorie       = ForeignKey(Categorie, CASCADE)
```

- Le `prix` a un validateur `MinValueValidator(0)` — ne peut pas être négatif
- Clé étrangère vers `Categorie` : si on supprime une catégorie → **tous ses produits sont supprimés** (CASCADE)

### Table `clients`

```python
class Client(models.Model):
    numero_client    = AutoField(primary_key=True)  # clé primaire auto
    nom              = CharField(max_length=100)
    prenom           = CharField(max_length=100)
    date_inscription = DateField()
    adresse          = TextField()
```

### Table `commandes`

```python
class Commande(models.Model):
    numero_commande = AutoField(primary_key=True)
    client          = ForeignKey(Client, CASCADE)
    date_commande   = DateTimeField(auto_now_add=True)  # rempli AUTOMATIQUEMENT
```

- La date est remplie automatiquement à la création, impossible à modifier manuellement
- Si on supprime un client → toutes ses commandes disparaissent (CASCADE)

### Table `lignes_commande`

```python
class LigneCommande(models.Model):
    commande = ForeignKey(Commande, CASCADE)
    produit  = ForeignKey(Produit, CASCADE)
    quantite = IntegerField(>= 1)

    def get_total(self):
        return self.produit.prix * self.quantite
```

- C'est la **table de jonction** : elle fait le lien entre une commande et ses produits
- La méthode `get_total()` calcule le montant d'une ligne (prix × quantité)

### Requête SQL importante à connaître (dans database.sql)

```sql
-- Fiche complète d'une commande avec le total par ligne :
SELECT
    c.numero_commande,
    cl.nom, cl.prenom,
    p.nom AS produit,
    p.prix,
    lc.quantite,
    (p.prix * lc.quantite) AS total_ligne
FROM lignes_commande lc
JOIN commandes c ON lc.commande_id = c.numero_commande
JOIN clients cl ON c.client_id = cl.numero_client
JOIN produits p ON lc.produit_id = p.id
WHERE c.numero_commande = 1;
```

C'est exactement ce que fait la vue `commande_detail` côté Django.

---

## 5. La configuration — project/settings.py

### Point technique majeur : la bascule automatique MySQL / SQLite

Au démarrage, Django **teste la connexion réseau** à la VM MariaDB :

```python
def check_mysql_available():
    socket.create_connection(('10.128.207.87', 3306), timeout=2)
```

- **En salle de TP / salle de cours** → MySQL accessible → Django utilise **MariaDB** sur la VM 2
- **À la maison / hors réseau** → timeout → Django bascule automatiquement sur **SQLite local** (`db.sqlite3`)

Cela évite d'avoir deux fichiers de configuration séparés. Une seule base de code fonctionne dans les deux contextes.

### Apps installées

L'app `drive` est déclarée dans `INSTALLED_APPS` — Django la reconnaît comme une sous-application du projet.

### Sécurité CSRF

Le middleware `CsrfViewMiddleware` est actif — tous les formulaires POST incluent un token `{% csrf_token %}` pour éviter les attaques CSRF (Cross-Site Request Forgery).

---

## 6. Le routage — project/urls.py + drive/urls.py

### Routage principal

```python
# project/urls.py
path('admin/', admin.site.urls)          # interface admin Django
path('drive/', include('drive.urls'))    # délègue tout /drive/ à l'app
```

### Les 17 URLs de l'application

**Catégories (4 routes) :**

| URL | Vue | Description |
|-----|-----|-------------|
| `/drive/categories/` | `categorie_list` | Liste toutes les catégories |
| `/drive/categories/create/` | `categorie_create` | Formulaire de création |
| `/drive/categories/<id>/edit/` | `categorie_update` | Formulaire de modification |
| `/drive/categories/<id>/delete/` | `categorie_delete` | Page de confirmation de suppression |

**Produits (4 routes) :** même structure que catégories

**Clients (5 routes) :**

| URL | Vue | Description |
|-----|-----|-------------|
| `/drive/clients/` | `client_list` | Liste des clients |
| `/drive/clients/<id>/` | `client_detail` | Fiche détaillée + historique commandes |
| `/drive/clients/create/` | `client_create` | Création |
| `/drive/clients/<id>/edit/` | `client_update` | Modification |
| `/drive/clients/<id>/delete/` | `client_delete` | Suppression |

**Commandes (7 routes) :**

| URL | Vue | Description |
|-----|-----|-------------|
| `/drive/commandes/` | `commande_list` | Liste des commandes |
| `/drive/commandes/create/` | `commande_create` | Créer une commande vide |
| `/drive/commandes/<id>/` | `commande_detail` | Détail + ajout/modif/suppression de lignes |
| `/drive/commandes/<id>/delete/` | `commande_delete` | Supprimer la commande |
| `/drive/commandes/<id>/ajouter-produit/` | `commande_add_produit` | Ajouter une ligne |
| `/drive/commandes/<id>/produit/<ligne_id>/modifier/` | `commande_update_produit` | Modifier une quantité |
| `/drive/commandes/<id>/produit/<ligne_id>/supprimer/` | `commande_delete_produit` | Retirer une ligne |

---

## 7. La logique métier — drive/views.py

### Pattern GET/POST utilisé partout

Toutes les vues de création/modification/suppression suivent le même schéma :

```
Requête GET  →  affiche le formulaire (ou la page de confirmation)
Requête POST →  traite les données, puis redirige (pattern PRG)
```

Le **pattern PRG** (Post/Redirect/Get) évite la double soumission si on recharge la page après un POST.

### Vues simples (catégories, produits)

```python
def categorie_create(request):
    if request.method == 'POST':
        nom = request.POST.get('nom', '').strip()
        if nom:  # validation minimale
            Categorie.objects.create(nom=nom, descriptif=...)
            messages.success(request, 'Catégorie créée!')
            return redirect('categorie_list')
    return render(request, 'drive/categorie/form.html')
```

### Vue la plus complexe — client_detail

```python
def client_detail(request, numero_client):
    client = get_object_or_404(Client, numero_client=numero_client)
    commandes = Commande.objects.filter(client=client) \
                    .prefetch_related('lignecommande_set__produit')
    return render(request, 'drive/client/detail.html', {
        'client': client,
        'commandes_avec_totaux': [
            {
                'commande': c,
                'lignes': c.lignecommande_set.all(),
                'total': sum(l.get_total() for l in c.lignecommande_set.all())
            }
            for c in commandes
        ]
    })
```

- `prefetch_related` : Django précharge en une seule requête SQL toutes les lignes et leurs produits — évite le problème N+1 requêtes
- La liste `commandes_avec_totaux` est construite côté Python avec le total calculé pour chaque commande

### Vue commande_detail — la page centrale de gestion

Envoie au template :
- La commande
- Les lignes existantes (avec `select_related('produit')` pour ne pas faire une requête SQL par ligne)
- Tous les produits disponibles (pour le formulaire d'ajout)
- Le total général calculé

### get_object_or_404

Utilisé partout — si un ID n'existe pas en base, renvoie une page 404 propre au lieu de planter avec une erreur serveur.

### Messages flash

`messages.success(request, '...')` → Django stocke le message en session, le template `base.html` l'affiche au prochain chargement de page, puis le supprime automatiquement.

---

## 8. Les templates — drive/templates/drive/

### Organisation en dossiers

Les 14 templates HTML sont organisés par entité :

```
templates/drive/
├── base.html                    ← template parent commun
├── categorie/
│   ├── list.html                ← liste + boutons modifier/supprimer
│   ├── form.html                ← formulaire création ET modification (même fichier !)
│   └── confirm_delete.html
├── produit/
│   ├── list.html                ← tableau avec ID, nom, marque, prix, catégorie, péremption
│   ├── form.html
│   └── confirm_delete.html
├── client/
│   ├── list.html                ← tableau avec bouton "Détails" en plus
│   ├── detail.html              ← fiche client + historique de toutes ses commandes
│   ├── form.html
│   └── confirm_delete.html      ← avertit que les commandes seront aussi supprimées
└── commande/
    ├── list.html
    ├── detail.html              ← page la plus riche : lignes, total, formulaire ajout
    ├── form.html                ← simple : juste choisir un client
    └── confirm_delete.html
```

### Template parent base.html

Toutes les pages héritent de lui via `{% extends 'drive/base.html' %}` :
- Navigation sticky (fixée en haut lors du scroll) avec liens vers les 4 sections + Admin
- Zone d'affichage des messages flash
- Inclusion du CSS et du JS global
- Bloc `{% block content %}` que chaque page remplace avec son propre contenu

### Formulaire intelligent — création ET modification dans le même fichier

```html
<h1>{% if categorie %}Modifier la catégorie{% else %}Nouvelle catégorie{% endif %}</h1>
<input value="{% if categorie %}{{ categorie.nom }}{% endif %}">
```

Le même template gère les deux cas : si l'objet est passé en contexte → mode édition avec les valeurs pré-remplies, sinon → mode création avec champs vides.

### Page de suppression — message d'avertissement cascade

```html
<!-- client/confirm_delete.html -->
<p class="text-danger">
    Cette action est irréversible. Toutes ses commandes seront également supprimées.
</p>

<!-- commande/confirm_delete.html -->
<p class="text-danger">
    Cette action est irréversible. Tous les produits de cette commande seront également supprimés.
</p>
```

L'interface prévient l'utilisateur de l'effet CASCADE défini dans le modèle SQL.

---

## 9. Le style — drive/static/drive/style.css

### Système de variables CSS

```css
:root {
    --releve-principale: #2c3e50;   /* bleu foncé — nav, en-têtes tableau */
    --releve-secondaire: #3498db;   /* bleu clair — liens, accent */
    --accent: #27ae60;              /* vert — boutons succès */
    --fond: #f5f5f5;                /* gris clair — fond de page */
    --fond-clair: white;            /* blanc — cartes, tableaux */
}
```

### Composants CSS principaux

- **Navigation** : sticky (reste en haut lors du scroll), flex centré, transition hover sur les liens
- **Tableaux** : en-têtes bleu foncé, surlignage des lignes au hover, `border-collapse`
- **Boutons** : `.btn` (neutre bleu foncé), `.btn-success` (vert), `.btn-danger` (rouge)
- **Formulaires** : labels en gras, inputs full-width, textarea redimensionnable verticalement
- **Messages flash** : `.message.success` (fond vert clair) / `.message.error` (fond rouge clair) avec bordure gauche colorée
- **Cartes** : `.card` avec ombre légère, `.card-accent` avec bordure gauche bleue (utilisé dans la fiche client)
- **Total box** : `.total-box` aligné à droite, fond gris, pour afficher les montants des commandes
- **État vide** : `.empty` avec bordure pointillée et texte centré en gris
- **Formulaire inline** : `.inline-form` pour la modification de quantité directement dans le tableau des lignes
- **Autocomplete** : `.autocomplete-suggestions`, `.autocomplete-item`, `.autocomplete-item-empty`
- **Responsive** : `@media (max-width: 768px)` → boutons pleine largeur, nav réduite, padding réduit

---

## 10. L'autocomplete JavaScript — drive/static/drive/autocomplete.js

C'est la fonctionnalité la plus technique du projet.

### Fonctionnement étape par étape

1. L'utilisateur focus sur le champ de recherche → la boîte de suggestions est créée dans le DOM (lazy creation — seulement au premier focus)
2. L'utilisateur tape → **debounce 300ms** (si on retape dans les 300ms, le timer repart à zéro)
3. Après 300ms sans frappe → appel `fetch()` vers l'API : `/drive/api/produits/search/?q=texte`
4. L'API répond en JSON :

```json
{
  "produits": [
    {"id": 1, "nom": "Coca-Cola", "prix": "2.50", "categorie": "Boissons", "marque": "Coca-Cola"},
    ...
  ]
}
```

5. Les suggestions s'affichent sous le champ (nom en gras, catégorie + prix + marque en petit)
6. Clic sur une suggestion → le `<select>` caché est mis à jour avec l'ID du produit, le champ texte affiche le nom, le focus passe automatiquement au champ quantité
7. Clic ailleurs dans la page → suggestions masquées

### Pourquoi le debounce ?

Sans debounce, chaque touche enverrait une requête réseau. Si l'utilisateur tape "coca" rapidement, ça enverrait 4 requêtes (c, co, coc, coca). Avec 300ms de délai, seule la frappe finale déclenche la requête.

### Fonctions clés du script

| Fonction | Rôle |
|----------|------|
| `createSuggestionsBox()` | Crée le `<div>` de suggestions et l'attache au DOM |
| `hideSuggestions()` | Masque la boîte |
| `fetchProducts(query)` | Appel API via `fetch()`, gère les erreurs HTTP |
| `renderSuggestions(produits)` | Crée les items HTML cliquables |
| `selectProduct(produit)` | Met à jour le `<select>` + déplace le focus |
| `handleSearchInput()` | Gère le debounce de 300ms |
| `handleDocumentClick()` | Ferme la liste si clic en dehors du champ |

---

## 11. L'interface d'administration — drive/admin.py

Django génère un **back-office complet et automatique** sur `/admin/`. La configuration personnalise l'affichage :

```python
@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display  = ('id', 'nom', 'marque', 'prix', 'categorie', 'date_peremption')
    list_filter   = ('categorie', 'date_peremption')  # filtres latéraux
    search_fields = ('nom', 'marque')                 # barre de recherche
```

### Inline des lignes de commande

```python
class LigneCommandeInline(admin.TabularInline):
    model = LigneCommande
    extra = 1  # 1 ligne vide proposée par défaut
```

Quand on ouvre une commande dans l'admin, les lignes de commande sont **éditables directement dans le formulaire de la commande** — pas besoin d'aller dans un autre écran. C'est la fonctionnalité `inline` de Django Admin.

---

## 12. Le script de données — populate_db.py

Script autonome (pas une commande Django) à lancer une seule fois pour remplir la base avec des données réalistes :

```bash
python populate_db.py
```

**Ce qu'il crée :**
- **50 catégories** (Boissons, Fruits, Légumes, Viande, Poisson, Surgelés, Hygiène...)
- **50 produits** avec noms de marques réels (Coca-Cola, Tropicana, Barilla, Yoplait, Lindt...)
- **50 clients** avec des adresses réelles dans la région Mulhouse/Colmar/Saint-Louis
- **50 commandes** réparties sur les clients (1 par client en tournant)
- **Lignes de commande** : 2 à 4 produits par commande, quantités aléatoires (1 à 5)

Il commence toujours par **vider toute la base** avant de la remplir — permet de repartir d'un état propre connu.

---

## 13. L'infrastructure — 2 VM Debian

### Architecture complète

```
        Utilisateur (navigateur)
               │
               │ HTTP port 80
               ▼
┌──────────────────────────────────┐
│     VM 1 — Serveur Web           │
│                                  │
│  ┌─────────┐    ┌─────────────┐  │
│  │ Apache  │───►│   Django    │  │
│  │ port 80 │    │ port 8000   │  │
│  │ (proxy) │    │ (localhost) │  │
│  └─────────┘    └─────────────┘  │
│   /var/www/SAE203/               │
└──────────────────┬───────────────┘
                   │ MySQL port 3306
                   │ IP: 10.128.207.87
                   ▼
┌──────────────────────────────────┐
│     VM 2 — Base de données       │
│                                  │
│           MariaDB                │
│   Base: sae203 / User: django    │
└──────────────────────────────────┘
```

### Pourquoi Apache devant Django ?

- Apache écoute sur le port 80 (port standard HTTP) et fait du **reverse proxy** — il reçoit les requêtes des utilisateurs et les redirige vers Django sur `127.0.0.1:8000`
- Django n'est pas accessible directement de l'extérieur (lié uniquement sur `127.0.0.1`)
- Les fichiers statiques (CSS, JS) sont servis **directement par Apache** sans passer par Django, grâce à la directive `ProxyPass /static/ !` — c'est plus rapide et évite de surcharger Django

### Les scripts shell et leur ordre d'utilisation

**1. `verify-vm.sh`** — à lancer EN PREMIER sur une VM vierge

- Teste connexion internet, accès sudo, espace disque (>5GB), présence d'apt-get
- Si tous les tests passent → on peut lancer le suivant

**2. `init-vm.sh`** — initialisation complète (une seule fois)

- `apt-get install` : git, python3, pip, apache2, libapache2-mod-proxy-http
- `git clone` du repo GitHub dans `/var/www/SAE203`
- `pip3 install -r requirements.txt` (Django, PyMySQL...)
- `chown www-data:www-data` : donne les droits Apache sur le projet
- `chmod +x` sur tous les scripts

**3. `setup-apache.sh`** — configure Apache (une seule fois)

- Active les modules `proxy` et `proxy_http`
- Crée le fichier `/etc/apache2/sites-available/sae203.conf` avec le VirtualHost
- Désactive le site par défaut d'Apache, active le site SAE203
- Teste la config avec `apache2ctl configtest` avant de recharger

**4. `start-django.sh`** — à relancer après chaque redémarrage de la VM

- Tue les anciennes instances de Django (`pkill`)
- Applique les migrations (`python3 manage.py migrate`)
- Lance Django en arrière-plan : `nohup python3 manage.py runserver 127.0.0.1:8000 &`
- Les logs vont dans `/tmp/django.log`

**`deploy.sh`** — à chaque mise à jour du code

- `git reset --hard origin/main` (force la mise à jour depuis GitHub)
- Redémarre Apache

---

## 14. Le fichier database.sql — schéma SQL brut

En plus des modèles Django, le fichier `database.sql` contient le schéma SQL pur et des exemples de requêtes CRUD commentées. C'est la version SQL directe de ce que Django fait via l'ORM.

### Création des tables

```sql
CREATE TABLE categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    descriptif TEXT
);

CREATE TABLE produits (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(150) NOT NULL,
    date_peremption DATE,
    photo VARCHAR(255),
    marque VARCHAR(100),
    prix DECIMAL(10,2) NOT NULL,
    categorie_id INT NOT NULL,
    FOREIGN KEY (categorie_id) REFERENCES categories(id) ON DELETE CASCADE
);

CREATE TABLE clients (
    numero_client INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    date_inscription DATE NOT NULL,
    adresse TEXT NOT NULL
);

CREATE TABLE commandes (
    numero_commande INT AUTO_INCREMENT PRIMARY KEY,
    client_id INT NOT NULL,
    date_commande DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (client_id) REFERENCES clients(numero_client) ON DELETE CASCADE
);

CREATE TABLE lignes_commande (
    id INT AUTO_INCREMENT PRIMARY KEY,
    commande_id INT NOT NULL,
    produit_id INT NOT NULL,
    quantite INT NOT NULL,
    FOREIGN KEY (commande_id) REFERENCES commandes(numero_commande) ON DELETE CASCADE,
    FOREIGN KEY (produit_id) REFERENCES produits(id) ON DELETE CASCADE
);
```

### Requêtes avancées disponibles dans le fichier

```sql
-- Montant total par commande
SELECT c.numero_commande, cl.nom, cl.prenom,
       SUM(p.prix * lc.quantite) AS montant_total
FROM lignes_commande lc
JOIN commandes c ON lc.commande_id = c.numero_commande
JOIN clients cl ON c.client_id = cl.numero_client
JOIN produits p ON lc.produit_id = p.id
GROUP BY c.numero_commande, cl.nom, cl.prenom;

-- Produit le plus commandé
SELECT p.nom, SUM(lc.quantite) AS total_vendu
FROM lignes_commande lc
JOIN produits p ON lc.produit_id = p.id
GROUP BY p.nom
ORDER BY total_vendu DESC;

-- Clients avec nombre de commandes
SELECT cl.numero_client, cl.nom, cl.prenom,
       COUNT(c.numero_commande) AS nombre_commandes
FROM clients cl
LEFT JOIN commandes c ON cl.numero_client = c.client_id
GROUP BY cl.numero_client, cl.nom, cl.prenom;
```

---

## 15. Résumé "formule" pour l'oral

> **Ce projet est une application web Django de gestion de drive.** Elle est structurée autour de 5 modèles reliés par des clés étrangères en cascade : Catégorie → Produit → LigneCommande ↔ Commande → Client. L'application expose 17 URLs qui implémentent un CRUD complet sur chaque entité, avec une logique GET/POST dans les vues, des templates HTML qui héritent tous d'un `base.html` commun, et un autocomplete JavaScript sur la recherche de produits dans les commandes. Côté déploiement, elle tourne sur deux VM Debian : l'une avec Apache en reverse proxy devant Django, l'autre avec MariaDB — et la configuration bascule automatiquement sur SQLite si le serveur MySQL est injoignable.
