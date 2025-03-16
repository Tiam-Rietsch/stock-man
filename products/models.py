import uuid
from django.db import models

from useraccounts.models import User


class ProductBrands(models.TextChoices):
    cisco = 'C', 'CISCO'
    sdmo = 'S', 'SDMO'


class ProductCategory(models.TextChoices):
    electric = 'A', 'ELECTRIQUE'
    electronic = 'B', 'ELECTRONIQUE'


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=1, choices=ProductBrands.choices, default=ProductBrands.cisco)
    category = models.CharField(max_length=1, choices=ProductCategory.choices, default=ProductCategory.electronic)
    quantity = models.IntegerField(default=0)
    min_stock = models.IntegerField(default=10)
    sid = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    unit_buy_price = models.FloatField()
    unit_selling_price = models.FloatField(default=0.0)
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return f'{self.name} | {self.category} | {self.brand}'
    

class InventoryRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='inventory_records')
    quantity_recorded = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    done_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='inventory_recordings')

    def __str__(self):
        return f'{self.quantity_recorded} {self.product.name} recorded on {self.date} by {self.done_by}'