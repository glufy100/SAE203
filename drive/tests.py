from datetime import date
from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from .models import Categorie, Produit, Client, Commande, LigneCommande


class HomeViewTests(TestCase):
    def setUp(self):
        categorie = Categorie.objects.create(nom='Boissons', descriptif='Boissons fraîches')
        produit = Produit.objects.create(nom='Eau', prix=Decimal('1.50'), categorie=categorie)
        client = Client.objects.create(
            nom='Dupont',
            prenom='Alice',
            date_inscription=date(2026, 6, 12),
            adresse='1 rue de la Paix',
        )
        commande = Commande.objects.create(client=client)
        LigneCommande.objects.create(commande=commande, produit=produit, quantite=2)

    def test_drive_root_resolves_to_home_page(self):
        self.assertEqual(reverse('home'), '/drive/')

        response = self.client.get('/drive/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'drive/home.html')
        self.assertEqual(response.context['categories_count'], 1)
        self.assertEqual(response.context['produits_count'], 1)
        self.assertEqual(response.context['clients_count'], 1)
        self.assertEqual(response.context['commandes_count'], 1)
