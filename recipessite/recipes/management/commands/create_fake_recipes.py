from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import lorem_ipsum

from recipes.models import Recipe, RecipeCategory, Category

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
        time = models.DurationField(verbose_name='Время приготовления')
        image = models.FileField(upload_to='photos', blank=True, null=True, verbose_name='Изображение')
        author = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name='Автор')
        created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
        changed_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    """
        data = [Recipe(
            title=f'Рецепт {last_id + i}',
            description=lorem_ipsum.paragraph(),
            steps=lorem_ipsum.paragraph(),
            time=timedelta(minutes=random.randint(1, 60)),
            author=random.choice(users),
        ) for i in range(options['n'])]
        Recipe.objects.bulk_create(data)

        recipes = filter(lambda x: not x.category, Recipe.objects.all())
        categories = Category.objects.all()

        data = [RecipeCategory(
            recipe=recipe,
            category=random.choice(categories))
            for recipe in recipes]
        if not data:
            self.stdout.write(self.style.WARNING('No recipes without category found'))
            return
        RecipeCategory.objects.bulk_create(data)

        self.stdout.write(self.style.SUCCESS(f'{options["n"]} fake recipes created'))
        return
