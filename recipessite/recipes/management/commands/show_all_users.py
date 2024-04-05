from django.core.management.base import BaseCommand

from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Show all no staff users'

    def handle(self, *args, **options):
        users = User.objects.filter(is_staff=False)
        for user in users:
            print(user)
        print(f'Total: {len(users)}')
        return
