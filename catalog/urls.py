from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import home, contact, product_list, product_detail


app_name = CatalogConfig.name

urlpatterns = [
    path('home/', home, name='home'),
    path('contacts/', contact, name='contact'),
    path('products/', product_list, name='product_list'),
    path('product/<int:pk>/', product_detail, name='product_detail'),
]
