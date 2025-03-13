import uuid
from django.db import models

from useraccounts.models import User
from products.models import Product

class Sale(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='sales')
    done_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='sales')
    quantity = models.IntegerField()
    total_price = models.FloatField(default=0)

    def __str__(self):
        return f'{self.date} | {self.quantity} {self.product.name} by {self.done_by}'