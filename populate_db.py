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

print("📂 Création de 50 catégories...")
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
    ("Épices", "Épices et herbes aromatiques"),
    ("Riz et Pâtes", "Riz, pâtes et céréales"),
    ("Huiles", "Huiles de cuisine"),
    ("Conserves", "Conserves et aliments en bocal"),
    ("Œufs", "Œufs frais"),
    ("Chocolat", "Chocolat et confiseries"),
    ("Café et Thé", "Café, thé et infusions"),
    ("Condiments", "Sauces et condiments"),
    ("Desserts", "Gâteaux et desserts"),
    ("Crèmes", "Crèmes et produits frais"),
    ("Jus", "Jus et boissons fruitées"),
    ("Eau", "Eau minérale et pétillante"),
    ("Bière", "Bière et boissons alcoolisées"),
    ("Vin", "Vin et alcools fins"),
    ("Produits surgelés viande", "Viande surgelée"),
    ("Produits surgelés poisson", "Poisson surgelé"),
    ("Produits surgelés légumes", "Légumes surgelés"),
    ("Produits surgelés fruits", "Fruits surgelés"),
    ("Produits diététiques", "Produits allégés et diététiques"),
    ("Nourriture pour animaux", "Aliments pour animaux domestiques"),
    ("Bébé", "Produits pour bébé"),
    ("Nettoyage", "Produits de nettoyage"),
    ("Hygiène", "Produits d'hygiène"),
    ("Papier", "Papier toilette et serviettes"),
    ("Savon", "Savons et savonnettes"),
    ("Shampoing", "Shampoing et après-shampoing"),
    ("Dentaire", "Produits dentaires"),
    ("Maquillage", "Cosmétiques et maquillage"),
    ("Santé", "Médicaments et santé"),
    ("Surgelé pizza", "Pizzas surgelées"),
    ("Surgelé frites", "Frites et produits à cuire"),
    ("Confiture", "Confitures et pâtes à tartiner"),
    ("Miel", "Miel et produits apicoles"),
    ("Fromage blanc", "Fromages blancs et frais"),
    ("Yaourt spécial", "Yaourts spécialisés"),
    ("Lait fermenté", "Produits laitiers fermentés"),
    ("Charcuterie", "Jambon et charcuterie fine"),
    ("Volaille", "Poulet et volaille"),
    ("Steak", "Steaks et viande rouge"),
    ("Côte", "Côtes et côtelettes"),
]

categories = []
for nom, descriptif in categories_data:
    cat = Categorie.objects.create(nom=nom, descriptif=descriptif)
    categories.append(cat)
    print(f"  ✓ {nom}")

# ════════════════════════════════════════════════════════════════════════════
# PRODUITS
# ════════════════════════════════════════════════════════════════════════════

