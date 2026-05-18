from django.db import models
from django.core.validators import MinValueValidator


class Categorie(models.Model):
    """Modèle pour les catégories de produits"""
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100, null=False)
    descriptif = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'categories'
        verbose_name_plural = 'Catégories'

    def __str__(self):
        return self.nom


class Produit(models.Model):
    """Modèle pour les produits"""
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=150, null=False)
    date_peremption = models.DateField(blank=True, null=True)
    photo = models.CharField(max_length=255, blank=True, null=True)
    marque = models.CharField(max_length=100, blank=True, null=True)
    prix = models.DecimalField(max_digits=10, decimal_places=2, null=False, validators=[MinValueValidator(0)])
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, db_column='categorie_id')

    class Meta:
        db_table = 'produits'

    def __str__(self):
        return self.nom


class Client(models.Model):
    """Modèle pour les clients"""
    numero_client = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100, null=False)
    prenom = models.CharField(max_length=100, null=False)
    date_inscription = models.DateField(null=False)
    adresse = models.TextField(null=False)

    class Meta:
        db_table = 'clients'

    def __str__(self):
        return f"{self.prenom} {self.nom}"


class Commande(models.Model):
    """Modèle pour les commandes"""
    numero_commande = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, db_column='client_id')
    date_commande = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'commandes'

    def __str__(self):
        return f"Commande #{self.numero_commande} - {self.client}"


class LigneCommande(models.Model):
    """Modèle pour les lignes de commande"""
    id = models.AutoField(primary_key=True)
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE, db_column='commande_id')
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE, db_column='produit_id')
    quantite = models.IntegerField(null=False, validators=[MinValueValidator(1)])

    class Meta:
        db_table = 'lignes_commande'

    def __str__(self):
        return f"{self.produit.nom} x{self.quantite}"
    
    def get_total(self):
        """Retourne le total de la ligne (prix * quantité)"""
        return self.produit.prix * self.quantite
