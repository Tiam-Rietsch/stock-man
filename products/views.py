from django.http import HttpResponse
from openpyxl import Workbook
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.timezone import make_naive

from .models import Product, ProductCategory, ProductBrands, InventoryRecord
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
    

@login_required(login_url='login')
def inventory_view(request):
    products = Product.objects.all()
    context = {
        'products': products,
        'inventory_records': InventoryRecord.objects.all(),
        'sales': Sale.objects.all()
    }
    return render(request, 'products/inventory.html', context)


@login_required(login_url='login')
def stock_update_view(request, id):
    if request.method == 'POST':
        quantity = int(request.POST['quantity'])
        supplied = bool(request.GET['supplied'] == 'true')
        record_id = request.GET['record_id'] if not supplied else None
        product = Product.objects.get(pk=id)

        if supplied:
            inventory_record = InventoryRecord.objects.create(
                quantity_recorded=quantity,
                done_by=request.user
            )
            inventory_record.save()
            product.inventory_records.add(inventory_record)
            product.quantity = product.quantity + quantity
            product.save()
        else:
            inventory_record = InventoryRecord.objects.get(pk=record_id)
            product.quantity += quantity - inventory_record.quantity_recorded
            inventory_record.quantity_recorded = quantity
            inventory_record.save()
            product.save()

        notification = InventoryUpdateNotification.objects.create(product=product)
        for user in User.objects.all(): notification.target.add(user)
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

        return redirect('inventory')
    

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from openpyxl import Workbook
from django.utils.timezone import make_naive  # Convert timezone-aware datetimes to naive datetimes

from .models import Product, ProductCategory, ProductBrands, InventoryRecord
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
    

@login_required(login_url='login')
def inventory_view(request):
    products = Product.objects.all()
    context = {
        'products': products,
        'inventory_records': InventoryRecord.objects.all(),
        'sales': Sale.objects.all()
    }
    return render(request, 'products/inventory.html', context)


@login_required(login_url='login')
def stock_update_view(request, id):
    if request.method == 'POST':
        quantity = int(request.POST['quantity'])
        supplied = bool(request.GET['supplied'] == 'true')
        record_id = request.GET['record_id'] if not supplied else None
        product = Product.objects.get(pk=id)

        if supplied:
            inventory_record = InventoryRecord.objects.create(
                quantity_recorded=quantity,
                done_by=request.user
            )
            inventory_record.save()
            product.inventory_records.add(inventory_record)
            product.quantity = product.quantity + quantity
            product.save()
        else:
            inventory_record = InventoryRecord.objects.get(pk=record_id)
            product.quantity += quantity - inventory_record.quantity_recorded
            inventory_record.quantity_recorded = quantity
            inventory_record.save()
            product.save()

        notification = InventoryUpdateNotification.objects.create(product=product)
        for user in User.objects.all(): notification.target.add(user)
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

        return redirect('inventory')


from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Border, Side, Alignment, Font
from openpyxl.utils import get_column_letter
from django.utils.timezone import make_naive

from .models import Product, InventoryRecord
from sales.models import Sale

