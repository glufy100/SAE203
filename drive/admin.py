from django.contrib import admin
from .models import Categorie, Produit, Client, Commande, LigneCommande


@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'descriptif')
    search_fields = ('nom',)


@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'marque', 'prix', 'categorie', 'date_peremption')
    list_filter = ('categorie', 'date_peremption')
    search_fields = ('nom', 'marque')


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('numero_client', 'nom', 'prenom', 'date_inscription', 'adresse')
    search_fields = ('nom', 'prenom')


# Inline pour afficher les lignes de commande directement dans la page Commande
class LigneCommandeInline(admin.TabularInline):
    model = LigneCommande
    extra = 1
    fields = ('produit', 'quantite')
    raw_id_fields = ('produit',)


@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display = ('numero_commande', 'client', 'date_commande')
    search_fields = ('client__nom', 'client__prenom')
    date_hierarchy = 'date_commande'
    inlines = [LigneCommandeInline]
    readonly_fields = ('date_commande',)

