from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Product, ProductCategory, ProductBrands


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
        unit_price = request.POST['unit_price']

        print(request.FILES)

        image = request.FILES['image']

        product = Product.objects.create(
            name=name,
            brand=brand,
            category=category,
            sid=sid,
            description=description,
            unit_price=unit_price,
            image=image
        )
        product.save()

        return redirect('products_list')


@login_required(login_url='login')
def product_edit_view(request, id):
    if request.method == 'POST':
        name = request.POST['name']
        brand = request.POST['brand']
        category = request.POST['category']
        sid = request.POST['sid']
        description = request.POST['description']
        unit_price = request.POST['unit_price']
        image = request.FILES['image']

        product = Product.objects.get(pk=id)
        product.name = name
        product.brand = brand
        product.category = category
        product.sid = sid
        product.description = description
        product.unit_price = unit_price
        product.image = image

        product.save()

        return redirect('products_list')
    

@login_required(login_url='login')
def product_delete_view(request, id):
    if request.method == 'POST':
        product = Product.objects.get(pk=id)
        product.delete()
        return redirect('products_list')
    

@login_required(login_url='login')
def inventory_view(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'products/inventory.html', context)


@login_required(login_url='login')
def stock_update_view(request, id):
    if request.method == 'POST':
        quantity = int(request.POST['quantity'])
        supplied = bool(request.GET['supplied'] == 'true')

        product = Product.objects.get(pk=id)

        product.quantity = product.quantity + quantity if supplied else quantity
        product.save()

        return redirect('inventory')
    

