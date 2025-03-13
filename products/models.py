import uuid
from django.db import models

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
    min_stock = models.IntegerField(default=3)
    sid = models.CharField(max_length=255)
    description = models.TextField()
    unit_price = models.FloatField()
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return f'{self.name} | {self.category} | {self.brand} | {self.unit_price} FCFA'