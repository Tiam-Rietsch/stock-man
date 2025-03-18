from django.http import HttpResponse
from openpyxl import Workbook
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.timezone import make_naive

from .models import Product, ProductCategory, ProductBrands
from notifications.models import InventoryUpdateNotification, LowStockNotification, NotificationTypeChoices
from useraccounts.models import Roles, User
from sales.models import Sale

@login_required(login_url='login')
def products_list_view(request):
    products = Product.objects.all()
    context =  {
        'products': products,
        'categories': ProductCategory.choices,
        'brands': ProductBrands.choices
    }
    return render(request, 'products/products.html', context)


@login_required(login_url='login')
def product_add_view(request):
    if request.method == 'POST':
        name = request.POST['name']
        brand = request.POST['brand']
        category = request.POST['category']
        sid = request.POST['sid']
        description = request.POST['description']
        unit_selling_price = request.POST['unit_selling_price']
        unit_buy_price = request.POST['unit_buy_price']
        min_stock = request.POST['min_stock']
        image = request.FILES['image']

        product = Product.objects.create(
            name=name,
            brand=brand,
            category=category,
            sid=sid,
            description=description,
            unit_selling_price=unit_selling_price,
            unit_buy_price=unit_buy_price,
            image=image,
        )
        if min_stock:
            product.min_stock = min_stock
        product.save()

        notification = InventoryUpdateNotification.objects.create(product=product)
        for user in User.objects.filter(role=Roles.manager): notification.target.add(user)
        notification.save()

        return redirect('products_list')


@login_required(login_url='login')
def product_edit_view(request, id):
    if request.method == 'POST':
        name = request.POST['name']
        brand = request.POST['brand']
        category = request.POST['category']
        sid = request.POST['sid']
        description = request.POST['description']
        unit_buy_price = request.POST['unit_buy_price']
        unit_selling_price = request.POST['unit_selling_price']
        image = request.FILES['image'] if request.FILES else None
        min_stock = request.POST['min_stock']

        product = Product.objects.get(pk=id)
        product.name = name
        product.brand = brand
        product.category = category
        product.sid = sid
        product.description = description
        product.unit_buy_price = unit_buy_price
        product.unit_selling_price = unit_selling_price
        product.min_stock = min_stock
        if image:
            product.image = image

        product.save()

        return redirect('products_list')
    

@login_required(login_url='login')
def product_delete_view(request, id):
    if request.method == 'POST':
        product = Product.objects.get(pk=id)
        product.delete()
        return redirect('products_list')
    
