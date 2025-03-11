import uuid
from django.db import models

class ProductBrands(models.TextChoices):
    cisco = 'C', 'CISCO'
    sdmo = 'S', 'SDMO'


class PRoductCategory(models.TextChoices):
    electric = 'ELECTRIC', 'ELECTRIC'
    electronic = 'ELECTRONIC', 'ELECTRONIC'


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=1, choices=ProductBrands.choices, default=ProductBrands.cisco)
    category = models.CharField(max_length=10, choices=PRoductCategory.choices, default=PRoductCategory.electronic)
    sid = models.CharField(max_length=255)
    description = models.TextField()
    quantity = models.IntegerField()
    unit_price = models.IntegerField()
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return f'{self.name} | {self.category} | {self.brand} | {self.unit_price} FCFA'