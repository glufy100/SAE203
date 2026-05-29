# 🔧 Troubleshooting - Problèmes Courants

## 🎯 Autocomplete

### ❓ L'autocomplete n'affiche rien

**Symptôme:** 
- Je tape dans le champ de recherche mais aucune suggestion n'apparaît

**Causes possibles:**

1. **Pas de produits en base de données**
   - Solution: Allez à **Produits** et créez des produits
   - Vérifiez qu'ils sont bien enregistrés

2. **L'API retourne une erreur**
   - Ouvrez la console (F12)
   - Regardez les logs
   - Si vous voyez "❌ Erreur API: HTTP 404":
     - Vérifiez que `/drive/api/produits/search/` existe
     - Vérifiez dans `drive/urls.py`

3. **Erreur JavaScript**
   - Ouvrez F12 → Console
   - Vérifiez qu'il n'y a pas d'erreurs rouges
   - Vérifiez que le script est bien chargé

**Fix complet:**

```
1. Ouvrir F12
2. Console → Voir les erreurs
3. Taper dans le champ
4. Noter les messages de log
5. Si erreur API 404:
   - Vérifier que le endpoint existe
   - Redémarrer le serveur Django
```

---

### ❓ L'autocomplete affiche mais la sélection ne marche pas

**Symptôme:**
- Les suggestions apparaissent
- Mais cliquer sur une suggestion ne la sélectionne pas

**Causes:**

1. **Le select #produit_id n'existe pas**
   - Vérifiez le template `commande_detail.html`
   - S'assurer que `<select id="produit_id" name="produit_id">` existe

2. **Erreur JavaScript au clic**
   - Un script cesse l'exécution
   - Vérifiez F12 → Console pour les erreurs

**Fix:**

```html
<!-- Vérifiez que ce code existe dans commande_detail.html -->
<select id="produit_id" name="produit_id" required style="display: none;">
    <option value="">-- Sélectionnez un produit --</option>
    {% for produit in produits %}
    <option value="{{ produit.id }}">{{ produit.nom }}</option>
    {% endfor %}
</select>
```

---

### ❓ L'autocomplete est très lent

**Symptôme:**
- Il y a un gros délai avant que les suggestions n'apparaissent

**Causes:**

1. **Trop de produits**
   - L'API recherche dans tous les produits
   - Solution: L'API limite à 10 résultats

2. **Réseau lent**
   - Normal en développement local
   - Solution: Attendre

3. **Serveur Django surchargé**
   - Close les autres onglets/applications

**Fix:**

```javascript
// Dans commande_detail.html, ligne ~153:
// Augmentez le délai de debounce si trop de requêtes
}, 300);  // 300ms = attendre 300 millisecondes avant chercher
```

---

## 🚀 Serveur Django

### ❓ "Address already in use"

**Problème:** Le port 8000 est déjà utilisé

**Solution 1:** Utiliser un autre port
```bash
python manage.py runserver 8001
```

**Solution 2:** Tuer le processus existant
```bash
# Sur macOS/Linux:
lsof -ti:8000 | xargs kill -9

# Sur Windows (PowerShell):
Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess | Stop-Process
```

---

### ❓ "No module named 'django'"

**Problème:** Django n'est pas installé

**Solution:**
```bash
# 1. S'assurer que le venv est activé
source venv/bin/activate  # macOS/Linux
# ou
venv\Scripts\activate     # Windows

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Vérifier
python -c "import django; print(django.VERSION)"
```

---

### ❓ "ModuleNotFoundError: No module named 'drive'"

**Problème:** Le projet n'est pas bien configuré

**Solution:**
```bash
# Vérifier que vous êtes dans le bon répertoire
cd /Users/louis/Documents/IUT/SAE203

# Vérifier la structure
ls drive/
# Doit afficher: __init__.py, models.py, views.py, urls.py, etc.

# Vérifier settings.py
grep -n "INSTALLED_APPS" project/settings.py
# Doit contenir 'drive'
```

---

## 🗄️ Base de Données

