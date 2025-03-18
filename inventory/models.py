import uuid
from django.db import models

from products.models import Product
from useraccounts.models import User


class InventoryRecord(models.Model):
    """Modèle représentant un enregistrement d'inventaire."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # Identifiant unique de l'enregistrement
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='inventory_records')  # Produit associé
    quantity_recorded = models.IntegerField()  # Quantité enregistrée
    date = models.DateTimeField(auto_now_add=True)  # Date de l'enregistrement (automatiquement ajoutée)
    done_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='inventory_recordings')  # Utilisateur ayant effectué l'enregistrement