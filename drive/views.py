from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Categorie, Produit, Client, Commande, LigneCommande


def categorie_list(request):
    return render(request, 'drive/categorie/list.html', {'categories': Categorie.objects.all()})


def categorie_create(request):
    if request.method == 'POST':
        nom = request.POST.get('nom', '').strip()
        if nom:
            Categorie.objects.create(nom=nom, descriptif=request.POST.get('descriptif', ''))
            messages.success(request, 'Catégorie créée!')
            return redirect('categorie_list')
    return render(request, 'drive/categorie/form.html')


def categorie_update(request, id):
    categorie = get_object_or_404(Categorie, id=id)
    if request.method == 'POST':
        categorie.nom = request.POST.get('nom', categorie.nom)
        categorie.descriptif = request.POST.get('descriptif', categorie.descriptif)
        categorie.save()
        messages.success(request, 'Catégorie mise à jour!')
        return redirect('categorie_list')
    return render(request, 'drive/categorie/form.html', {'categorie': categorie})


def categorie_delete(request, id):
    categorie = get_object_or_404(Categorie, id=id)
    if request.method == 'POST':
        categorie.delete()
        messages.success(request, 'Catégorie supprimée!')
        return redirect('categorie_list')
    return render(request, 'drive/categorie/confirm_delete.html', {'categorie': categorie})


def produit_list(request):
    return render(request, 'drive/produit/list.html', {'produits': Produit.objects.select_related('categorie')})


def produit_create(request):
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
    produit = get_object_or_404(Produit, id=id)
    if request.method == 'POST':
        produit.delete()
        messages.success(request, 'Produit supprimé!')
        return redirect('produit_list')
    return render(request, 'drive/produit/confirm_delete.html', {'produit': produit})


def client_list(request):
    return render(request, 'drive/client/list.html', {'clients': Client.objects.all()})


def client_detail(request, numero_client):
    client = get_object_or_404(Client, numero_client=numero_client)
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
    client = get_object_or_404(Client, numero_client=numero_client)
    if request.method == 'POST':
        client.delete()
        messages.success(request, 'Client supprimé!')
        return redirect('client_list')
    return render(request, 'drive/client/confirm_delete.html', {'client': client})


def commande_list(request):
    return render(request, 'drive/commande/list.html', {'commandes': Commande.objects.select_related('client')})


def commande_create(request):
    if request.method == 'POST':
        client_id = request.POST.get('client_id')
        if client_id:
            commande = Commande.objects.create(client_id=client_id)
            messages.success(request, 'Commande créée!')
            return redirect('commande_detail', numero_commande=commande.numero_commande)
    return render(request, 'drive/commande/form.html', {'clients': Client.objects.all()})


def commande_detail(request, numero_commande):
    commande = get_object_or_404(Commande, numero_commande=numero_commande)
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
    commande = get_object_or_404(Commande, numero_commande=numero_commande)
    if request.method == 'POST':
        commande.delete()
        messages.success(request, 'Commande supprimée!')
        return redirect('commande_list')
    return render(request, 'drive/commande/confirm_delete.html', {'commande': commande})


def commande_add_produit(request, numero_commande):
    commande = get_object_or_404(Commande, numero_commande=numero_commande)
    if request.method == 'POST':
        produit_id = request.POST.get('produit_id')
        quantite = request.POST.get('quantite', 1)
        if produit_id:
            LigneCommande.objects.create(commande=commande, produit_id=produit_id, quantite=quantite)
            messages.success(request, 'Produit ajouté!')
    return redirect('commande_detail', numero_commande=numero_commande)


def commande_update_produit(request, numero_commande, ligne_id):
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
    commande = get_object_or_404(Commande, numero_commande=numero_commande)
    ligne = get_object_or_404(LigneCommande, id=ligne_id, commande=commande)
    if request.method == 'POST':
        ligne.delete()
        messages.success(request, 'Produit supprimé!')
    return redirect('commande_detail', numero_commande=numero_commande)



