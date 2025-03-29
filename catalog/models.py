from django.db import models

from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Наименование")
    description = models.TextField(verbose_name='Описание')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Наименование")
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='media/images', verbose_name='Изображение')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория',
                                 related_name='products')
    price = models.IntegerField(verbose_name='Цена за покупку')
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    update_at = models.DateField(auto_now=True, verbose_name='Дата последнего изменения')
    is_published = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Владелец')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        permissions = [
            ("can_unpublish_product", "Can unpublish product"),
            ("can_delete_product", "Can delete product"),
        ]

    def __str__(self):
        return self.name
