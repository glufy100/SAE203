import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from drive.models import Categorie, Produit, Client, Commande, LigneCommande
from datetime import datetime, timedelta

# Effacer les données existantes
print("🗑️ Suppression des données existantes...")
Categorie.objects.all().delete()
Produit.objects.all().delete()
Client.objects.all().delete()
Commande.objects.all().delete()
LigneCommande.objects.all().delete()

# ════════════════════════════════════════════════════════════════════════════
# CATÉGORIES
# ════════════════════════════════════════════════════════════════════════════

print("📂 Création de 10 catégories...")
categories_data = [
    ("Boissons", "Boissons fraiches et gazeuses"),
    ("Fruits", "Fruits frais et exotiques"),
    ("Légumes", "Légumes frais et de saison"),
    ("Produits laitiers", "Lait, fromage, yaourt"),
    ("Boulangerie", "Pain, pâtisserie, viennoiserie"),
    ("Viande", "Viande fraîche et charcuterie"),
    ("Poisson", "Poisson et fruits de mer"),
    ("Snacks", "Chips, biscuits, bonbons"),
    ("Surgelés", "Produits surgelés"),
    ("Produits bio", "Produits biologiques certifiés"),
]

categories = []
for nom, descriptif in categories_data:
    cat = Categorie.objects.create(nom=nom, descriptif=descriptif)
    categories.append(cat)
    print(f"  ✓ {nom}")

# ════════════════════════════════════════════════════════════════════════════
# PRODUITS
# ════════════════════════════════════════════════════════════════════════════

print("\n📦 Création de 10 produits...")
produits_data = [
    ("Coca-Cola 1.5L", datetime.now() + timedelta(days=365), "coca.jpg", "Coca-Cola", 2.50, categories[0]),
    ("Jus d'orange naturel", datetime.now() + timedelta(days=180), "jus.jpg", "Tropicana", 3.20, categories[0]),
    ("Pommes Golden", datetime.now() + timedelta(days=30), "pommes.jpg", "Vergers France", 1.99, categories[1]),
    ("Bananes équitables", datetime.now() + timedelta(days=15), "bananes.jpg", "Fair Trade", 2.10, categories[1]),
    ("Tomates cerises", datetime.now() + timedelta(days=10), "tomates.jpg", "Ferme Bio", 2.80, categories[2]),
    ("Carottes biologiques", datetime.now() + timedelta(days=20), "carottes.jpg", "Bio Valley", 1.50, categories[2]),
    ("Yaourt nature 125g", datetime.now() + timedelta(days=25), "yaourt.jpg", "Yoplait", 0.99, categories[3]),
    ("Fromage camembert", datetime.now() + timedelta(days=45), "camembert.jpg", "Normandie", 3.50, categories[3]),
    ("Pain complet 500g", datetime.now() + timedelta(days=5), "pain.jpg", "Boulangerie du coin", 2.20, categories[4]),
    ("Croissants x4", datetime.now() + timedelta(days=3), "croissants.jpg", "Artisan", 3.80, categories[4]),
]

produits = []
for nom, date, photo, marque, prix, categorie in produits_data:
    prod = Produit.objects.create(
        nom=nom,
        date_peremption=date,
        photo=photo,
        marque=marque,
        prix=prix,
        categorie=categorie
    )
    produits.append(prod)
    print(f"  ✓ {nom} ({prix}€)")

# ════════════════════════════════════════════════════════════════════════════
# CLIENTS
# ════════════════════════════════════════════════════════════════════════════

print("\n👤 Création de 10 clients...")
clients_data = [
    ("Dupont", "Jean", "2026-01-15", "12 rue des Fleurs, 68100 Mulhouse"),
    ("Martin", "Claire", "2026-02-20", "5 avenue de Colmar, 68100 Mulhouse"),
    ("Bernard", "Lucas", "2026-03-10", "8 rue des Vosges, 68000 Colmar"),
    ("Dubois", "Sophie", "2026-04-05", "42 place du Marché, 68300 Saint-Louis"),
    ("Lefebvre", "Marc", "2026-05-12", "15 chemin de la Forêt, 68200 Mulhouse"),
    ("Moreau", "Pauline", "2026-01-30", "33 rue de la Paix, 68100 Mulhouse"),
    ("Simon", "Thomas", "2026-02-14", "7 boulevard Clemenceau, 68000 Colmar"),
    ("Laurent", "Marie", "2026-03-25", "21 rue Victor Hugo, 68200 Mulhouse"),
    ("Michel", "Pierre", "2026-04-18", "100 avenue Foch, 68100 Mulhouse"),
    ("Garcia", "Anne", "2026-05-08", "50 rue Pasteur, 68300 Saint-Louis"),
]

clients = []
for nom, prenom, date, adresse in clients_data:
    client = Client.objects.create(
        nom=nom,
        prenom=prenom,
        date_inscription=date,
        adresse=adresse
    )
    clients.append(client)
    print(f"  ✓ {prenom} {nom}")

# ════════════════════════════════════════════════════════════════════════════
# COMMANDES
# ════════════════════════════════════════════════════════════════════════════

print("\n🧾 Création de 10 commandes...")
commandes = []
for i in range(10):
    client = clients[i % len(clients)]
    commande = Commande.objects.create(
        client=client,
        date_commande=datetime.now() - timedelta(days=10-i)
    )
    commandes.append(commande)
    print(f"  ✓ Commande #{commande.numero_commande} - {client.prenom} {client.nom}")

# ════════════════════════════════════════════════════════════════════════════
# LIGNES DE COMMANDE
# ════════════════════════════════════════════════════════════════════════════

print("\n🧮 Création de lignes de commande...")
# Pour chaque commande, ajouter 2-3 produits
import random

for commande in commandes:
    num_produits = random.randint(2, 4)
    produits_aleatoires = random.sample(produits, num_produits)
    
    for produit in produits_aleatoires:
        quantite = random.randint(1, 5)
        LigneCommande.objects.create(
            commande=commande,
            produit=produit,
            quantite=quantite
        )
        print(f"  ✓ Commande #{commande.numero_commande}: {produit.nom} x{quantite}")

# ════════════════════════════════════════════════════════════════════════════
# RÉSUMÉ
# ════════════════════════════════════════════════════════════════════════════

print("\n" + "="*70)
print("✅ BASE DE DONNÉES REMPLIE AVEC SUCCÈS!")
print("="*70)
print(f"📂 Catégories: {Categorie.objects.count()}")
print(f"📦 Produits: {Produit.objects.count()}")
print(f"👤 Clients: {Client.objects.count()}")
print(f"🧾 Commandes: {Commande.objects.count()}")
print(f"🧮 Lignes de commande: {LigneCommande.objects.count()}")
print("="*70)
