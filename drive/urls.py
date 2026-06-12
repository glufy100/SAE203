from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # CRUD categories
    path('categories/', views.categorie_list, name='categorie_list'),
    path('categories/create/', views.categorie_create, name='categorie_create'),
    path('categories/<int:id>/edit/', views.categorie_update, name='categorie_update'),
    path('categories/<int:id>/delete/', views.categorie_delete, name='categorie_delete'),

    # CRUD produits
    path('produits/', views.produit_list, name='produit_list'),
    path('produits/create/', views.produit_create, name='produit_create'),
    path('produits/<int:id>/edit/', views.produit_update, name='produit_update'),
    path('produits/<int:id>/delete/', views.produit_delete, name='produit_delete'),

    # CRUD clients
    path('clients/', views.client_list, name='client_list'),
    path('clients/<int:numero_client>/', views.client_detail, name='client_detail'),
    path('clients/create/', views.client_create, name='client_create'),
    path('clients/<int:numero_client>/edit/', views.client_update, name='client_update'),
    path('clients/<int:numero_client>/delete/', views.client_delete, name='client_delete'),

    # CRUD commandes et gestion des lignes de commande
    path('commandes/', views.commande_list, name='commande_list'),
    path('commandes/create/', views.commande_create, name='commande_create'),
    path('commandes/<int:numero_commande>/', views.commande_detail, name='commande_detail'),
    path('commandes/<int:numero_commande>/delete/', views.commande_delete, name='commande_delete'),
    path('commandes/<int:numero_commande>/ajouter-produit/', views.commande_add_produit, name='commande_add_produit'),
    path('commandes/<int:numero_commande>/produit/<int:ligne_id>/modifier/', views.commande_update_produit, name='commande_update_produit'),
    path('commandes/<int:numero_commande>/produit/<int:ligne_id>/supprimer/', views.commande_delete_produit, name='commande_delete_produit'),
]
