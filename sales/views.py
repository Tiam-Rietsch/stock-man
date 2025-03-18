from django.shortcuts import render, redirect  # Importation des fonctions pour afficher et rediriger des pages
from django.db import transaction  # Permet d'assurer une transaction atomique

# Importation des modèles nécessaires
from django.contrib.auth.decorators import login_required  # Vérifie si l'utilisateur est connecté avant d'accéder à une vue
from .models import Sale  # Modèle représentant une vente
from products.models import Product  # Modèle représentant un produit
from useraccounts.models import User, Roles  # Modèle utilisateur et énumération des rôles
from notifications.models import (
    SaleRecordNotification,  # Notification de vente
    LowStockNotification,  # Notification de stock bas
    NotificationTypeChoices  # Types de notifications disponibles
)


# Vue permettant d'afficher la liste des ventes
@login_required(login_url='login')  # Oblige l'utilisateur à être connecté pour accéder à cette vue
def sales_list_view(request):
    """
    Affiche la liste des ventes en fonction du rôle de l'utilisateur.

    - Si l'utilisateur est un gestionnaire ('M'), il voit toutes les ventes.
    - Sinon, il ne voit que ses propres ventes.
    """
    if request.user.role == 'M':  
        sales = Sale.objects.all()  # Récupère toutes les ventes si l'utilisateur est un gestionnaire
    else:
        sales = request.user.sales.all()  # Récupère uniquement les ventes effectuées par l'utilisateur

    products = Product.objects.all()  # Récupère tous les produits disponibles en base de données

    context = {
        'sales': sales,  # Liste des ventes à afficher
        'products': products  # Liste des produits
    }

    return render(request, 'sales/sales.html', context)  # Renvoie la page avec les ventes et les produits


# Vue permettant d'ajouter une nouvelle vente
@login_required(login_url='login')  # Oblige l'utilisateur à être connecté pour accéder à cette vue
@transaction.atomic  # Assure que toutes les opérations sont effectuées dans une transaction atomique
def sale_add_view(request):
    """
    Permet d'ajouter une vente et met à jour le stock du produit concerné.

    - Enregistre la vente dans la base de données.
    - Met à jour la quantité du produit vendu.
    - Génère une notification pour les administrateurs et l'utilisateur connecté.
    - Vérifie si le stock est bas et crée une alerte si nécessaire.
    """
    if request.method == 'POST':  # Vérifie si la requête est de type POST (formulaire soumis)
        product = Product.objects.get(id=request.POST['product_id'])  # Récupère le produit vendu
        done_by = request.user  # Identifie l'utilisateur qui effectue la vente
        quantity = int(request.POST['quantity'])  # Récupère et convertit la quantité vendue en entier
        total_price = float(request.POST['total_price'])  # Récupère et convertit le prix total en flottant

        # Création et enregistrement de la vente
        sale = Sale.objects.create(
            product=product,  # Associe la vente au produit sélectionné
            done_by=done_by,  # Associe la vente à l'utilisateur qui l'a effectuée
            quantity=quantity,  # Stocke la quantité vendue
            total_price=total_price  # Stocke le prix total de la vente
        )

        product.quantity -= sale.quantity  # Met à jour la quantité en stock du produit
        product.save()  # Sauvegarde les modifications du produit

        # Création d'une notification pour informer les administrateurs et l'utilisateur de la nouvelle vente
        notification = SaleRecordNotification.objects.create(sale=sale)
        for user in User.objects.filter(role=Roles.admin):  # Sélectionne tous les administrateurs
            notification.target.add(user)  # Associe la notification à chaque administrateur
        notification.target.add(request.user)  # Associe également la notification à l'utilisateur ayant effectué la vente
        notification.save()  # Sauvegarde la notification

        # Vérification du stock pour générer une alerte si nécessaire
        stock_notifications = LowStockNotification.objects.filter(
            product=product, 
            type=NotificationTypeChoices.low_stock  # Filtre les notifications existantes pour ce produit
        )

        if stock_notifications.exists():  # Vérifie si des notifications de stock bas existent déjà
            for notification in stock_notifications:
                if product.quantity < product.min_stock:  # Si le stock est toujours insuffisant, on met à jour la notification
                    notification.save()
                else:
                    notification.delete()  # Si le stock est suffisant, on supprime la notification
        elif product.quantity < product.min_stock:  # Si aucune notification n'existe mais que le stock est bas
            notification = LowStockNotification.objects.create(product=product)  # Crée une nouvelle notification
            for user in User.objects.all():  # Associe cette notification à tous les utilisateurs
                notification.target.add(user)
            notification.save()  # Sauvegarde la notification

        return redirect('sales_list')  # Redirige l'utilisateur vers la liste des ventes après l'ajout réussi
