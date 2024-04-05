from django.core.management.base import BaseCommand

from recipes.models import Recipe


class Command(BaseCommand):
    help = 'Show all recipes'

    def handle(self, *args, **options):
        recipes = Recipe.objects.all()
        for recipe in recipes:
            print(recipe)
        print(f'Total recipes: {recipes.count()}')
        return
