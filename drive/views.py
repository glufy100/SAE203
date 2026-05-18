from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Categorie, Produit, Client, Commande, LigneCommande


# ════════════════════════════════════════════════════════════════════════════
# 🧩 VIEWS — CATÉGORIES
# ════════════════════════════════════════════════════════════════════════════

def categorie_list(request):
    """Affiche la liste de toutes les catégories"""
    categories = Categorie.objects.all()
    return render(request, 'drive/categorie_list.html', {'categories': categories})


def categorie_create(request):
    """Crée une nouvelle catégorie"""
    if request.method == 'POST':
        nom = request.POST.get('nom')
        descriptif = request.POST.get('descriptif')
        
        if nom:
            Categorie.objects.create(nom=nom, descriptif=descriptif)
            messages.success(request, 'Catégorie créée avec succès!')
            return redirect('categorie_list')
        else:
            messages.error(request, 'Le nom est obligatoire!')
    
    return render(request, 'drive/categorie_form.html')


def categorie_update(request, id):
    """Met à jour une catégorie"""
    categorie = get_object_or_404(Categorie, id=id)
    
    if request.method == 'POST':
        categorie.nom = request.POST.get('nom', categorie.nom)
        categorie.descriptif = request.POST.get('descriptif', categorie.descriptif)
        categorie.save()
        messages.success(request, 'Catégorie mise à jour!')
        return redirect('categorie_list')
    
    return render(request, 'drive/categorie_form.html', {'categorie': categorie})


def categorie_delete(request, id):
    """Supprime une catégorie"""
    categorie = get_object_or_404(Categorie, id=id)
    
    if request.method == 'POST':
        categorie.delete()
        messages.success(request, 'Catégorie supprimée!')
        return redirect('categorie_list')
    
    return render(request, 'drive/categorie_confirm_delete.html', {'categorie': categorie})


# ════════════════════════════════════════════════════════════════════════════
# 📦 VIEWS — PRODUITS
# ════════════════════════════════════════════════════════════════════════════

def produit_list(request):
    """Affiche la liste de tous les produits"""
    produits = Produit.objects.select_related('categorie').all()
    return render(request, 'drive/produit_list.html', {'produits': produits})


def produit_create(request):
    """Crée un nouveau produit"""
    if request.method == 'POST':
        nom = request.POST.get('nom')
        categorie_id = request.POST.get('categorie_id')
        prix = request.POST.get('prix')
        
        if nom and categorie_id and prix:
            Produit.objects.create(
                nom=nom,
                date_peremption=request.POST.get('date_peremption') or None,
                photo=request.POST.get('photo') or None,
                marque=request.POST.get('marque') or None,
                prix=prix,
                categorie_id=categorie_id
            )
            messages.success(request, 'Produit créé avec succès!')
            return redirect('produit_list')
        else:
            messages.error(request, 'Remplissez tous les champs obligatoires!')
    
    categories = Categorie.objects.all()
    return render(request, 'drive/produit_form.html', {'categories': categories})


def produit_update(request, id):
    """Met à jour un produit"""
    produit = get_object_or_404(Produit, id=id)
    
    if request.method == 'POST':
        produit.nom = request.POST.get('nom', produit.nom)
        produit.marque = request.POST.get('marque', produit.marque)
        produit.prix = request.POST.get('prix', produit.prix)
        produit.date_peremption = request.POST.get('date_peremption') or produit.date_peremption
        produit.photo = request.POST.get('photo') or produit.photo
        categorie_id = request.POST.get('categorie_id')
        if categorie_id:
            produit.categorie_id = categorie_id
        produit.save()
        messages.success(request, 'Produit mis à jour!')
        return redirect('produit_list')
    
    categories = Categorie.objects.all()
    return render(request, 'drive/produit_form.html', {'produit': produit, 'categories': categories})


def produit_delete(request, id):
    """Supprime un produit"""
    produit = get_object_or_404(Produit, id=id)
    
    if request.method == 'POST':
        produit.delete()
        messages.success(request, 'Produit supprimé!')
        return redirect('produit_list')
    
    return render(request, 'drive/produit_confirm_delete.html', {'produit': produit})


# ════════════════════════════════════════════════════════════════════════════
# 👤 VIEWS — CLIENTS
# ════════════════════════════════════════════════════════════════════════════

def client_list(request):
    """Affiche la liste de tous les clients"""
    clients = Client.objects.all()
    return render(request, 'drive/client_list.html', {'clients': clients})


def client_detail(request, numero_client):
    """Affiche les détails d'un client et toutes ses commandes"""
    client = get_object_or_404(Client, numero_client=numero_client)
    commandes = Commande.objects.filter(client=client).prefetch_related('lignecommande_set__produit')
    
    # Calculer le montant total pour chaque commande
    commandes_avec_totaux = []
    for commande in commandes:
        lignes = commande.lignecommande_set.all()
        total = sum(ligne.produit.prix * ligne.quantite for ligne in lignes)
        commandes_avec_totaux.append({
            'commande': commande,
            'lignes': lignes,
            'total': total
        })
    
    return render(request, 'drive/client_detail.html', {
        'client': client,
        'commandes_avec_totaux': commandes_avec_totaux
    })


