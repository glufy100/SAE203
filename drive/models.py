from django.db import models
from django.core.validators import MinValueValidator


class Categorie(models.Model):
    """Categorie de produits utilisee comme referentiel de classement."""
    nom = models.CharField(max_length=100)
    descriptif = models.TextField(blank=True)

    class Meta:
        # Mapping direct vers la table SQL existante.
        db_table = 'categories'
        verbose_name_plural = 'Catégories'

    def __str__(self):
        """Retourne le nom affiche dans l'admin et les selects."""
        return self.nom


class Produit(models.Model):
    """Produit vendable associe a une categorie et a des attributs optionnels."""
    nom = models.CharField(max_length=150)
    date_peremption = models.DateField(blank=True, null=True)
    photo = models.CharField(max_length=255, blank=True)
    marque = models.CharField(max_length=100, blank=True)
    prix = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)

    class Meta:
        # Table dediee aux produits dans la base.
        db_table = 'produits'

    def __str__(self):
        """Retourne le libelle du produit pour les listes et l'admin."""
        return self.nom


class Client(models.Model):
    """Client de l'application avec informations d'identite et adresse."""
    numero_client = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_inscription = models.DateField()
    adresse = models.TextField()

    class Meta:
        # Table des clients existante en base.
        db_table = 'clients'

    def __str__(self):
        """Retourne l'identite lisible du client."""
        return f"{self.prenom} {self.nom}"


class Commande(models.Model):
    """Commande passee par un client avec timestamp de creation."""
    numero_commande = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date_commande = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Table des commandes, alignee sur le schema SQL fourni.
        db_table = 'commandes'

    def __str__(self):
        """Retourne une etiquette exploitable dans l'admin."""
        return f"Commande #{self.numero_commande} - {self.client}"


class LigneCommande(models.Model):
    """Ligne de commande reliant une commande a un produit avec une quantite."""
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.IntegerField(validators=[MinValueValidator(1)])

    class Meta:
        # Table d'association des lignes de commande.
        db_table = 'lignes_commande'

    def __str__(self):
        """Retourne un resume court de la ligne pour l'admin et les logs."""
        return f"{self.produit.nom} x{self.quantite}"

    def get_total(self):
        """Retourne le total de la ligne.

        Entrée:
        - aucun parametre.

        Sortie:
        - Decimal correspondant a prix * quantite.
        """
        return self.produit.prix * self.quantite
