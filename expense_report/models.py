from django.db import models
from django.utils import timezone

# Create your models here.

CATEGORIES = (('Salaries', 'Salaries'),
              ('Commissions', 'Commissions'),
              ('Labor Fees', 'Labor Fees'),
              ('Professional Fees', 'Professional Fees'),
              ('Allowance', 'Allowance'),
              ('Repair & Maintenance', 'Repair and Maintenance'),
              ('Office Supplies', 'Office Supplies'),
              ('Transportation', 'Transportation'),
              ('Electicity', 'Electicity'),
              ('Utilities', 'Utilities'),
              ('Miscellaneous', 'Miscellaneous'))


class Expense(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    date = models.DateField(null=False, blank=False, default=timezone.now)
    reference_number = models.CharField(max_length=256, blank=True, null=True)
    payee = models.CharField(max_length=256, blank=False, null=False)
    amount = models.FloatField(default=0.01)
    category = models.CharField(max_length=128, blank=False, null=False, choices=CATEGORIES, default='Salaries')
    description = models.CharField(max_length=512, blank=True, null=True)

    def __str__(self):
        text = self.payee
        if self.reference_number:
            text = '{0}: {1}'.format(self.reference_number, self.payee)
        return text
