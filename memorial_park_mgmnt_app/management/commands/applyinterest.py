from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from memorial_park_mgmnt_app.models import Bill

class Command(BaseCommand):

    def add_arguments(self, parser):

        parser.add_argument(
            'date',
            action='store',
            help='format: YYYY-MM-DD | Bills with due date not later than this will be considered overdue'
        )

    def handle(self, *args, **options):
        date = datetime.strptime(options.get('date'), '%Y-%m-%d')
        overdue_bills = Bill.objects.filter(due_date__lt=date)

        for bill in overdue_bills.order_by('due_date'):
            if not bill.is_paid and bill.interest < 1:
                last_bill = bill.contract.bills.filter(due_date__lt=bill.due_date).order_by('-due_date').first()

                if last_bill:
                    bill.interest = last_bill.balance * 0.02
                    bill.save()
                    print('{0} >>> {1}'.format(str(bill), bill.interest))