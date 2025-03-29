from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden

from catalog.models import Product
from catalog.forms import ProductForm

from django.urls import reverse_lazy


class ReviewProductView(LoginRequiredMixin, View):
    def post(self, request, pk):
        product = get_object_or_404(Product, id=pk)

        if not (request.user == product.owner or request.user.has_perm('catalog.can_unpublish_product')):
            return HttpResponseForbidden('У вас нет прав для этого действия')

        if 'unpublish' in request.POST:
            product.is_published = False
            product.save()
            return redirect('catalog:product_list')

        if 'publish' in request.POST:
            if request.user != product.owner:
                return HttpResponseForbidden('Только владелец может опубликовать товар')
            product.is_published = True
            product.save()
            return redirect('catalog:product_list')

        if 'delete' in request.POST:
            if not (request.user == product.owner or request.user.has_perm('catalog.can_delete_product')):
                return HttpResponseForbidden('У вас нет прав на удаление продукта')
            product.delete()
            return redirect('catalog:product_list')

        return redirect('catalog:product_list')


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
            return Product.objects.filter(is_published=True)
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
