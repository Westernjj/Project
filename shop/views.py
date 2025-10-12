from django.shortcuts import render
from .models import Product

def index(request):
    products = Product.objects.select_related('category').all()
    return render(request, 'shop/index.html', {'products': products})
