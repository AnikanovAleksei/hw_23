from .models import Category, Product

from .models import Product, Category


class CategoryService:

    @staticmethod
    def get_products_by_category(category_id):
        category = Category.objects.get(id=category_id)
        return Product.objects.filter(category=category)
