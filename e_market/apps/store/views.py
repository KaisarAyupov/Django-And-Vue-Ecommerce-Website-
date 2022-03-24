import random

from datetime import datetime

from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Product, Category


def search(request):
    query = request.GET.get('query')
    instock = request.GET.get('instock')
    price_from = request.GET.get('price_from', 0)
    price_to = request.GET.get('price_to', 100000)
    sorting = request.GET.get('sorting', '-date_added')
    products = Product.objects.filter(Q(title__icontains=query) | Q(
        description__icontains=query)).filter(price__gte=price_from).filter(price__lte=price_to)

    if instock:
        products = products.filter(num_available__gte=1)

    context = {
        'query': query,
        'products': products.order_by(sorting),
        'instock': instock,
        'price_from': price_from,
        'price_to': price_to,
        'sorting': sorting
    }

    return render(request, 'search.html', context)


def product_detail(request, category_slug, slug):
    product = get_object_or_404(Product, slug=slug)

    imagesstring = "{'thumbnail': '%s', 'image': '%s'}," % (product.thumbnail.url, product.image.url)

    for image in product.images.all():
        imagesstring = imagesstring + \
            ("{'thumbnail': '%s', 'image': '%s'}," % (
                image.thumbnail.url, image.image.url))

    context = {
        'product': product,
        'imagesstring': imagesstring
    }

    return render(request, 'product_detail.html', context)


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.products.all()

    context = {
        'category': category,
        'products': products
    }

    return render(request, 'category_detail.html', context)
