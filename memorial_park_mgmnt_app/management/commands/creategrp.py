from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group


class Command(BaseCommand):

    def handle(self, *args, **options):
        grp_names = ['Baliwag', 'San Rafael', 'San Miguel']

        for grp_name in grp_names:
            print('Check if group exists')
            if not Group.objects.filter(name=grp_name).exists():
                print('Creating group: {0}'.format(grp_name))
                Group.objects.create(name=grp_name)
