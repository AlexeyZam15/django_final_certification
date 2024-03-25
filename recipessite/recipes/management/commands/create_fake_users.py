from django.core.management.base import BaseCommand
from django.utils import lorem_ipsum

from django.contrib.auth.models import User

import random


class Command(BaseCommand):
    help = 'Create fake n users'

    def add_arguments(self, parser):
        parser.add_argument('n', type=int, help='Number of users to create')

    def handle(self, *args, **options):
        if User.objects.count() == 0:
            last_id = 1
        else:
            last_id = User.objects.last().id + 1
        count = options['n']
        data = [User(
            username=f'user{last_id + i}',
            password='123456',
            email=f'user{last_id + i}@example.com')
            for i in range(count)]
        User.objects.bulk_create(data)
        self.stdout.write(self.style.SUCCESS(f'{count} fake users created'))
        return
