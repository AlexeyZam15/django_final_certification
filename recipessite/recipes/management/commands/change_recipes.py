from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import lorem_ipsum

from recipes.models import Recipe

import random


class Command(BaseCommand):
    help = 'Random change fake recipes'

    def handle(self, *args, **options):
        change_count = 0
        for recipe in Recipe.objects.all():
            if random.randint(0, 2) == 0:
                change_count += 1
                recipe.description = lorem_ipsum.paragraph()
                recipe.steps = lorem_ipsum.paragraph()
                recipe.time = timedelta(minutes=random.randint(1, 60))
                recipe.save()
        self.stdout.write(self.style.SUCCESS(f'Changed {change_count} recipes'))
        return
