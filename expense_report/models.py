from django.db import models
from django.utils import timezone
from django.db.models import Sum

# Create your models here.

CATEGORIES = (('Salaries', 'Salaries'),
              ('Commissions', 'Commissions'),
              ('Petty Cash Replenishment', 'Petty Cash Replenishment'),
              ('Labor Fees', 'Labor Fees'),
              ('Professional Fees', 'Professional Fees'),
              ('Allowance', 'Allowance'),
              ('Repair & Maintenance', 'Repair and Maintenance'),
              ('Office Supplies', 'Office Supplies'),
              ('Transportation', 'Transportation'),
              ('Electicity', 'Electicity'),
              ('Utilities', 'Utilities'),
              ('Miscellaneous', 'Miscellaneous'))

CREDIT = 1
DEBIT = -1
TRANSACTION_TYPES = ((CREDIT, 'CREDIT'),
                     (DEBIT, 'DEBIT'))

class Expense(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    date = models.DateField(null=False, blank=False, default=timezone.now)
    reference_number = models.CharField(max_length=256, blank=True, null=True)
    payee = models.CharField(max_length=256, blank=False, null=False)
    amount = models.FloatField(default=0.00)
    category = models.CharField(max_length=128, blank=False, null=False, choices=CATEGORIES, default='Salaries')
    description = models.CharField(max_length=512, blank=True, null=True)

    def __str__(self):
        text = self.payee
        if self.reference_number:
            text = '{0}: {1}'.format(self.reference_number, self.payee)
        return text

class Transaction(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    timestamp = models.DateTimeField(null=False, blank=False, default=timezone.now)
    payee = models.CharField(max_length=256, blank=False, null=False)
    amount = models.FloatField(null=False, blank=False, default=0.00)
    description = models.CharField(max_length=512, blank=True, null=True)

    transaction_type = models.SmallIntegerField(null=False, blank=False, choices=TRANSACTION_TYPES, default=DEBIT)
    value = models.FloatField(null=False, blank=False, default=0.00)

    class Meta:
        verbose_name = 'Petty Cash Transaction'
        verbose_name_plural = 'Petty Cash Transactions'

    def __str__(self):
        return '{0}: {1}'.format(self.timestamp.strftime('%Y-%m-%d %I:%M %p'), self.amount)

    @property
    def balance(self):
        query_set = type(self).objects.filter(timestamp__lt=self.timestamp)
        if query_set:
            agg = query_set.aggregate(balance=Sum('value'))
            balance = agg.get('balance', 0) + self.value
        else:
            balance = 0 + self.value

        return balance
