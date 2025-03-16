from django.shortcuts import render
from django.db import models
from django.http import JsonResponse
from datetime import datetime, timedelta
from django.db.models import Sum

from products.models import Product
from sales.models import Sale


def dashboard_view(request):
    context = {
        'total_stock_value': sum([product.quantity * product.unit_selling_price for product in Product.objects.all()]),
        'total_day_sales': sum([sale.total_price for sale in Sale.objects.filter(date__date=datetime.now().date())]),
        'low_stock_count': len([product for product in Product.objects.filter(quantity__lt=models.F("min_stock"))]),
        'total_products_count': len(Product.objects.all())
    }
    return render(request, 'dashboard/dashboard.html', context)


def get_chart_data(request):
    # Get the current date and time
    now = datetime.now()

    # Yearly Sales Data
    yearly_sales = []
    for month in range(1, 13):
        start_of_month = now.replace(month=month, day=1, hour=0, minute=0, second=0, microsecond=0)
        end_of_month = (start_of_month + timedelta(days=32)).replace(day=1) - timedelta(microseconds=1)
        monthly_sales = Sale.objects.filter(date__gte=start_of_month, date__lte=end_of_month).aggregate(total_sales=Sum('total_price'))['total_sales'] or 0
        yearly_sales.append(monthly_sales)

    # Monthly Sales Data
    monthly_sales = []
    for day in range(1, 32):
        start_of_day = now.replace(day=day, hour=0, minute=0, second=0, microsecond=0)
        end_of_day = start_of_day + timedelta(days=1) - timedelta(microseconds=1)
        daily_sales = Sale.objects.filter(date__gte=start_of_day, date__lte=end_of_day).aggregate(total_sales=Sum('total_price'))['total_sales'] or 0
        monthly_sales.append(daily_sales)

    # Top Selling Products
    top_selling_products = Product.objects.annotate(total_sold=Sum('sales__quantity')).order_by('-total_sold')[:7]
    top_selling_data = {
        "products": [product.name for product in top_selling_products],
        "quantities": [product.total_sold or 0 for product in top_selling_products],
    }

    # Inventory Overview
    inventory_overview = Product.objects.all()
    inventory_data = {
        "labels": [product.name for product in inventory_overview],
        "quantities": [product.quantity for product in inventory_overview],
    }

    # Compile all data into a JSON response
    data = {
        "yearly_sales": yearly_sales,
        "monthly_sales": monthly_sales,
        "top_selling_products": top_selling_data,
        "inventory_overview": inventory_data,
    }

    return JsonResponse(data)


