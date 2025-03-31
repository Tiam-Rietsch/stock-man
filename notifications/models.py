import uuid
from django.db import models

from useraccounts.models import User
from products.models import Product
from sales.models import Sale

class StatusChoices(models.TextChoices):
    orange = 'O', 'orange'
    green = 'G', 'green'
    red = 'R', 'red'


class NotificationTypeChoices(models.TextChoices):
    base = 'D', 'Base Notification'
    low_stock = 'A', 'Alerte Stock Faible'
    inventory_update = 'C', "Mis a jour de l'Inventaire"
    sale_record = 'B', "Notification de Vente"


class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.CharField(max_length=1, choices=StatusChoices.choices, default=StatusChoices.green)
    target = models.ManyToManyField(User, related_name='notifications')
    type = models.CharField(max_length=1, choices=NotificationTypeChoices.choices, default=NotificationTypeChoices.base)
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='notifications', null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='notifications', null=True)
    date = models.DateTimeField(auto_now_add=True)
    body = models.CharField(max_length=500)

    class Meta:
        ordering = ['type', '-date']


class LowStockNotification(Notification):
    class Meta:
        proxy = True 

    def save(self, *args, **kwargs):
        self.type = NotificationTypeChoices.low_stock
        self.status = StatusChoices.red
        self.body = f'Le Produit "{ self.product.name} | { self.product.get_brand_display()}" est en dessous du stock minimale. Stock restant: { self.product.quantity }.'
        return super().save(*args, **kwargs)
    

class InventoryUpdateNotification(Notification):
    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.type = NotificationTypeChoices.inventory_update
        self.status = StatusChoices.orange
        self.body = f'Le Stock du produit "{ self.product.name } | {self.product.get_brand_display()}" a ete mis a jour. Nouvelle quantite: { self.product.quantity }.'
        return super().save(*args, **kwargs)


class SaleRecordNotification(Notification):
    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.status = StatusChoices.green
        self.type = NotificationTypeChoices.sale_record
        self.body = f'Vente de  { self.sale.quantity } "{ self.sale.product.name} | {self.sale.product.get_brand_display() }" par { self.sale.done_by.name }.'
        return super().save(*args, **kwargs)
    

















    