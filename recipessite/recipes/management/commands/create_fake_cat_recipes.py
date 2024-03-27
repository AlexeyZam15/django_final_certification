import random

from django.core.management.base import BaseCommand

from recipes.models import Recipe, Category, RecipeCategory


class Command(BaseCommand):
    help = 'Create fake random RecipeCategory for each non-category recipe'

    def handle(self, *args, **options):
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
        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(data)} fake RecipeCategories'))
        return
