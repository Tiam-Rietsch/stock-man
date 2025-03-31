from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import models
from django.http import JsonResponse
from datetime import datetime, timedelta
from django.db.models import Sum

from products.models import Product
from sales.models import Sale
from notifications.models import Notification


@login_required()
def dashboard_view(request):
    """Affiche le tableau de bord avec les statistiques principales."""
    context = {
        'total_stock_value': sum([product.quantity * product.unit_selling_price for product in Product.objects.all()]),  # Valeur totale du stock
        'total_day_sales': sum([sale.total_price for sale in Sale.objects.filter(date__date=datetime.now().date())]),  # Ventes totales du jour
        'low_stock_count': len([product for product in Product.objects.filter(quantity__lt=models.F("min_stock"))]),  # Nombre de produits en stock faible
        'total_products_count': len(Product.objects.all()),  # Nombre total de produits
        'notifications': Notification.objects.all()[:12]  # 12 dernières notifications
    }
    return render(request, 'dashboard/dashboard.html', context)


def get_chart_data(request):
    """Récupère les données pour les graphiques du tableau de bord."""
    # Obtenir la date et l'heure actuelles
    now = datetime.now()

    # Données des ventes annuelles
    yearly_sales = []
    for month in range(1, 13):
        start_of_month = now.replace(month=month, day=1, hour=0, minute=0, second=0, microsecond=0)  # Début du mois
        end_of_month = (start_of_month + timedelta(days=32)).replace(day=1) - timedelta(microseconds=1)  # Fin du mois
        monthly_sales = Sale.objects.filter(date__gte=start_of_month, date__lte=end_of_month).aggregate(total_sales=Sum('total_price'))['total_sales'] or 0  # Ventes mensuelles
        yearly_sales.append(monthly_sales)

    # Données des ventes mensuelles
    monthly_sales = []
    for day in range(1, 32):
        start_of_day = now.replace(day=day, hour=0, minute=0, second=0, microsecond=0)  # Début du jour
        end_of_day = start_of_day + timedelta(days=1) - timedelta(microseconds=1)  # Fin du jour
        daily_sales = Sale.objects.filter(date__gte=start_of_day, date__lte=end_of_day).aggregate(total_sales=Sum('total_price'))['total_sales'] or 0  # Ventes quotidiennes
        monthly_sales.append(daily_sales)

    # Produits les plus vendus
    top_selling_products = Product.objects.annotate(total_sold=Sum('sales__quantity')).order_by('-total_sold')[:7]  # Top 7 des produits
    top_selling_data = {
        "products": [product.name for product in top_selling_products],  # Noms des produits
        "quantities": [product.total_sold or 0 for product in top_selling_products],  # Quantités vendues
    }

    # Aperçu de l'inventaire
    inventory_overview = Product.objects.all()
    inventory_data = {
        "labels": [product.name for product in inventory_overview],  # Noms des produits
        "quantities": [product.quantity for product in inventory_overview],  # Quantités en stock
    }

    # Compiler toutes les données dans une réponse JSON
    data = {
        "yearly_sales": yearly_sales,  # Ventes annuelles
        "monthly_sales": monthly_sales,  # Ventes mensuelles
        "top_selling_products": top_selling_data,  # Produits les plus vendus
        "inventory_overview": inventory_data,  # Aperçu de l'inventaire
    }

    return JsonResponse(data)  # Retourner les données au format JSON