from django.shortcuts import render, redirect
from django.db import transaction

from .models import Sale
from products.models import Product
from useraccounts.models import User, Roles
from notifications.models import SaleRecordNotification, LowStockNotification, NotificationTypeChoices

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

        notification = SaleRecordNotification.objects.create(sale=sale)
        for user in User.objects.filter(role=Roles.manager): notification.target.add(user)
        notification.save()

        stock_notifications = LowStockNotification.objects.filter(product=product, type=NotificationTypeChoices.low_stock)
        if len(stock_notifications) > 0:
            for notification in stock_notifications:
                if product.quantity < product.min_stock:
                    notification.save()
                else:
                    notification.delete()
        elif product.quantity < product.min_stock:
            notification = LowStockNotification.objects.create(product=product)
            for user in User.objects.all(): notification.target.add(user)
            notification.save()

        product.save()

        return redirect('sales_list')
