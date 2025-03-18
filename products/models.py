import uuid
from django.db import models

from useraccounts.models import User


class ProductBrands(models.TextChoices):
    """Choix pour les marques de produits."""
    cisco = 'C', 'CISCO'  # Marque CISCO
    sdmo = 'S', 'SDMO'    # Marque SDMO


class ProductCategory(models.TextChoices):
    """Choix pour les catégories de produits."""
    electric = 'A', 'ELECTRIQUE'    # Catégorie ÉLECTRIQUE
    electronic = 'B', 'ELECTRONIQUE'  # Catégorie ÉLECTRONIQUE


class Product(models.Model):
    """Modèle représentant un produit."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # Identifiant unique du produit
    name = models.CharField(max_length=255)  # Nom du produit
    brand = models.CharField(max_length=1, choices=ProductBrands.choices, default=ProductBrands.cisco)  # Marque du produit
    category = models.CharField(max_length=1, choices=ProductCategory.choices, default=ProductCategory.electronic)  # Catégorie du produit
    quantity = models.IntegerField(default=0)  # Quantité en stock
    min_stock = models.IntegerField(default=10)  # Stock minimum requis
    sid = models.CharField(max_length=255)  # Identifiant unique du produit (SKU ou autre)
    description = models.TextField(blank=True, null=True)  # Description du produit (optionnelle)
    unit_buy_price = models.FloatField()  # Prix d'achat unitaire
    unit_selling_price = models.FloatField(default=0.0)  # Prix de vente unitaire
    image = models.ImageField(upload_to='products/')  # Image du produit (stockée dans le dossier 'products/')

    def __str__(self):
        """Représentation en chaîne de caractères du produit."""
        return f'{self.name} | {self.category} | {self.brand}'