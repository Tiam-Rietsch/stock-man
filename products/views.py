from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Product, ProductCategory, ProductBrands
from notifications.models import InventoryUpdateNotification
from useraccounts.models import Roles, User

@login_required(login_url='login')
def products_list_view(request):
    """Affiche une liste de tous les produits."""
    products = Product.objects.all()
    context = {
        'products': products,
        'categories': ProductCategory.choices,
        'brands': ProductBrands.choices
    }
    return render(request, 'products/products.html', context)


@login_required(login_url='login')
def product_add_view(request):
    """Gère l'ajout d'un nouveau produit."""
    if request.method == 'POST':
        name = request.POST.get('name')
        brand = request.POST.get('brand')
        category = request.POST.get('category')
        sid = request.POST.get('sid')
        description = request.POST.get('description')
        unit_selling_price = request.POST.get('unit_selling_price')
        unit_buy_price = request.POST.get('unit_buy_price')
        min_stock = request.POST.get('min_stock', None)
        image = request.FILES.get('image')

        # Création d'un nouveau produit
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

        # Si le stock minimum est spécifié, on l'ajoute au produit
        if min_stock:
            product.min_stock = min_stock
            product.save()

        # Envoi de notifications de mise à jour de l'inventaire aux managers
        notification = InventoryUpdateNotification.objects.create(product=product)
        managers = User.objects.filter(role=Roles.manager)
        notification.target.add(*managers)
        notification.save()

        return redirect('products_list')

    return render(request, 'products/add_product.html')


@login_required(login_url='login')
def product_edit_view(request, id):
    """Gère la modification d'un produit existant."""
    product = get_object_or_404(Product, pk=id)

    if request.method == 'POST':
        # Mise à jour des champs du produit
        product.name = request.POST.get('name')
        product.brand = request.POST.get('brand')
        product.category = request.POST.get('category')
        product.sid = request.POST.get('sid')
        product.description = request.POST.get('description')
        product.unit_buy_price = request.POST.get('unit_buy_price')
        product.unit_selling_price = request.POST.get('unit_selling_price')
        product.min_stock = request.POST.get('min_stock')

        # Si une nouvelle image est fournie, on la met à jour
        if 'image' in request.FILES:
            product.image = request.FILES['image']

        product.save()
        return redirect('products_list')

    return render(request, 'products/edit_product.html', {'product': product})


@login_required(login_url='login')
def product_delete_view(request, id):
    """Gère la suppression d'un produit."""
    product = get_object_or_404(Product, pk=id)

    if request.method == 'POST':
        # Suppression du produit
        product.delete()
        return redirect('products_list')

    return render(request, 'products/confirm_delete.html', {'product': product})