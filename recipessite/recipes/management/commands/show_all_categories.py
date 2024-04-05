from django.core.management.base import BaseCommand

from recipes.models import Category


class Command(BaseCommand):
    help = 'Show all categories'

    def handle(self, *args, **options):
        categories = Category.objects.all()
        for category in categories:
            print(category)
        print(f'Total categories: {categories.count()}')
        return
