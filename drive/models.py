from django.db import models
from django.core.validators import MinValueValidator


class Categorie(models.Model):
    nom = models.CharField(max_length=100)
    descriptif = models.TextField(blank=True)

    class Meta:
        db_table = 'categories'
        verbose_name_plural = 'Catégories'

    def __str__(self):
        return self.nom


class Produit(models.Model):
    nom = models.CharField(max_length=150)
    date_peremption = models.DateField(blank=True, null=True)
    photo = models.CharField(max_length=255, blank=True)
    marque = models.CharField(max_length=100, blank=True)
    prix = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)

    class Meta:
        db_table = 'produits'

    def __str__(self):
        return self.nom


class Client(models.Model):
    numero_client = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_inscription = models.DateField()
    adresse = models.TextField()

    class Meta:
        db_table = 'clients'

    def __str__(self):
        return f"{self.prenom} {self.nom}"


class Commande(models.Model):
    numero_commande = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date_commande = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'commandes'

    def __str__(self):
        return f"Commande #{self.numero_commande} - {self.client}"


class LigneCommande(models.Model):
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.IntegerField(validators=[MinValueValidator(1)])

    class Meta:
        db_table = 'lignes_commande'

    def __str__(self):
        return f"{self.produit.nom} x{self.quantite}"
    
    def get_total(self):
        return self.produit.prix * self.quantite
