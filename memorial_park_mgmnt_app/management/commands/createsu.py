from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        print('Check if user exists')
        if not User.objects.filter(username='admin').exists():
            print('Creating super user')
            User.objects.create_superuser(username='admin',
                                          password='admin1234',
                                          email='johnjabola@gmail.com')