@login_required(login_url='login')
def export_inventory_to_excel(request):
    # Create a workbook and add sheets
    wb = Workbook()

    # Define styles
    header_fill = PatternFill(start_color="007BFF", end_color="007BFF", fill_type="solid")  # Blue background
    header_font = Font(color="FFFFFF", bold=True)  # White text, bold
    border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )
    alignment = Alignment(horizontal="left", vertical="center")

    # Sheet 1: All Inventory
    ws_all = wb.active
    ws_all.title = "All Inventory"
    ws_all.append(['Name', 'Brand', 'Category', 'Quantity in Stock'])

    # Apply header styles
    for col in range(1, 5):
        cell = ws_all.cell(row=1, column=col)
        cell.fill = header_fill
        cell.font = header_font
        cell.border = border
        cell.alignment = alignment

    # Add data and apply styles
    products = Product.objects.all()
    for product in products:
        ws_all.append([product.name, product.get_brand_display(), product.get_category_display(), product.quantity])

    for row in ws_all.iter_rows(min_row=2, max_row=ws_all.max_row, min_col=1, max_col=4):
        for cell in row:
            cell.border = border
            cell.alignment = alignment

    # Set column widths
    ws_all.column_dimensions['A'].width = 30  # Name
    ws_all.column_dimensions['B'].width = 20  # Brand
    ws_all.column_dimensions['C'].width = 20  # Category
    ws_all.column_dimensions['D'].width = 15  # Quantity

    # Sheet 2: Products Registered (Inventory Records)
    ws_registered = wb.create_sheet("Products Registered")
    ws_registered.append(['Product Name', 'Brand', 'Category', 'Quantity Recorded', 'Date', 'Recorded By'])

    # Apply header styles
    for col in range(1, 7):
        cell = ws_registered.cell(row=1, column=col)
        cell.fill = header_fill
        cell.font = header_font
        cell.border = border
        cell.alignment = alignment

    # Add data and apply styles
    inventory_records = InventoryRecord.objects.all()
    for record in inventory_records:
        naive_date = make_naive(record.date)
        ws_registered.append([
            record.product.name,
            record.product.get_brand_display(),
            record.product.get_category_display(),
            record.quantity_recorded,
            naive_date,
            record.done_by.name
        ])

    for row in ws_registered.iter_rows(min_row=2, max_row=ws_registered.max_row, min_col=1, max_col=6):
        for cell in row:
            cell.border = border
            cell.alignment = alignment

    # Set column widths
    ws_registered.column_dimensions['A'].width = 30  # Product Name
    ws_registered.column_dimensions['B'].width = 20  # Brand
    ws_registered.column_dimensions['C'].width = 20  # Category
    ws_registered.column_dimensions['D'].width = 15  # Quantity Recorded
    ws_registered.column_dimensions['E'].width = 20  # Date
    ws_registered.column_dimensions['F'].width = 20  # Recorded By

    # Sheet 3: Products Sold
    ws_sold = wb.create_sheet("Products Sold")
    ws_sold.append(['Product Name', 'Brand', 'Category', 'Quantity Sold', 'Unit Selling Price', 'Total Price', 'Sold By'])

    # Apply header styles
    for col in range(1, 8):
        cell = ws_sold.cell(row=1, column=col)
        cell.fill = header_fill
        cell.font = header_font
        cell.border = border
        cell.alignment = alignment

    # Add data and apply styles
    sales = Sale.objects.all()
    for sale in sales:
        ws_sold.append([
            sale.product.name,
            sale.product.get_brand_display(),
            sale.product.get_category_display(),
            sale.quantity,
            sale.product.unit_selling_price,
            sale.total_price,
            sale.done_by.name
        ])

    for row in ws_sold.iter_rows(min_row=2, max_row=ws_sold.max_row, min_col=1, max_col=7):
        for cell in row:
            cell.border = border
            cell.alignment = alignment

    # Set column widths
    ws_sold.column_dimensions['A'].width = 30  # Product Name
    ws_sold.column_dimensions['B'].width = 20  # Brand
    ws_sold.column_dimensions['C'].width = 20  # Category
    ws_sold.column_dimensions['D'].width = 15  # Quantity Sold
    ws_sold.column_dimensions['E'].width = 15  # Unit Selling Price
    ws_sold.column_dimensions['F'].width = 15  # Total Price
    ws_sold.column_dimensions['G'].width = 20  # Sold By

    # Set row heights
    for sheet in wb:
        for row in sheet.iter_rows():
            sheet.row_dimensions[row[0].row].height = 20  # Set row height to 20

    # Save the workbook to a HttpResponse
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="inventory_report.xlsx"'
    wb.save(response)

    return response