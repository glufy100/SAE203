from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Categorie, Produit, Client, Commande, LigneCommande


# -----------------------------
# ACCUEIL
# -----------------------------
def home(request):
    """Afficher le tableau de bord principal de l'application.

    Entree:
    - request: requete HTTP entrante.

    Sortie:
    - HttpResponse rendant la page d'accueil du module Drive.
    """
    context = {
        'categories_count': Categorie.objects.count(),
        'produits_count': Produit.objects.count(),
        'clients_count': Client.objects.count(),
        'commandes_count': Commande.objects.count(),
    }
    return render(request, 'drive/home.html', context)


# -----------------------------
# API
# -----------------------------
def api_produits_search(request):
    """Rechercher des produits pour l'autocomplete des commandes.

    Entree:
    - request: requete HTTP contenant un parametre `q`.

    Sortie:
    - JsonResponse avec une liste de produits compatibles avec l'autocomplete.
    """
    query = request.GET.get('q', '').strip()
    produits = Produit.objects.select_related('categorie').all()

    if query:
        produits = produits.filter(
            Q(nom__icontains=query)
            | Q(marque__icontains=query)
            | Q(categorie__nom__icontains=query)
        )

    produits = produits.order_by('nom')[:10]

    return JsonResponse({
        'produits': [
            {
                'id': produit.id,
                'nom': produit.nom,
                'prix': str(produit.prix),
                'categorie': produit.categorie.nom,
                'marque': produit.marque or '-',
            }
            for produit in produits
        ]
    })


# -----------------------------
# CATEGORIES
# -----------------------------
def categorie_list(request):
    """Lister les categories.

    Entree:
    - request: requete HTTP entrante.

    Sortie:
    - HttpResponse rendant la page de liste des categories.
    """
    return render(request, 'drive/categorie/list.html', {'categories': Categorie.objects.all()})


def categorie_create(request):
    """Creer une categorie.

    Entree:
    - request: requete HTTP contenant potentiellement 'nom' et 'descriptif' en POST.

    Sortie:
    - render() du formulaire si GET ou si validation echoue.
    - redirect vers la liste des categories si la creation reussit.
    """
    if request.method == 'POST':
        nom = request.POST.get('nom', '').strip()
        if nom:
            Categorie.objects.create(nom=nom, descriptif=request.POST.get('descriptif', ''))
            messages.success(request, 'Catégorie créée!')
            return redirect('categorie_list')
    return render(request, 'drive/categorie/form.html')


def categorie_update(request, id):
    """Mettre a jour une categorie existante.

    Entree:
    - request: requete HTTP avec les nouvelles valeurs en POST.
    - id: identifiant de la categorie a modifier.

    Sortie:
    - render() du formulaire avec les donnees de la categorie en GET.
    - redirect vers la liste si la mise a jour est enregistree.
    """
    categorie = get_object_or_404(Categorie, id=id)
    if request.method == 'POST':
        categorie.nom = request.POST.get('nom', categorie.nom)
        categorie.descriptif = request.POST.get('descriptif', categorie.descriptif)
        categorie.save()
        messages.success(request, 'Catégorie mise à jour!')
        return redirect('categorie_list')
    return render(request, 'drive/categorie/form.html', {'categorie': categorie})


def categorie_delete(request, id):
    """Supprimer une categorie apres confirmation.

    Entree:
    - request: requete HTTP.
    - id: identifiant de la categorie a supprimer.

    Sortie:
    - render() de la page de confirmation en GET.
    - redirect vers la liste apres suppression en POST.
    """
    categorie = get_object_or_404(Categorie, id=id)
    if request.method == 'POST':
        categorie.delete()
        messages.success(request, 'Catégorie supprimée!')
        return redirect('categorie_list')
    return render(request, 'drive/categorie/confirm_delete.html', {'categorie': categorie})


# -----------------------------
# PRODUITS
# -----------------------------
def produit_list(request):
    """Lister les produits.

    Entree:
    - request: requete HTTP entrante.

    Sortie:
    - HttpResponse rendant la liste des produits avec leurs categories.
    """
    return render(request, 'drive/produit/list.html', {'produits': Produit.objects.select_related('categorie')})


def produit_create(request):
    """Creer un produit.

    Entree:
    - request: requete HTTP contenant les champs du produit en POST.

    Sortie:
    - render() du formulaire si GET ou si champs incomplets.
    - redirect vers la liste des produits si la creation reussit.
    """
    if request.method == 'POST':
        nom = request.POST.get('nom', '').strip()
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
            messages.success(request, 'Produit créé!')
            return redirect('produit_list')
    return render(request, 'drive/produit/form.html', {'categories': Categorie.objects.all()})


