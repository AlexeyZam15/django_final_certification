from django.core.management.base import BaseCommand
from django.utils import lorem_ipsum

from recipes.models import Category

import random


class Command(BaseCommand):
    help = 'Create fake n categories'

    def add_arguments(self, parser):
        parser.add_argument('n', type=int, help='Number of categories to create')

    def handle(self, *args, **options):
        n = options['n']
        if Category.objects.count() == 0:
            last_id = 1
        else:
            last_id = Category.objects.last().id + 1
        """Генерация полей для модели Категории:
        title = models.CharField(max_length=255, unique=True, verbose_name='Название')
        description = models.TextField(max_length=1000, verbose_name='Описание')
        """
        data = [Category(
            title=f'Category {last_id + i}',
            description=lorem_ipsum.paragraph())
            for i in range(n)]
        Category.objects.bulk_create(data)
        self.stdout.write(self.style.SUCCESS('Successfully created %s categories' % n))
        return
