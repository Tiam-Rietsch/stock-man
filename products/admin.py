from django.contrib import admin

from .models import Product, InventoryRecord

admin.site.register(Product)
admin.site.register(InventoryRecord)