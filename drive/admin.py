from django.contrib import admin
from .models import Categorie, Produit, Client, Commande, LigneCommande


# L'admin sert ici de back-office pour consulter et corriger rapidement les donnees CRUD.
@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    """Vue admin des categories.

    Entree:
    - les objets Categorie fournis par Django.

    Sortie:
    - une interface de listing, recherche et edition dans /admin.
    """
    list_display = ('id', 'nom', 'descriptif')
    search_fields = ('nom',)


@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    """Vue admin des produits avec filtres par categorie et peremption."""
    list_display = ('id', 'nom', 'marque', 'prix', 'categorie', 'date_peremption')
    list_filter = ('categorie', 'date_peremption')
    search_fields = ('nom', 'marque')


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    """Vue admin des clients pour retrouver rapidement une fiche."""
    list_display = ('numero_client', 'nom', 'prenom', 'date_inscription')
    search_fields = ('nom', 'prenom')


# Affichage compact des lignes directement dans le formulaire de commande.
class LigneCommandeInline(admin.TabularInline):
    """Sous-formulaire inline pour ajouter ou modifier des lignes de commande.

    Entree:
    - une instance de Commande dans l'admin.

    Sortie:
    - un tableau inline permettant d'editer les lignes sans quitter la commande.
    """
    model = LigneCommande
    extra = 1
    fields = ('produit', 'quantite')


@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    """Vue admin des commandes avec edition inline des lignes."""
    list_display = ('numero_commande', 'client', 'date_commande')
    search_fields = ('client__nom', 'client__prenom')
    date_hierarchy = 'date_commande'
    inlines = [LigneCommandeInline]
    readonly_fields = ('date_commande',)
