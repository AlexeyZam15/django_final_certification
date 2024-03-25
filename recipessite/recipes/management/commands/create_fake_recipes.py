from datetime import time

from django.core.management.base import BaseCommand
from django.utils import lorem_ipsum

from recipes.models import Recipe

from django.contrib.auth.models import User

import random


class Command(BaseCommand):
    help = 'Create fake n recipes'

    def add_arguments(self, parser):
        parser.add_argument('n', type=int, help='Number of recipes to create')

    def handle(self, *args, **options):
        if Recipe.objects.exists():
            last_id = Recipe.objects.last().id + 1
        else:
            last_id = 1
        users = User.objects.all()
        """
        Генерация следующий полей для модели рецепты:
        title = models.CharField(max_length=100, unique=True, verbose_name='Название')
        description = models.TextField(max_length=1000, verbose_name='Описание')
        steps = models.TextField(max_length=1000, verbose_name='Шаги приготовления')
        time = models.TimeField(verbose_name='Время приготовления')
        author = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name='Автор')
        created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
        changed_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    """
        data = [Recipe(
            title=f'Рецепт {last_id + i}',
            description=lorem_ipsum.paragraph(),
            steps=lorem_ipsum.paragraph(),
            time=time(hour=random.randint(0, 12), minute=random.randint(1, 59)),
            author=random.choice(users),
        ) for i in range(options['n'])]
        Recipe.objects.bulk_create(data)
        self.stdout.write(self.style.SUCCESS(f'{options["n"]} fake recipes created'))
        return
