import os
import uuid
from datedelta import datedelta
from datetime import date, datetime, timedelta

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.core import exceptions

# Constants
# LOT_TYPES = (('SPL', 'Special'),
#              ('REG', 'Regular'))

BUYER_TYPES = (('PRE-NEED', 'Pre-Need'),
               ('AT-NEED', 'At-Need'))

CONTRACT_STATUSES = (('NEW', 'New'),
                     ('REVIEWED', 'Reviewed'),
                     ('FORFEITED', 'Forfeited'))

PAYMENT_TERMS = (('SPOT', 'Spot'),
                 ('INSTALLMENT', 'Installment'))

AGENT_TYPES = (('SALES_AGENT', 'Sales Agent'),
               ('UNIT_MNGR', 'Unit Manager'),
               ('SALES_LEADER', 'Sales Leader'),
               ('REFERENT', 'Referent'))

SERVICE_TYPES = (('CERTIFICATE_OF_OWNERSHIP', 'Certificate of Ownership'),
                 ('CHANGE_OF_TITLE', 'Change of Title'),
                 ('CHANGE_OF_LOT', 'Change of Lot'),
                 ('INTERMENT', 'Interment'),
                 ('OTHERS', 'Others'))

CONTRACT_STATUSES = (('NEW', 'New'),
                     ('REVIEWED', 'Reviewed'),
                     ('FORFEITED', 'Forfeited'))

BILL_TYPES = (('SPOT', 'Spot'),
             ('DOWNPAYMENT', 'Downpayment'),
             ('INSTALLMENT', 'Installment'),
             ('OTHERS', 'Others'))

BILL_STATUSES = (('NEW', 'New'),
                 ('PAID', 'Paid'),
                 ('OVERDUE', 'Overdue'))

PAYMENT_TYPES = (('CASH', 'Cash'),
                 ('CHECK', 'Check'),
                 ('OTHERS', 'Others'))

def valid_id_directory_path(instance, filename):
    ext  = os.path.splitext(filename)[1]
    uid = uuid.uuid4().hex
    return '{model}_ids/{uid}_{name}{ext}'.format(model=type(instance)._meta.verbose_name.lower(),
                                                  uid=uid,
                                                  name=str(instance).title().replace(' ', ''),
                                                  ext=ext)

def one_year_from_today():
    pst = datetime.utcnow() + timedelta(hours=8)
    nxt_year = pst + datedelta(years=1)

    return nxt_year.date()

