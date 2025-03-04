from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import HomeListView, ContactView, ProductDetailView, ProductsListView


app_name = CatalogConfig.name

urlpatterns = [
    path('home/', HomeListView.as_view(), name='home'),
    path('contacts/', ContactView.as_view(), name='contact'),
    path('products/', ProductsListView.as_view(), name='product_list'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
]
