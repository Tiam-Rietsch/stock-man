from django.shortcuts import render, redirect
from django.db import transaction

from .models import Sale
from products.models import Product

def sales_list_view(request):
    sales = Sale.objects.all() if request.user.role == 'M' else request.user.sales.all()
    products = Product.objects.all() 
    context = {
        'sales': sales,
        'products': products
    }
    return render(request, 'sales/sales.html', context)


@transaction.atomic
def sale_add_view(request):
    if request.method == 'POST':
        product = Product.objects.get(id=request.POST['product_id'])
        done_by = request.user
        quantity = int(request.POST['quantity'])
        total_price = float(request.POST['total_price'])

        sale = Sale.objects.create(
            product=product,
            done_by=done_by,
            quantity=quantity,
            total_price=total_price
        )

        product.quantity -= sale.quantity
        sale.save()
        product.save()

        return redirect('sales_list')
