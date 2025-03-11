import uuid
from django.db import models

class ProductBrands(models.TextChoices):
    cisco = 'C', 'CISCO'
    sdmo = 'S', 'SDMO'


class PRoductCategory(models.TextChoices):
    electric = 'A', 'ELECTRIC'
    electronic = 'B', 'ELECTRONIC'


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=1, choices=ProductBrands.choices, default=ProductBrands.cisco)
    category = models.CharField(max_length=1, choices=PRoductCategory.choices, default=PRoductCategory.electronic)
    quantity = models.IntegerField()
    sid = models.CharField(max_length=255)
    description = models.TextField()
    unit_price = models.IntegerField()
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return f'{self.name} | {self.category} | {self.brand} | {self.unit_price} FCFA'