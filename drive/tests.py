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


class CommandeAutocompleteTests(TestCase):
    def setUp(self):
        self.categorie = Categorie.objects.create(nom='Boissons', descriptif='Boissons fraîches')
        self.produit_eau = Produit.objects.create(nom='Eau', prix=Decimal('1.50'), categorie=self.categorie)
        self.produit_jus = Produit.objects.create(nom='Jus d\'orange', prix=Decimal('2.10'), categorie=self.categorie)
        client = Client.objects.create(
            nom='Dupont',
            prenom='Alice',
            date_inscription=date(2026, 6, 12),
            adresse='1 rue de la Paix',
        )
        self.commande = Commande.objects.create(client=client)
        LigneCommande.objects.create(commande=self.commande, produit=self.produit_eau, quantite=2)

    def test_api_produits_search_returns_matching_products(self):
        response = self.client.get(reverse('api_produits_search'), {'q': 'jus'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'produits': [
                {
                    'id': self.produit_jus.id,
                    'nom': "Jus d'orange",
                    'prix': '2.10',
                    'categorie': 'Boissons',
                    'marque': '-',
                }
            ]
        })

    def test_commande_detail_page_renders(self):
        response = self.client.get(reverse('commande_detail', args=[self.commande.numero_commande]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Rechercher un produit')