def produit_update(request, id):
    """Modifier un produit.

    Entree:
    - request: requete HTTP contenant les valeurs a mettre a jour.
    - id: identifiant du produit cible.

    Sortie:
    - render() du formulaire avec les donnees courantes si GET.
    - redirect vers la liste apres sauvegarde.
    """
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
    return render(request, 'drive/produit/form.html', {'produit': produit, 'categories': Categorie.objects.all()})


def produit_delete(request, id):
    """Supprimer un produit apres confirmation.

    Entree:
    - request: requete HTTP.
    - id: identifiant du produit a supprimer.

    Sortie:
    - render() de la confirmation en GET.
    - redirect vers la liste apres suppression en POST.
    """
    produit = get_object_or_404(Produit, id=id)
    if request.method == 'POST':
        produit.delete()
        messages.success(request, 'Produit supprimé!')
        return redirect('produit_list')
    return render(request, 'drive/produit/confirm_delete.html', {'produit': produit})


# -----------------------------
# CLIENTS
# -----------------------------
def client_list(request):
    """Lister les clients.

    Entree:
    - request: requete HTTP entrante.

    Sortie:
    - HttpResponse rendant la page de liste des clients.
    """
    return render(request, 'drive/client/list.html', {'clients': Client.objects.all()})


def client_detail(request, numero_client):
    """Afficher la fiche detaillee d'un client.

    Entree:
    - request: requete HTTP.
    - numero_client: identifiant metier du client a afficher.

    Sortie:
    - HttpResponse avec la fiche client, ses commandes et leurs totaux.
    """
    client = get_object_or_404(Client, numero_client=numero_client)
    # On charge toutes les commandes du client, puis les lignes et produits associes,
    # afin de construire une fiche detaillee sans multiplier les requetes SQL.
    commandes = Commande.objects.filter(client=client).prefetch_related('lignecommande_set__produit')
    return render(request, 'drive/client/detail.html', {
        'client': client,
        'commandes_avec_totaux': [
            {
                'commande': c,
                'lignes': c.lignecommande_set.all(),
                'total': sum(l.get_total() for l in c.lignecommande_set.all())
            } for c in commandes
        ]
    })


def client_create(request):
    """Creer un client.

    Entree:
    - request: requete HTTP contenant les champs du formulaire en POST.

    Sortie:
    - render() du formulaire si GET ou si les donnees sont invalides.
    - redirect vers la liste si la creation reussit.
    """
    if request.method == 'POST':
        nom = request.POST.get('nom', '').strip()
        prenom = request.POST.get('prenom', '').strip()
        date_inscription = request.POST.get('date_inscription')
        adresse = request.POST.get('adresse', '').strip()
        if all([nom, prenom, date_inscription, adresse]):
            Client.objects.create(nom=nom, prenom=prenom, date_inscription=date_inscription, adresse=adresse)
            messages.success(request, 'Client créé!')
            return redirect('client_list')
    return render(request, 'drive/client/form.html')


def client_update(request, numero_client):
    """Mettre a jour un client existant.

    Entree:
    - request: requete HTTP avec les valeurs modifiees.
    - numero_client: identifiant du client cible.

    Sortie:
    - render() du formulaire en GET.
    - redirect vers la liste apres sauvegarde.
    """
    client = get_object_or_404(Client, numero_client=numero_client)
    if request.method == 'POST':
        client.nom = request.POST.get('nom', client.nom)
        client.prenom = request.POST.get('prenom', client.prenom)
        client.date_inscription = request.POST.get('date_inscription', client.date_inscription)
        client.adresse = request.POST.get('adresse', client.adresse)
        client.save()
        messages.success(request, 'Client mis à jour!')
        return redirect('client_list')
    return render(request, 'drive/client/form.html', {'client': client})


def client_delete(request, numero_client):
    """Supprimer un client apres confirmation.

    Entree:
    - request: requete HTTP.
    - numero_client: identifiant du client a supprimer.

    Sortie:
    - render() de la confirmation en GET.
    - redirect vers la liste apres suppression en POST.
    """
    client = get_object_or_404(Client, numero_client=numero_client)
    if request.method == 'POST':
        client.delete()
        messages.success(request, 'Client supprimé!')
        return redirect('client_list')
    return render(request, 'drive/client/confirm_delete.html', {'client': client})


