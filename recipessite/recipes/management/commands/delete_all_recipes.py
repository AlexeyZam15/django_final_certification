from django.core.management.base import BaseCommand

from recipes.models import Recipe


class Command(BaseCommand):
    help = 'Delete all recipes'

    def handle(self, *args, **options):
        if Recipe.objects.count() == 0:
            self.stdout.write(self.style.SUCCESS('No recipes found'))
            return
        Recipe.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('All recipes deleted'))
        return
