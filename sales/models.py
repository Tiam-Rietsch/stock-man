import uuid  # Importation du module UUID pour générer des identifiants uniques
from django.db import models  # Importation du module models pour définir les modèles Django

# Importation des modèles nécessaires
from useraccounts.models import User  # Modèle utilisateur
from products.models import Product  # Modèle produit


class Sale(models.Model):
    """
    Modèle représentant une vente.
    
    Une vente est liée à un produit, un utilisateur (vendeur) et contient des informations 
    sur la quantité vendue et le prix total.
    """
    id = models.UUIDField(
        primary_key=True,  # Définit cet attribut comme clé primaire
        default=uuid.uuid4,  # Génère automatiquement un UUID unique pour chaque vente
        editable=False  # Empêche la modification de cet identifiant après la création
    )
    
    date = models.DateTimeField(
        auto_now_add=True  # Enregistre automatiquement la date et l'heure de création de la vente
    )
    
    product = models.ForeignKey(
        Product,  # Référence au modèle Product
        on_delete=models.SET_NULL,  # Si le produit est supprimé, la référence devient NULL au lieu de supprimer la vente
        null=True,  # Permet d'avoir une valeur NULL si le produit est supprimé
        related_name='sales'  # Permet d'accéder aux ventes associées depuis un produit via product.sales
    )
    
    done_by = models.ForeignKey(
        User,  # Référence au modèle User
        on_delete=models.SET_NULL,  # Si l'utilisateur est supprimé, la référence devient NULL
        null=True,  # Permet d'avoir une valeur NULL si l'utilisateur est supprimé
        related_name='sales'  # Permet d'accéder aux ventes effectuées par un utilisateur via user.sales
    )
    
    quantity = models.IntegerField(
        help_text="Quantité de produits vendus"  # Ajoute une aide descriptive pour ce champ
    )
    
    total_price = models.FloatField(
        default=0,  # Valeur par défaut du prix total
        help_text="Prix total de la vente"  # Ajoute une aide descriptive pour ce champ
    )

    def __str__(self):
        """
        Retourne une représentation textuelle de la vente.

        Ex : "2024-03-18 14:30 | 2 iPhone 13 by John Doe"
        """
        return f'{self.date} | {self.quantity} {self.product.name} by {self.done_by}'