### ❓ "database is locked"

**Problème:** Vous avez plusieurs instances qui accèdent à la BDD

**Solution:**
```bash
# 1. Arrêter le serveur (Ctrl+C)
# 2. Attendre quelques secondes
# 3. Relancer le serveur
python manage.py runserver
```

---

### ❓ "No such table: drive_produit"

**Problème:** Les migrations n'ont pas été exécutées

**Solution:**
```bash
python manage.py migrate
```

---

## 🌐 Interface Web

### ❓ "Page not found" (404)

**Problème:** Une route n'existe pas

**Symptômes:**

```
Page not found (404)
Request Method: GET
Request URL: http://127.0.0.1:8000/something
```

**Solution:**

1. Vérifier l'URL
2. Vérifier qu'elle existe dans `drive/urls.py`
3. Vérifier que le nome est correct

**Exemple:**

Si vous voyez:
```
Request URL: http://127.0.0.1:8000/produits/
```

Vérifier dans `urls.py`:
```python
path('produits/', views.produit_list, name='produit_list'),
```

---

### ❓ "Disallowed Host"

**Problème:** L'URL accédée n'est pas autorisée

**Solution:** Dans `project/settings.py`, modifier:
```python
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '*']  # '*' = tout autoriser (dev seulement!)
```

---

## 👨‍💻 JavaScript/Frontend

### ❓ Les styles CSS ne s'appliquent pas

**Problème:** Les couleurs et layouts ne sont pas visibles

**Solution:**

```bash
# Recueillir les fichiers statiques
python manage.py collectstatic

# Et/ou vider le cache du navigateur
# F12 → Vider cache, rechargez la page
```

---

### ❓ Le formulaire ne soumet pas

**Problème:** Le bouton "Ajouter" ne fait rien

**Causes:**

1. **Validation HTML**
   - Les champs `required` ne sont pas remplis
   - Solution: Remplissez tous les champs

2. **JavaScript bloque la soumission**
   - `event.preventDefault()` empêche la soumission
   - Vérifiez le script

3. **CSRF token manquant**
   - Template doit avoir: `{% csrf_token %}`
   - Vérifiez `commande_detail.html` ligne ~50

**Fix:**

```html
<!-- Dans chaque formulaire POST -->
<form method="POST">
    {% csrf_token %}
    <!-- Champs du formulaire -->
</form>
```

---

## 📝 Logs et Debugging

### Voir les logs du serveur

```bash
# Terminal où le serveur Django tourne:
# Les messages s'affichent en temps réel
```

Exemple de logs utiles:
```
[30/May/2026 10:30:45] "GET /drive/produits/ HTTP/1.1" 200 5234
│                                                          │
│                                                          └─ 200 = OK
│                                                             404 = Not Found
│                                                             500 = Erreur serveur

[30/May/2026 10:30:46] "GET /drive/api/produits/search/?q=pom HTTP/1.1" 200 456
```

### Voir les logs JavaScript

Ouvrir F12 dans le navigateur → Onglet **Console**:

```javascript
console.log('Message de debug')
console.error('Message d\'erreur')
console.warn('Avertissement')
```

---

## 🧪 Tester en ligne de commande

### Tester l'API directement

```bash
# Depuis le serveur Django en train de tourner, dans un autre terminal:
curl "http://127.0.0.1:8000/drive/api/produits/search/?q=pom"
```

Résultat attendu:
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

## 🆘 Si rien ne fonctionne

1. **Arrêtez le serveur** (Ctrl+C)
2. **Vérifiez l'environnement**
   ```bash
   source venv/bin/activate
   python manage.py check
   ```
3. **Regardez les erreurs** affichées
4. **Redémarrez le serveur**
   ```bash
   python manage.py runserver
   ```
5. **Ouvrez F12** dans le navigateur
6. **Onglet Console** pour voir les erreurs JavaScript
7. **Terminal** pour voir les erreurs Django

---

**Toujours démarrer par regarder les logs!** 📊

Bon debugging! 🐛

