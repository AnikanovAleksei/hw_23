from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import (HomeListView, ContactView, ProductDetailView, ProductsListView, ProductCreateView,
                           ProductUpdateView, ProductDeleteView, PublishProductView, UnpublishProductView,
                           ProductListByCategoryView)

app_name = CatalogConfig.name

urlpatterns = [
    path('home/', HomeListView.as_view(), name='home'),
    path('contacts/', ContactView.as_view(), name='contact'),
    path('products/', ProductsListView.as_view(), name='product_list'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/create/', ProductCreateView.as_view(), name='product_create'),
    path('product/update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('product/delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),
    path('product/<int:product_id>/publish/', PublishProductView.as_view(), name='product_publish'),
    path('product/<int:product_id>/unpublish/', UnpublishProductView.as_view(), name='product_unpublish'),
    path('category/<int:category_id>/', ProductListByCategoryView.as_view(), name='product_list_by_category'),
]
