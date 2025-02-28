from django.shortcuts import render, get_object_or_404
from catalog.models import Product


def home(request):
    return render(request, 'catalog/home.html')


def contact(request):
    return render(request, 'catalog/contacts.html')


def product_list(request):
    products = Product.objects.all()
    context = {"products": products}
    return render(request, 'catalog/product.html', context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {"product": product}
    return render(request, 'catalog/product_detail.html', context)
