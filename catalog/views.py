from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View

from catalog.models import Product


class HomeListView(ListView):
    model = Product


class ProductDetailView(DetailView):
    model = Product


class ContactView(View):
    def get(self, request):
        return render(request, 'catalog/contact.html')


class ProductsListView(ListView):
    model = Product
