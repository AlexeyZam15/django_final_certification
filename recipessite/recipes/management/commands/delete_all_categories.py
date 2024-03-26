from django.core.management.base import BaseCommand

from recipes.models import Category


class Command(BaseCommand):
    help = 'Delete all categories'

    def handle(self, *args, **options):
        if Category.objects.count() == 0:
            self.stdout.write(self.style.SUCCESS('No categories found'))
            return
        Category.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('All categories deleted'))
        return
