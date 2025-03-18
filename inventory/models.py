import uuid
from django.db import models

from products.models import Product
from useraccounts.models import User

# Create your models here.
class InventoryRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='inventory_records')
    quantity_recorded = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    done_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='inventory_recordings')
