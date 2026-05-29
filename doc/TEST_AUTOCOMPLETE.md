# 🧪 Guide de Test - Autocomplete Produits

## ✅ Prérequis

1. **Avoir des produits** dans la base de données
   - Allez à **Produits** → créez au moins 5-10 produits
   - Exemple: Pommes, Tomates, Carottes, Bananes, Cerises, etc.

2. **Avoir une commande** (vide ou avec produits)
   - Allez à **Commandes** → créez une nouvelle commande
   - Sélectionnez un client

## 🚀 Comment tester l'autocomplete

### Étape 1: Aller à la page de détails de commande

```
Accueil → Commandes → Cliquer sur une commande → Section "Ajouter un produit"
```

### Étape 2: Tester la recherche

Dans le champ **"Rechercher un produit"**:

1. **Tapez lentement** le début du nom d'un produit
   - Exemple: Le"gu"me pour Légume
   - Les suggestions doivent apparaître immédiatement

2. **Cherchez plusieurs termes**
   - "Pom" → Pommes
   - "Ban" → Bananes
   - "Car" → Carottes

### Étape 3: Cliquer sur une suggestion

- Une liste déroulante apparaît avec les produits
- Chaque suggestion affiche:
  - 📦 **Nom du produit** (gras)
  - 📂 **Catégorie**
  - 💰 **Prix** en euros
  - 🏷️ **Marque** du produit

Exemple:
```
━━━━━━━━━━━━━━━━━━━━━━━
Pommes
Fruits • 2,50€ • Verger Local
━━━━━━━━━━━━━━━━━━━━━━━
Pommes Rouges
Fruits • 3,00€ • BioFresh
━━━━━━━━━━━━━━━━━━━━━━━
```

### Étape 4: Sélectionner un produit

- **Cliquez** sur une suggestion
- Le produit est sélectionné 
- Le champ de recherche se remplit avec le nom
- Le curseur passe automatiquement à "Quantité"

### Étape 5: Remplir la quantité et ajouter

1. Entrez la **quantité** désirée (ex: 2, 5, 10, etc.)
2. Cliquez sur **"Ajouter"**
3. Le produit s'ajoute à la commande ✅

## 🐛 Dépannage

### Si chezl'autocomplete ne fonctionne pas

**1. Vérifier la console du navigateur**

Ouvrez les **Outils du Développeur** (F12 ou Ctrl+Shift+I):
- Allez à l'onglet **"Console"**
- Tapez dans le champ de recherche
- Vous devriez voir des logs comme:
  ```
  ✅ Autocomplete activé
  API URL: /drive/api/produits/search/
  🔍 Recherche: p
  📡 Requête API: /drive/api/produits/search/?q=p
  📦 Résultats API: 3
  ✅ Produit sélectionné: Pommes
  ```

**2. Chercher "Erreur API"**

Si vous voyez:
```
❌ Erreur API: HTTP 404
```

Cela signifie que l'API ne trouve pas la route.

**Solutions:**
- Vérifier que l'URL est correcte dans le script
- S'assurer que `drive/urls.py` a la route `api_produits_search`
- Vérifier les logs du serveur Django

### Si aucune suggestion n'apparaît

1. **Vérifier qu'il y a des produits** en base de données
   - Allez à **Produits** et créez-en

2. **Taper au moins 1 caractère**
   - La recherche démarre avec 1+ caractères
   - Attendez 300ms pour voir les résultats

3. **Accès à la console**
   - Vérifiez s'il y a des erreurs JavaScript

### Si la sélection d'un produit ne fonctionne pas

1. **Vérifier le select caché**
   - Le select `#produit_id` doit être caché (display: none)
   - Il se remplit quand on sélectionne une suggestion

2. **Vérifier le formulaire POST**
   - S'assurer que `name="produit_id"` est présent dans le select

## 📊 Tester l'affichage

1. **Passer la souris** sur une suggestion
   - La couleur doit changer légèrement (hover effect)

2. **Cliquer ailleurs**
   - Les suggestions doivent disparaître

3. **Responsive**
   - Testez sur mobile/tablette
   - Les suggestions doivent rester visibles et cliquables

## ✨ Cas d'usage

### Cas 1: Ajouter plusieurs produits

```
Produit 1: Pommes (quantité: 3) → Ajouter
│ Produit ajouté ✅
│
Produit 2: Bananes (quantité: 2) → Ajouter
│ Produit ajouté ✅
│
Produit 3: Tomates (quantité: 5) → Ajouter
│ Produit ajouté ✅
```

### Cas 2: Chercher un produit qui n'existe pas

```
Taper: "XYZ"
│ Aucun produit trouvé ❌
```

### Cas 3: Chercher avec des majuscules

```
Taper: "POMMES" ou "pommes" ou "Pommes"
│ Les 3 doivent fonctionner (case-insensitive) ✅
```

---

## 📝 Notes

- La recherche est **case-insensitive** (Pommes = pommes = POMMES)
- Max **10 résultats** affichés pour chaque recherche
- **Debounce 300ms** pour éviter trop de requêtes API
- Le fetch utilise **GET** (pas de données sensibles en POST)

---

**Besoin d'aide ?** Regardez la console (F12) pour les logs de debug ! 🐛