class Branch(models.Model):
    name = models.CharField(max_length=128, null=False, blank=False)
    address = models.CharField(max_length=512, null=True, blank=True)
    group = models.OneToOneField(Group, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Branches'


class LotType(models.Model):
    lot_type = models.CharField(max_length=32, blank=False, null=False, default='REG')
    price = models.FloatField(null=False, blank=False, default=0.00)
    vat = models.FloatField(null=False, blank=False, default=0.00)
    care_fund = models.FloatField(null=False, blank=False, default=0.00)

    def __str__(self):
        return self.lot_type


class Lot(models.Model):
    block = models.CharField(max_length=32, blank=False, null=False)
    lot = models.CharField(max_length=32, blank=False, null=False)
    unit = models.CharField(max_length=32, blank=False, null=False)

    lot_type = models.ForeignKey(LotType, null=False, blank=False, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, null=True, blank=True, related_name='lots', on_delete=models.SET_NULL)

    class Meta:
        unique_together = ('block', 'lot', 'unit')

    def __str__(self):
        return 'B{0}-LOT{1}{2}'.format(self.block, self.lot, self.unit)


class Agent(models.Model):
    last_name = models.CharField(max_length=56, blank=False, null=False)
    first_name = models.CharField(max_length=56, blank=False, null=False)
    middle_name = models.CharField(max_length=56, blank=True, null=True)
    rank = models.CharField(max_length=56, blank=False, null=False, choices=AGENT_TYPES, default='SALES_AGENT')

    mobile = models.CharField(max_length=18, blank=True, null=True)
    landline = models.CharField(max_length=18, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    # Address
    house_number = models.CharField(max_length=8, blank=True, null=True)
    street = models.CharField(max_length=128, blank=True, null=True)
    barangay = models.CharField(max_length=128, blank=True, null=True)
    town = models.CharField(max_length=128, blank=True, null=True)
    province = models.CharField(max_length=128, blank=True, null=True)

    valid_id = models.FileField(upload_to=valid_id_directory_path, blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)
    other_address = models.CharField(max_length=512, blank=True, null=True)
    business_name = models.CharField(max_length=512, blank=True, null=True)
    business_address = models.CharField(max_length=512, blank=True, null=True)

    class Meta:
        unique_together = ('last_name', 'first_name')

    def __str__(self):
        fullname = '{0} {1}'.format(self.last_name, self.first_name)
        if self.middle_name:
            fullname = '{0} {1} {2}'.format(self.last_name, self.first_name, self.middle_name)
        return fullname

    @property
    def contact_number(self):
        if self.mobile:
            return self.mobile
        elif self.landline:
            return self.landline
        else:
            return ''


    @property
    def main_address(self):
        addr = '{barangay}, {town}, {province}'.format(barangay=self.barangay or '', 
                                                       town=self.town or '', 
                                                       province=self.province or '')
        if self.street:
            addr = '{street}, {address}'.format(street=self.street, address=addr)
        if self.house_number:
            addr = '{house_number} {address}'.format(house_number=self.house_number, address=addr)

        return addr


class Client(models.Model):
    last_name = models.CharField(max_length=56, blank=False, null=False)
    first_name = models.CharField(max_length=56, blank=False, null=False)
    middle_name = models.CharField(max_length=56, blank=True, null=True)

    mobile = models.CharField(max_length=18, blank=True, null=True)
    landline = models.CharField(max_length=18, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    # Address
    house_number = models.CharField(max_length=8, blank=True, null=True)
    street = models.CharField(max_length=128, blank=True, null=True)
    barangay = models.CharField(max_length=128, blank=False, null=False)
    town = models.CharField(max_length=128, blank=False, null=False)
    province = models.CharField(max_length=128, blank=False, null=False)

    valid_id = models.FileField(upload_to=valid_id_directory_path, blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)
    other_address = models.CharField(max_length=512, blank=True, null=True)
    business_name = models.CharField(max_length=512, blank=True, null=True)
    business_address = models.CharField(max_length=512, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    branch = models.ForeignKey(Branch, null=True, blank=True, related_name='clients', on_delete=models.SET_NULL)

    class Meta:
        unique_together = ('last_name', 'first_name')

    def __str__(self):
        fullname = '{0} {1}'.format(self.last_name, self.first_name)
        if self.middle_name:
            fullname = '{0} {1} {2}'.format(self.last_name, self.first_name, self.middle_name)
        return fullname

    @property
    def main_address(self):
        addr = '{barangay}, {town}, {province}'.format(barangay=self.barangay, town=self.town, province=self.province)
        if self.street:
            addr = '{street}, {address}'.format(street=self.street, address=addr)
        if self.house_number:
            addr = '{house_number} {address}'.format(house_number=self.house_number, address=addr)

        return addr

    @property
    def contact_number(self):
        if self.mobile:
            return self.mobile
        elif self.landline:
            return self.landline
        else:
            return ''


class DownpaymentPromo(models.Model):
    name = models.CharField(max_length=256, blank=False, null=False)
    split = models.PositiveSmallIntegerField(default=1)
    discount = models.FloatField(blank=False, null=False, default=0.00)

    start_date = models.DateField(null=False, blank=False, default=date.today)
    end_date = models.DateField(null=False, blank=False, default=one_year_from_today)

    def __str__(self):
        return '{0}: {1}% OFF'.format(self.name, int(self.discount * 100))


class InstallmentPromo(models.Model):
    name = models.CharField(max_length=256, blank=False, null=False)
    months = models.PositiveSmallIntegerField(default=12)
    interest = models.FloatField(blank=False, null=False, default=0.00)

    start_date = models.DateField(null=False, blank=False, default=date.today)
    end_date = models.DateField(null=False, blank=False, default=one_year_from_today)

    def __str__(self):
        return '{0}: {1}% INTEREST'.format(self.name, int(self.interest * 100))


class SpotPromo(models.Model):
    discount = models.FloatField(blank=False, null=False, default=0.15)
    start_date = models.DateField(null=False, blank=False, default=date.today)
    end_date = models.DateField(null=False, blank=False, default=one_year_from_today)

    def __str__(self):
        return 'Spot | {0}% OFF'.format(int(self.discount * 100))


class Contract(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)

    number = models.CharField(max_length=256, blank=False, null=False, unique=True)
    date = models.DateField(null=False, blank=False, default=date.today)
    buyer_type = models.CharField(max_length=32, blank=False, null=False, choices=BUYER_TYPES, default='PRE-NEED')

    status = models.CharField(max_length=64, blank=False, null=False, choices=CONTRACT_STATUSES, default='NEW')
    remarks = models.CharField(max_length=256, blank=True, null=True)

    reservation = models.FloatField(blank=False, null=False, default=0.00)
    payment_terms = models.CharField(max_length=256, blank=False, null=False, choices=PAYMENT_TERMS, default='SPOT')

    lot = models.ForeignKey(Lot, null=False, blank=False, related_name='lot_contracts', on_delete=models.CASCADE)
    price = models.FloatField(null=False, blank=False, default=0.00)
    vat = models.FloatField(null=False, blank=False, default=0.00)
    care_fund = models.FloatField(null=False, blank=False, default=0.00)

    client = models.ForeignKey(Client, null=False, blank=False, related_name='client_contracts', on_delete=models.CASCADE)

    # Commission = 7%
    sales_agent = models.ForeignKey(Agent, null=True, blank=True, related_name='sales_agent_contracts', on_delete=models.SET_NULL)
    # Commission = 1%
    unit_manager = models.ForeignKey(Agent, null=True, blank=True, related_name='unit_manager_contracts', on_delete=models.SET_NULL)
    # Commission = 1%
    sales_leader = models.ForeignKey(Agent, null=True, blank=True, related_name='sales_leader_contracts', on_delete=models.SET_NULL)
    # Referral
    referent = models.ForeignKey(Agent, null=True, blank=True, related_name='referral_contracts', on_delete=models.SET_NULL)

    # Scenario helpers
    sold_by = models.CharField(max_length=32, blank=False, null=False, choices=AGENT_TYPES, default='SALES_AGENT')

    def __str__(self):
        return '{0} - {1}'.format(str(self.client), str(self.lot))

    def save(self, **kwargs):
        self.clean()
        return super(Contract, self).save(**kwargs)

    def clean(self):
        super(Contract, self).clean()
        if self._state.adding and self.pk is None:
            qs = self.lot.lot_contracts.filter(status__in=['NEW', 'REVIEWED'])
            if qs.exists():
                error = {'lot': 'Lot is already under an active contract'}
                raise exceptions.ValidationError(error)

    @property
    def installment_amount(self):
        installment = (self.price + self.care_fund) * 0.8
        if self.installment_option:
            installment = installment + (installment * self.installment_option.interest)

        return installment

    @property
    def installment_monthly(self):
        monthly = self.installment_amount
        if self.installment_option:
            monthly = self.installment_amount / (self.installment_option.months)

        return monthly

    @property
    def installment_paid(self):
        paid = 0
        for bill in self.bills.all():
            bill_paid = 0
            for payment in bill.payments.filter(payment_type='INSTALLMENT'):
                bill_paid = bill_paid + payment.amount

            if bill_paid < bill.amount_due:
                paid = paid + bill_paid
            else:
                paid = paid + bill.amount_due

        return paid

    @property
    def installment_balance(self):
        return self.installment_amount - self.installment_paid

    @property
    def downpayment_amount(self):
        downpayment = (self.price + self.care_fund) * 0.2
        if self.installment_option:
            downpayment = downpayment - (downpayment * self.installment_option.discount)

        return downpayment

    @property
    def downpayment_monthly(self):
        monthly = self.downpayment_amount
        if self.installment_option:
            monthly = self.downpayment_amount / (self.installment_option.split)

        return monthly

    @property
    def downpayment_paid(self):
        paid = 0
        for bill in self.bills.all():
            bill_paid = 0
            for payment in bill.payments.filter(payment_type='DOWNPAYMENT'):
                bill_paid = bill_paid + payment.amount

            if bill_paid < bill.amount_due:
                paid = paid + bill_paid
            else:
                paid = paid + bill.amount_due

        return paid

    @property
    def downpayment_balance(self):
        return self.downpayment_amount - self.downpayment_paid

    @property
    def contract_price(self):
        if self.buyer_type == 'AT-NEED':
            ### AT-NEED ###
            return self.price + (self.price * 0.5) + self.care_fund
        else:
            ### PRE-NEED ###
            if self.payment_terms == 'SPOT':
                discount = 0
                if hasattr(self, 'spot_option'):
                    discount = (self.price + self.care_fund) * self.spot_option.discount
                return self.price + self.care_fund - discount
            else:
                return self.downpayment_amount + self.installment_amount

    @property
    def total_payment(self):
        total = 0
        for bill in self.bills.all():
            for payment in bill.payments.all():
                total = total + payment.amount

        return total

    @property
    def commissionable_amount(self):
        if self.payment_terms == 'SPOT':
            discount = 0
            if self.spot_option:
                discount = (self.price + self.care_fund) * self.spot_option.discount

            gross = self.price - discount
            vat = gross - (gross / 1.12)
            net = gross - vat

            gross_commission = net * 0.07
            net_commission = gross_commission - (gross_commission * 0.1)

            return net_commission
        else:
            discount = 0
            if self.installment_option:
                discount = ((self.price + self.care_fund) * 0.2) * self.installment_option.discount

            gross = self.price - discount
            vat = gross - (gross / 1.12)
            net = gross - vat

            gross_commission = net * 0.07
            net_commission = gross_commission - (gross_commission * 0.1)

            return net_commission

    @property
    def commission_monthly(self):
        monthly = self.commissionable_amount
        if self.downpayment_option:
            monthly = self.downpayment_amount / (self.downpayment_option.split)

        return monthly

    # @property
    # def next_due_date(self):
    #     pst = datetime.utcnow() + timedelta(hours=8)
    #     for bill in self.bills.filter(due_date__gte=pst).order_by('due_date'):
    #         if not bill.is_paid:
    #             return bill.due_date

    #     return None

    # @property
    # def last_due_date(self):
    #     pst = datetime.utcnow() + timedelta(hours=8)
    #     for bill in self.bills.filter(due_date__lte=pst).order_by('-due_date'):
    #         if not bill.is_paid:
    #             return bill.due_date

    #     return None

    @property
    def due_date(self):
        due_date = None
        pst = datetime.utcnow() + timedelta(hours=8)

        for bill in self.bills.filter(due_date__lte=pst).order_by('-due_date'):
            if not bill.is_paid:
                due_date = bill.due_date
                break

        # Advanced payments
        if not due_date:
            for bill in self.bills.filter(due_date__gte=pst).order_by('due_date'):
                if not bill.is_paid:
                    due_date = bill.due_date
                    break

        return due_date

    @property
    def amount_due(self):
        amount_due = 0

        if self.due_date:
            for bill in self.bills.filter(due_date__lte=self.due_date):
                if not bill.is_paid:
                    amount_due = amount_due + bill.balance

        return amount_due

    @property
    def is_overdue(self):
        pst = datetime.utcnow() + timedelta(hours=8)
        if self.due_date and self.due_date < pst.date():
            return True
    
        return False

    @property
    def is_complete(self):
        for bill in self.bills.all():
            if not bill.is_paid:
                return False

        return True

    def get_commissions(self):
        base = self.commissionable_amount
        commissions = {
                'sales_agent': 0,
                'unit_manager': 0,
                'sales_leader': 0,
                'referent': 0
            }

        if self.sold_by == 'SALES_AGENT':
            # Scenario 1
            if self.unit_manager is not None:
                commissions = {
                    'sales_agent': base * 0.07,
                    'unit_manager': base * 0.01,
                    'sales_leader': base * 0.01,
                    'referent': 0
                }
            # Scenario 4
            else:
                commissions = {
                    'sales_agent': base * 0.07,
                    'unit_manager': 0,
                    'sales_leader': base * 0.01 + base * 0.01,
                    'referent': 0
                }
        # Scenario 2
        elif self.sold_by == 'UNIT_MNGR':
            commissions = {
                'sales_agent': 0,
                'unit_manager': base * 0.07 + base * 0.01,
                'sales_leader': base * 0.01,
                'referent': 0
            }
        # Scenario 3
        elif self.sold_by == 'SALES_LEADER':
            commissions = {
                'sales_agent': 0,
                'unit_manager': 0,
                'sales_leader': base * 0.07 + base * 0.01 + base * 0.01,
                'referent': 0
            }
        # Scenario 5
        elif self.sold_by == 'REFERENT':
            commissions = {
                'sales_agent': base * 0.01,
                'unit_manager': 0,
                'sales_leader': 0,
                'referent': base * 0.07
            }

        return commissions

    def get_monthly_commissions(self):
        commissions = self.get_commissions()
        if self.installment_option:
            for key in list(commissions.keys()):
                commissions[key] = commissions[key] / self.installment_option.split

        return commissions


class SpotOption(models.Model):
    discount = models.FloatField(blank=False, null=False, default=0.15)
    contract = models.OneToOneField(Contract, blank=True, null=True, related_name='spot_option', on_delete=models.CASCADE)


class InstallmentOption(models.Model):
    # Downpayment
    split = models.PositiveSmallIntegerField(blank=False, null=False, default=1)
    discount = models.FloatField(blank=False, null=False, default=0.00)

    # Installment
    months = models.PositiveSmallIntegerField(blank=False, null=False, default=12)
    interest = models.FloatField(blank=False, null=False, default=0.00)

    contract = models.OneToOneField(Contract, blank=True, null=True, related_name='installment_option', on_delete=models.CASCADE)


class Service(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    date = models.DateField(null=False, blank=False, default=date.today)
    amount = models.FloatField(null=False, blank=False, default=0.00)
    service_type = models.CharField(max_length=256, blank=True, null=True, choices=SERVICE_TYPES, default='INTERMENT')
    remarks = models.CharField(max_length=256, blank=True, null=True)

    contract = models.ForeignKey(Contract, null=False, blank=False, related_name='services', on_delete=models.CASCADE)

    def __str__(self):
        return '{0} {1}'.format(self.service_type, self.amount)


class Bill(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    start = models.DateField(null=False, blank=False, default=date.today)
    end = models.DateField(null=False, blank=False, default=date.today)

    bill_type = models.CharField(max_length=64, null=False, blank=False, choices=BILL_TYPES, default='SPOT')
    # 5 days before contract date
    issue_date = models.DateField(null=False, blank=False, default=date.today)
    # Same day as contract date
    due_date = models.DateField(null=False, blank=False, default=date.today)

    amount_due = models.FloatField(null=False, blank=False, default=0.00)
    interest = models.FloatField(null=False, blank=False, default=0.00)
    status = models.CharField(max_length=64, blank=False, null=False, choices=BILL_STATUSES, default='NEW')

    remarks = models.CharField(max_length=256, blank=True, null=True)

    contract = models.ForeignKey(Contract, null=False, blank=False, related_name='bills', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('contract', 'issue_date')

    def __str__(self):
        return '{0}: {1} - {2}'.format(str(self.contract),
                                       self.start.strftime('%b %d, %Y'),
                                       self.end.strftime('%b %d, %Y'))

    def save(self, **kwargs):
        self.clean()
        return super(Bill, self).save(**kwargs)

    def clean(self):
        super(Bill, self).clean()
        if self.end < self.start:
            error = {'end': 'End cannot be earlier than start.'}
            raise exceptions.ValidationError(error)

    @property
    def total_amount_paid(self):
        paid = 0
        for payment in self.payments.all():
            paid = paid + payment.amount

        return paid

    @property
    def total_amount_due(self):
        return self.amount_due + self.interest

    @property
    def is_paid(self):
        if self.total_amount_paid < self.total_amount_due:
            return False

        return True

    @property
    def is_overdue(self):
        if not self.is_paid:
            pst = datetime.utcnow() + timedelta(hours=8)
            if pst.date() > self.due_date:
                return True

        return False

    @property
    def balance(self):
        if self.is_paid:
            return 0
        else:
            return self.total_amount_due - self.total_amount_paid

    # @property
    # def interest(self):
    #     interest = 0

    #     bills = self.contract.bills.filter(issue_date__lt=self.issue_date)
    #     last_bill = bills.order_by('-issue_date').first()

    #     if last_bill and last_bill.is_overdue:
    #         interest = last_bill.balance * 0.02

    #     return interest


class Receipt(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    number = models.CharField(max_length=256, blank=False, null=False, unique=True)
    date = models.DateField(null=False, blank=False, default=date.today)
    amount = models.FloatField(null=False, blank=False, default=0.00)
    payment_type = models.CharField(max_length=32, blank=False, null=False, choices=PAYMENT_TYPES, default='CASH')
    remarks = models.CharField(max_length=256, blank=True, null=True)

    branch = models.ForeignKey(Branch, null=True, blank=True, related_name='receipts', on_delete=models.SET_NULL)

    def __str__(self):
        return self.number


class Payment(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    date = models.DateField(null=False, blank=False, default=date.today)
    amount = models.FloatField(null=False, blank=False, default=0.00)
    remarks = models.CharField(max_length=256, blank=True, null=True)

    bill = models.ForeignKey(Bill, null=False, blank=False, related_name='payments', on_delete=models.CASCADE)
    receipt = models.ForeignKey(Receipt, null=False, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return '{0}: {1:.2f}'.format(self.receipt.number, self.amount)

class Commission(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    amount = models.FloatField(null=False, blank=False, default=0.00)
    release_date = models.DateField(null=True, blank=True)

    bill = models.ForeignKey(Bill, null=False, blank=False, on_delete=models.CASCADE)
    agent = models.ForeignKey(Agent, null=False, blank=False, on_delete=models.CASCADE)