def client_create(request):
    """Crée un nouveau client"""
    if request.method == 'POST':
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        date_inscription = request.POST.get('date_inscription')
        adresse = request.POST.get('adresse')
        
        if nom and prenom and date_inscription and adresse:
            Client.objects.create(
                nom=nom,
                prenom=prenom,
                date_inscription=date_inscription,
                adresse=adresse
            )
            messages.success(request, 'Client créé avec succès!')
            return redirect('client_list')
        else:
            messages.error(request, 'Remplissez tous les champs!')
    
    return render(request, 'drive/client_form.html')


def client_update(request, numero_client):
    """Met à jour un client"""
    client = get_object_or_404(Client, numero_client=numero_client)
    
    if request.method == 'POST':
        client.nom = request.POST.get('nom', client.nom)
        client.prenom = request.POST.get('prenom', client.prenom)
        client.date_inscription = request.POST.get('date_inscription', client.date_inscription)
        client.adresse = request.POST.get('adresse', client.adresse)
        client.save()
        messages.success(request, 'Client mis à jour!')
        return redirect('client_list')
    
    return render(request, 'drive/client_form.html', {'client': client})


def client_delete(request, numero_client):
    """Supprime un client"""
    client = get_object_or_404(Client, numero_client=numero_client)
    
    if request.method == 'POST':
        client.delete()
        messages.success(request, 'Client supprimé!')
        return redirect('client_list')
    
    return render(request, 'drive/client_confirm_delete.html', {'client': client})


# ════════════════════════════════════════════════════════════════════════════
# 🧾 VIEWS — COMMANDES
# ════════════════════════════════════════════════════════════════════════════

def commande_list(request):
    """Affiche la liste de toutes les commandes"""
    commandes = Commande.objects.select_related('client').all()
    return render(request, 'drive/commande_list.html', {'commandes': commandes})


def commande_create(request):
    """Crée une nouvelle commande"""
    if request.method == 'POST':
        client_id = request.POST.get('client_id')
        
        if client_id:
            commande = Commande.objects.create(client_id=client_id)
            messages.success(request, 'Commande créée!')
            return redirect('commande_detail', numero_commande=commande.numero_commande)
        else:
            messages.error(request, 'Sélectionnez un client!')
    
    clients = Client.objects.all()
    return render(request, 'drive/commande_form.html', {'clients': clients})


def commande_detail(request, numero_commande):
    """Affiche les détails d'une commande"""
    commande = get_object_or_404(Commande, numero_commande=numero_commande)
    lignes = LigneCommande.objects.filter(commande=commande).select_related('produit')
    produits = Produit.objects.all()
    
    total = sum(ligne.produit.prix * ligne.quantite for ligne in lignes)
    
    return render(request, 'drive/commande_detail.html', {
        'commande': commande,
        'lignes': lignes,
        'produits': produits,
        'total': total
    })


def commande_delete(request, numero_commande):
    """Supprime une commande"""
    commande = get_object_or_404(Commande, numero_commande=numero_commande)
    
    if request.method == 'POST':
        commande.delete()
        messages.success(request, 'Commande supprimée!')
        return redirect('commande_list')
    
    return render(request, 'drive/commande_confirm_delete.html', {'commande': commande})


# ════════════════════════════════════════════════════════════════════════════
# 🧮 GESTION DES PRODUITS — DANS LA COMMANDE
# ════════════════════════════════════════════════════════════════════════════

def commande_add_produit(request, numero_commande):
    """Ajoute un produit à une commande"""
    commande = get_object_or_404(Commande, numero_commande=numero_commande)
    
    if request.method == 'POST':
        produit_id = request.POST.get('produit_id')
        quantite = request.POST.get('quantite')
        
        if produit_id and quantite:
            LigneCommande.objects.create(
                commande=commande,
                produit_id=produit_id,
                quantite=quantite
            )
            messages.success(request, 'Produit ajouté à la commande.')
        else:
            messages.error(request, 'Remplissez tous les champs.')
    
    return redirect('commande_detail', numero_commande=numero_commande)


def commande_update_produit(request, numero_commande, ligne_id):
    """Met à jour la quantité d'un produit dans une commande"""
    commande = get_object_or_404(Commande, numero_commande=numero_commande)
    ligne = get_object_or_404(LigneCommande, id=ligne_id, commande=commande)
    
    if request.method == 'POST':
        quantite = request.POST.get('quantite')
        if quantite:
            ligne.quantite = quantite
            ligne.save()
            messages.success(request, 'Quantité mise à jour.')
        else:
            messages.error(request, 'Quantité invalide.')
    
    return redirect('commande_detail', numero_commande=numero_commande)


def commande_delete_produit(request, numero_commande, ligne_id):
    """Supprime un produit d'une commande"""
    commande = get_object_or_404(Commande, numero_commande=numero_commande)
    ligne = get_object_or_404(LigneCommande, id=ligne_id, commande=commande)
    
    if request.method == 'POST':
        ligne.delete()
        messages.success(request, 'Produit supprimé de la commande.')
    
    return redirect('commande_detail', numero_commande=numero_commande)


