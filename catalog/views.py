from django.core.exceptions import PermissionDenied
from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from catalog.models import Product
from catalog.forms import ProductForm

from django.urls import reverse_lazy


class PublishProductView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "catalog.can_unpublish_product"

    def post(self, request: HttpRequest, product_id: int):
        product = get_object_or_404(Product, pk=product_id)
        product.is_published = True
        product.save()
        return redirect('catalog:product_detail', pk=product_id)


class UnpublishProductView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "catalog.can_unpublish_product"

    def post(self, request: HttpRequest, product_id: int):
        product = get_object_or_404(Product, pk=product_id)
        product.is_published = False
        product.save()
        return redirect('catalog:product_detail', pk=product_id)


class HomeListView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(is_published=True)


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:product_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

    def get_queryset(self):
        queryset = Product.objects.filter(is_published=True)

        if self.request.user.is_authenticated:
            user_products = Product.objects.filter(owner=self.request.user)
            if user_products.exists() or self.request.user.has_perm('catalog.can_unpublish_product'):
                queryset = Product.objects.all()

        return queryset


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:product_list')

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().owner != request.user:
            raise PermissionDenied("Вы не являетесь владельцем этого продукта")
        return super().dispatch(request, *args, **kwargs)


class ContactView(View):
    def get(self, request):
        return render(request, 'catalog/contact.html')

    def post(self, request):
        return redirect('catalog:contact')


class ProductsListView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            user_products = Product.objects.filter(owner=self.request.user)

            if user_products.exists() or self.request.user.has_perm('catalog.can_unpublish_product'):
                return Product.objects.all()

        return Product.objects.filter(is_published=True)


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:product_list')

    def dispatch(self, request, *args, **kwargs):
        product = self.get_object()
        if not (product.owner == request.user or request.user.has_perm('catalog.can_delete_product')):
            raise PermissionDenied("У вас нет прав на удаление этого продукта")
        return super().dispatch(request, *args, **kwargs)