# -----------------------------
# COMMANDES
# -----------------------------
def commande_list(request):
    """Lister les commandes.

    Entree:
    - request: requete HTTP.

    Sortie:
    - HttpResponse rendant la liste des commandes avec les clients associes.
    """
    return render(request, 'drive/commande/list.html', {'commandes': Commande.objects.select_related('client')})


def commande_create(request):
    """Creer une commande vide rattachee a un client.

    Entree:
    - request: requete HTTP contenant 'client_id' en POST.

    Sortie:
    - render() du formulaire si GET ou si aucun client n'est selectionne.
    - redirect vers le detail de la commande creee si la creation reussit.
    """
    if request.method == 'POST':
        client_id = request.POST.get('client_id')
        if client_id:
            commande = Commande.objects.create(client_id=client_id)
            messages.success(request, 'Commande créée!')
            return redirect('commande_detail', numero_commande=commande.numero_commande)
    return render(request, 'drive/commande/form.html', {'clients': Client.objects.all()})


def commande_detail(request, numero_commande):
    """Afficher le detail d'une commande.

    Entree:
    - request: requete HTTP.
    - numero_commande: identifiant de la commande.

    Sortie:
    - HttpResponse avec la commande, ses lignes, le catalogue produit et le total.
    """
    commande = get_object_or_404(Commande, numero_commande=numero_commande)
    # Les lignes sont jointes avec les produits pour limiter les requetes supplementaires.
    lignes = LigneCommande.objects.filter(commande=commande).select_related('produit')
    total = sum(ligne.get_total() for ligne in lignes)
    context = {
        'commande': commande,
        'lignes': lignes,
        'produits': Produit.objects.all(),
        'total': total
    }
    return render(request, 'drive/commande/detail.html', context)


def commande_delete(request, numero_commande):
    """Supprimer une commande apres confirmation.

    Entree:
    - request: requete HTTP.
    - numero_commande: identifiant de la commande a supprimer.

    Sortie:
    - render() de la confirmation en GET.
    - redirect vers la liste des commandes en POST.
    """
    commande = get_object_or_404(Commande, numero_commande=numero_commande)
    if request.method == 'POST':
        commande.delete()
        messages.success(request, 'Commande supprimée!')
        return redirect('commande_list')
    return render(request, 'drive/commande/confirm_delete.html', {'commande': commande})


def commande_add_produit(request, numero_commande):
    """Ajouter une ligne a une commande.

    Entree:
    - request: requete HTTP contenant 'produit_id' et 'quantite' en POST.
    - numero_commande: identifiant de la commande cible.

    Sortie:
    - redirect vers le detail de la commande apres ajout.
    """
    commande = get_object_or_404(Commande, numero_commande=numero_commande)
    if request.method == 'POST':
        produit_id = request.POST.get('produit_id')
        quantite = request.POST.get('quantite', 1)
        if produit_id:
            LigneCommande.objects.create(commande=commande, produit_id=produit_id, quantite=quantite)
            messages.success(request, 'Produit ajouté!')
    return redirect('commande_detail', numero_commande=numero_commande)


def commande_update_produit(request, numero_commande, ligne_id):
    """Mettre a jour la quantite d'une ligne de commande.

    Entree:
    - request: requete HTTP contenant la nouvelle quantite en POST.
    - numero_commande: identifiant de la commande parente.
    - ligne_id: identifiant de la ligne a modifier.

    Sortie:
    - redirect vers le detail de la commande apres sauvegarde.
    """
    commande = get_object_or_404(Commande, numero_commande=numero_commande)
    ligne = get_object_or_404(LigneCommande, id=ligne_id, commande=commande)
    if request.method == 'POST':
        quantite = request.POST.get('quantite')
        if quantite and int(quantite) > 0:
            ligne.quantite = quantite
            ligne.save()
            messages.success(request, 'Quantité mise à jour!')
    return redirect('commande_detail', numero_commande=numero_commande)


def commande_delete_produit(request, numero_commande, ligne_id):
    """Supprimer une ligne de commande.

    Entree:
    - request: requete HTTP.
    - numero_commande: identifiant de la commande parente.
    - ligne_id: identifiant de la ligne a supprimer.

    Sortie:
    - redirect vers le detail de la commande apres suppression.
    """
    commande = get_object_or_404(Commande, numero_commande=numero_commande)
    ligne = get_object_or_404(LigneCommande, id=ligne_id, commande=commande)
    if request.method == 'POST':
        ligne.delete()
        messages.success(request, 'Produit supprimé!')
    return redirect('commande_detail', numero_commande=numero_commande)
