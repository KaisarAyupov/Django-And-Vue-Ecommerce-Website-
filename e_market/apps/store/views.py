from django.shortcuts import render, get_object_or_404
from .models import Product

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)

    context = {
        'product' : product
    }
    
    return render(request, 'product_detail.html', context)