print("\n📦 Création de 50 produits...")
produits_data = [
    ("Coca-Cola 1.5L", datetime.now() + timedelta(days=365), "coca.jpg", "Coca-Cola", 2.50, categories[0]),
    ("Jus d'orange naturel", datetime.now() + timedelta(days=180), "jus.jpg", "Tropicana", 3.20, categories[0]),
    ("Sprite 2L", datetime.now() + timedelta(days=300), "sprite.jpg", "Coca-Cola", 2.80, categories[0]),
    ("Fanta Fraise", datetime.now() + timedelta(days=250), "fanta.jpg", "Fanta", 2.30, categories[0]),
    ("Eau pétillante San Pellegrino", datetime.now() + timedelta(days=400), "san_p.jpg", "San Pellegrino", 4.50, categories[0]),
    ("Pommes Golden", datetime.now() + timedelta(days=30), "pommes.jpg", "Vergers France", 1.99, categories[1]),
    ("Bananes équitables", datetime.now() + timedelta(days=15), "bananes.jpg", "Fair Trade", 2.10, categories[1]),
    ("Oranges Valencia", datetime.now() + timedelta(days=20), "oranges.jpg", "Citrus", 1.50, categories[1]),
    ("Raisins blancs", datetime.now() + timedelta(days=12), "raisins.jpg", "Vigneron", 3.20, categories[1]),
    ("Fraises fraîches", datetime.now() + timedelta(days=8), "fraises.jpg", "Bio Fresh", 4.50, categories[1]),
    ("Tomates cerises", datetime.now() + timedelta(days=10), "tomates.jpg", "Ferme Bio", 2.80, categories[2]),
    ("Carottes biologiques", datetime.now() + timedelta(days=20), "carottes.jpg", "Bio Valley", 1.50, categories[2]),
    ("Laitue", datetime.now() + timedelta(days=8), "laitue.jpg", "Maraicher", 1.20, categories[2]),
    ("Courgettes", datetime.now() + timedelta(days=14), "courgettes.jpg", "Fermier", 1.80, categories[2]),
    ("Aubergines", datetime.now() + timedelta(days=12), "aubergines.jpg", "Bio", 2.20, categories[2]),
    ("Yaourt nature 125g", datetime.now() + timedelta(days=25), "yaourt.jpg", "Yoplait", 0.99, categories[3]),
    ("Fromage camembert", datetime.now() + timedelta(days=45), "camembert.jpg", "Normandie", 3.50, categories[3]),
    ("Lait entier 1L", datetime.now() + timedelta(days=12), "lait.jpg", "Lactel", 1.10, categories[3]),
    ("Fromage emmental", datetime.now() + timedelta(days=60), "emmental.jpg", "Jura", 5.20, categories[3]),
    ("Crème fraîche 200ml", datetime.now() + timedelta(days=15), "creme.jpg", "Président", 2.10, categories[3]),
    ("Pain complet 500g", datetime.now() + timedelta(days=5), "pain.jpg", "Boulangerie du coin", 2.20, categories[4]),
    ("Croissants x4", datetime.now() + timedelta(days=3), "croissants.jpg", "Artisan", 3.80, categories[4]),
    ("Baguette française", datetime.now() + timedelta(days=2), "baguette.jpg", "Au Fournil", 1.00, categories[4]),
    ("Pain de mie", datetime.now() + timedelta(days=7), "pain_mie.jpg", "Bonne Maman", 1.50, categories[4]),
    ("Pain aux céréales", datetime.now() + timedelta(days=6), "pain_cereales.jpg", "Bio Nature", 2.80, categories[4]),
    ("Poulet fermier", datetime.now() + timedelta(days=8), "poulet.jpg", "Loué", 9.50, categories[5]),
    ("Steak haché 500g", datetime.now() + timedelta(days=5), "steak_hache.jpg", "Label Rouge", 7.20, categories[5]),
    ("Jambon de Paris", datetime.now() + timedelta(days=15), "jambon.jpg", "Fleury Michon", 4.50, categories[5]),
    ("Saucisses de Strasbourg", datetime.now() + timedelta(days=10), "saucisses.jpg", "Fleury Michon", 3.80, categories[5]),
    ("Côte de porc", datetime.now() + timedelta(days=6), "cote_porc.jpg", "Breton", 8.50, categories[5]),
    ("Saumon frais", datetime.now() + timedelta(days=4), "saumon.jpg", "Atlantique", 12.50, categories[6]),
    ("Truite arc-en-ciel", datetime.now() + timedelta(days=5), "truite.jpg", "Aqua Premium", 10.20, categories[6]),
    ("Moules fraîches", datetime.now() + timedelta(days=3), "moules.jpg", "Bretagne", 6.80, categories[6]),
    ("Crevettes", datetime.now() + timedelta(days=4), "crevettes.jpg", "Import", 14.50, categories[6]),
    ("Dorade royale", datetime.now() + timedelta(days=3), "dorade.jpg", "Méditerranée", 11.90, categories[6]),
    ("Chips salt and vinegar", datetime.now() + timedelta(days=120), "chips.jpg", "Lay's", 1.50, categories[7]),
    ("Biscuits apéritif", datetime.now() + timedelta(days=150), "biscuits.jpg", "Belin", 2.20, categories[7]),
    ("Bonbons acidulés", datetime.now() + timedelta(days=200), "bonbons.jpg", "Lutti", 3.50, categories[7]),
    ("Chocolat noir 100g", datetime.now() + timedelta(days=180), "choco.jpg", "Lindt", 4.20, categories[7]),
    ("Chewing-gum", datetime.now() + timedelta(days=120), "chewing.jpg", "Mentos", 1.20, categories[7]),
    ("Pizza 4 fromages surgelée", datetime.now() + timedelta(days=180), "pizza.jpg", "Buitoni", 5.50, categories[8]),
    ("Frites croustillantes", datetime.now() + timedelta(days=200), "frites.jpg", "McCain", 3.20, categories[8]),
    ("Nuggets poulet", datetime.now() + timedelta(days=150), "nuggets.jpg", "Tyson", 4.80, categories[8]),
    ("Légumes mixtes surgelés", datetime.now() + timedelta(days=180), "legumes_surg.jpg", "Picard", 2.50, categories[8]),
    ("Fruits rouges surgelés", datetime.now() + timedelta(days=210), "fruits_surg.jpg", "Picard", 3.80, categories[8]),
    ("Café Lavazza 500g", datetime.now() + timedelta(days=365), "cafe.jpg", "Lavazza", 6.50, categories[9]),
    ("Thé noir Earl Grey", datetime.now() + timedelta(days=400), "the.jpg", "Twinings", 5.20, categories[9]),
    ("Pâtes Barilla", datetime.now() + timedelta(days=365), "pates.jpg", "Barilla", 1.20, categories[9]),
    ("Riz basmati 500g", datetime.now() + timedelta(days=365), "riz.jpg", "Ebly", 2.80, categories[9]),
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

print("\n👤 Création de 50 clients...")
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
    ("Leroy", "André", "2026-01-05", "9 rue de la République, 68100 Mulhouse"),
    ("Fournier", "Isabelle", "2026-02-11", "25 chemin des Bourgognes, 68000 Colmar"),
    ("Mercier", "Franck", "2026-03-22", "17 rue de l'Église, 68200 Mulhouse"),
    ("Vincent", "Nadine", "2026-04-30", "60 boulevard de la Liberté, 68300 Saint-Louis"),
    ("Beaumont", "Yves", "2026-05-19", "3 place Stanislas, 68100 Mulhouse"),
    ("Renard", "Catherine", "2026-01-25", "44 avenue des Alpes, 68000 Colmar"),
    ("Leclerc", "Jacques", "2026-02-03", "18 rue Saint-Michel, 68200 Mulhouse"),
    ("Richard", "Michèle", "2026-03-15", "31 rue de la Gare, 68100 Mulhouse"),
    ("Blanc", "Alain", "2026-04-08", "22 avenue de la Paix, 68300 Saint-Louis"),
    ("Petit", "Sylvie", "2026-05-27", "7 rue des Roses, 68000 Colmar"),
    ("Dumont", "Christophe", "2026-01-12", "55 boulevard Thierry, 68100 Mulhouse"),
    ("Renault", "Joëlle", "2026-02-09", "14 chemin de l'Étuve, 68200 Mulhouse"),
    ("Boucher", "Henri", "2026-03-18", "20 rue Pascal, 68300 Saint-Louis"),
    ("Caron", "Denise", "2026-04-26", "45 avenue Clemenceau, 68000 Colmar"),
    ("Gauthier", "Olivier", "2026-05-06", "11 rue du Val, 68100 Mulhouse"),
    ("Germain", "Viviane", "2026-01-20", "38 rue Jules Ferry, 68200 Mulhouse"),
    ("Gibbons", "Robert", "2026-02-16", "64 boulevard de Belgique, 68100 Mulhouse"),
    ("Gillet", "Muriel", "2026-03-27", "29 chemin de la Drève, 68000 Colmar"),
    ("Gilson", "Georges", "2026-04-14", "76 avenue Jean Jaurès, 68300 Saint-Louis"),
    ("Godot", "Monique", "2026-05-01", "6 rue Montaigne, 68200 Mulhouse"),
    ("Godin", "Bruno", "2026-01-08", "19 place Victor Hugo, 68100 Mulhouse"),
    ("Gondar", "Louise", "2026-02-28", "41 rue des Marronniers, 68000 Colmar"),
    ("Gontrand", "Patrice", "2026-03-07", "27 avenue du Rhin, 68200 Mulhouse"),
    ("Gony", "Rita", "2026-04-12", "52 rue de Turenne, 68300 Saint-Louis"),
    ("Gorju", "Serge", "2026-05-14", "10 boulevard de la Marne, 68100 Mulhouse"),
    ("Gormand", "Françoise", "2026-01-29", "35 rue Thiers, 68000 Colmar"),
    ("Gorriaux", "Michel", "2026-02-05", "23 avenue de Strasbourg, 68200 Mulhouse"),
    ("Gorsky", "Nicole", "2026-03-20", "48 chemin des Prairies, 68100 Mulhouse"),
    ("Goscinny", "Paul", "2026-04-09", "71 rue de la Liberté, 68300 Saint-Louis"),
    ("Gossart", "Valérie", "2026-05-23", "13 rue d'Austerlitz, 68000 Colmar"),
    ("Gosseau", "Hervé", "2026-01-17", "39 avenue d'Alsace, 68200 Mulhouse"),
    ("Gossert", "Andrée", "2026-02-24", "26 rue Beethoven, 68100 Mulhouse"),
    ("Gossler", "Raphaël", "2026-03-03", "49 boulevard Pasteur, 68300 Saint-Louis"),
    ("Gossot", "Fabienne", "2026-04-17", "15 rue Molière, 68000 Colmar"),
    ("Goteff", "Daniel", "2026-05-10", "32 avenue Ledru-Rollin, 68200 Mulhouse"),
    ("Gotfass", "Evelyne", "2026-01-22", "8 place du Commerce, 68100 Mulhouse"),
    ("Gothland", "Guillaume", "2026-02-19", "58 rue Saint-Exupéry, 68300 Saint-Louis"),
    ("Gothorix", "Christiane", "2026-03-29", "24 avenue Foch, 68000 Colmar"),
    ("Gotland", "Philippe", "2026-04-02", "43 rue des Acacias, 68200 Mulhouse"),
    ("Gottardo", "Marguerite", "2026-05-09", "30 boulevard Richard, 68100 Mulhouse"),
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

print("\n🧾 Création de 50 commandes...")
commandes = []
for i in range(50):
    client = clients[i % len(clients)]
    commande = Commande.objects.create(
        client=client,
        date_commande=datetime.now() - timedelta(days=50-i)
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
