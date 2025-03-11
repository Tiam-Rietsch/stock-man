from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def products_list_view(request):
    return render(request, 'products/products.html')
