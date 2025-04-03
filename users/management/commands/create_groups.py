from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product


class Command(BaseCommand):
    help = 'Creates moderator group with permissions'

    def handle(self, *args, **options):
        # Создаем группу
        group, created = Group.objects.get_or_create(name="Модераторы")

        if created:
            # Получаем разрешения из модели Product
            content_type = ContentType.objects.get_for_model(Product)

            permissions = [
                'can_unpublish_product',
                'can_delete_product'
            ]

            # Добавляем разрешения в группу
            for codename in permissions:
                perm = Permission.objects.get(
                    content_type=content_type,
                    codename=codename
                )
                group.permissions.add(perm)

            self.stdout.write(self.style.SUCCESS('Группа модераторов создана'))
        else:
            self.stdout.write(self.style.WARNING('Группа модераторов уже существует'))
