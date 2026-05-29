# 🚀 Fonctionnalités - Projet Drive

## ✨ Autocomplete Produits (NEW!)

### 📍 Où ça fonctionne?
- **Commandes** → Ajouter un produit à une commande
- Recherche en temps réel avec suggestions

### 🎯 Comment ça marche?

#### 1. **Recherche par texte**
- Tapez une partie du nom du produit dans le champ de recherche
- Des suggestions apparaissent automatiquement 👇

#### 2. **Affichage des suggestions**
Chaque suggestion montre:
- **Nom du produit** (en gras)
- **Catégorie** du produit
- **Prix unitaire** (en euros)
- **Marque** du produit

Exemple:
```
Pommes
Fruits • 2.50€ • Local
```

#### 3. **Sélection rapide**
- Cliquez sur une suggestion
- Le produit est sélectionné automatiquement
- Le champ "Rechercher" se remplit avec le nom
- Le curseur passe à "Quantité" pour continuer

### ⚙️ API Utilisée

**Endpoint:** `GET /api/produits/search/?q=<query>`

**Paramètres:**
- `q` (string) : Terme de recherche (min 1 caractère)

**Réponse** (JSON):
```json
{
  "produits": [
    {
      "id": 1,
      "nom": "Pommes",
      "prix": 2.50,
      "categorie": "Fruits",
      "marque": "Local"
    },
    ...
  ]
}
```

### 🔧 Technologie

- **JavaScript vanille** (pas de dépendance externe)
- **Fetch API** pour les requêtes
- **Debounce** (300ms) pour optimiser les requêtes
- **CSS variables** pour le styling cohérent

### 📱 Responsive

- ✅ Compatible desktop, tablette, mobile
- ✅ Suggestions visibles et cliquables sur tous les écrans
- ✅ Optimisé pour les petits écrans

### 🔐 Sécurité

- ✅ Encodage URI des paramètres
- ✅ Validation serveur des requêtes
- ✅ Limite de 10 résultats max

---

## 📊 Architecture du Projet

### Fichiers modifiés

#### `drive/views.py`
- Ajout de l'import `JsonResponse`
- Nouvelle vue API: `api_produits_search()`
  - Recherche par terme (case-insensitive)
  - Retourne JSON avec détails produits

#### `drive/urls.py`
- Route API: `path('api/produits/search/', ...)`

#### `drive/templates/drive/commande_detail.html`
- Remplacement du select simple par:
  - Champ de recherche texte (`produit_search`)
  - Select caché (`produit_id`)
  - Script d'autocomplete intégré

#### `drive/static/drive/style.css`
- Styles pour les suggestions autocomplete
- Variables pour cohérence

#### `drive/templates/drive/base.html`
- Ajout du script `autocomplete.js`

### Nouveau fichier

#### `drive/static/drive/autocomplete.js`
- Logique réutilisable pour autocomplete
- Non utilisée actuellement (inline dans commande_detail.html)
- Peut être activée via le script du base.html

---

## 🎨 Styles Autocomplete

```css
/* Boîte de suggestions */
.autocomplete-suggestions { /* Container */ }
.autocomplete-item { /* Chaque suggestion */ }
.autocomplete-item:hover { /* Survol */ }
.autocomplete-item-empty { /* Pas de résultat */ }
```

Les couleurs utilisent les **CSS variables**:
- `--fond-clair` : Fond blanc
- `--gris-estompe` : Bordures
- `--releve-surlignage` : Survol

---

## 🚀 Utilisation

### Pour ajouter un produit à une commande:

1. Aller à **Commandes** → **Détails de la commande**
2. Section "Ajouter un produit" en bas
3. Taper le nom du produit dans le champ de recherche
4. Les suggestions apparaissent
5. Cliquer sur le produit souhaité
6. Entrer la quantité
7. Cliquer "Ajouter"

---

## 📝 Notes de développement

- La recherche est **insensible à la casse** (icontains)
- Limite à **10 résultats** pour performance
- **Debounce 300ms** pour réduire les requêtes réseau
- Peut être étendu à d'autres modèles (Clients, Catégories, etc.)

---

## 🔮 Améliorations futures

- [ ] Historique des recherches récentes
- [ ] Affichage du stock disponible
- [ ] Recommandations de produits
- [ ] Filtre par catégorie dans l'autocomplete
- [ ] Clavier (flèches haut/bas, Entrée)

