from django.core.management.base import BaseCommand

from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Delete all no staff users'

    def handle(self, *args, **options):
        users = User.objects.filter(is_staff=False)
        if not users:
            print(f'No no staff users to delete')
            return
        users.delete()
        print(f'All no staff users deleted')
        return
