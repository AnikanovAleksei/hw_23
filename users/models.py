from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Email')
    avatar = models.ImageField(upload_to='users/avatars/', blank=True, null=True)
    phone_number = models.CharField(max_length=15, verbose_name='Номер телефона', blank=True, null=True,
                                    help_text='Введите номер телефона')
    country = models.CharField(max_length=20, verbose_name='Страна', null=True, blank=True, help_text='Укажите страну')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email
