import os
import uuid
from datetime import date, datetime, timedelta

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db.models import Sum
from django.contrib.auth.models import Group

# Constants
# LOT_TYPES = (('SPL', 'Special'),
#              ('REG', 'Regular'))

BUYER_TYPES = (('PRE-NEED', 'Pre-Need'),
               ('IN-NEED', 'In-Need'))

CONTRACT_STATUSES = (('NEW', 'New'),
                     ('REVIEWED', 'Reviewed'),
                     ('FORFEITED', 'Forfeited'))

PAYMENT_TERMS = (('SPOT', 'Spot'),
                 ('INSTALLMENT', 'Installment'))

AGENT_TYPES = (('SALES_AGENT', 'Sales Agent'),
               ('UNIT_MNGR', 'Unit Manager'),
               ('SALES_LEADER', 'Sales Leader'),
               ('REFERRAL', 'Referral'))

SERVICE_TYPES = (('CERTIFICATE_OF_OWNERSHIP', 'Certificate of Ownership'),
                 ('CHANGE_OF_TITLE', 'Change of Title'),
                 ('CHANGE_OF_LOT', 'Change of Lot'),
                 ('INTERMENT', 'Interment'))

PAYMENT_TYPES = (('SPOT_CASH', 'Spot Cash'),
                 ('DOWNPAYMENT', 'Downpayment'),
                 ('INSTALLMENT', 'Installment'),
                 ('OTHERS', 'Others'))

def valid_id_directory_path(instance, filename):
    ext  = os.path.splitext(filename)[1]
    uid = uuid.uuid4().hex
    return '{model}_ids/{uid}_{name}{ext}'.format(model=type(instance)._meta.verbose_name.lower(),
                                                  uid=uid,
                                                  name=str(instance).title().replace(' ', ''),
                                                  ext=ext)

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
    price = models.FloatField(default=0.00)
    vat = models.FloatField(default=0.00)
    care_fund = models.FloatField(default=0.00)

    def __str__(self):
        return self.lot_type


class Lot(models.Model):
    block = models.CharField(max_length=32, blank=False, null=False)
    lot = models.CharField(max_length=32, blank=False, null=False)
    unit = models.CharField(max_length=32, blank=False, null=False)

    price = models.FloatField(default=0.00)
    lot_type = models.ForeignKey(LotType, null=False, blank=False, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, null=True, blank=True, related_name='lots', on_delete=models.SET_NULL)

    def __str__(self):
        return 'B{0}-LOT{1}{2}'.format(self.block, self.lot, self.unit)


class Agent(models.Model):
    last_name = models.CharField(max_length=56, blank=False, null=False)
    first_name = models.CharField(max_length=56, blank=False, null=False)
    middle_name = models.CharField(max_length=56, blank=True, null=True)

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

    branch = models.ForeignKey(Branch, null=True, blank=True, related_name='agents', on_delete=models.SET_NULL)

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


class DownpaymentOption(models.Model):
    name = models.CharField(max_length=256, blank=False, null=False)
    split = models.PositiveSmallIntegerField(default=1)
    discount = models.FloatField(blank=False, null=False, default=0.00)

    def __str__(self):
        return '{0}: {1}% OFF'.format(self.name, (self.discount * 100))


class InstallmentOption(models.Model):
    name = models.CharField(max_length=256, blank=False, null=False)
    months = models.PositiveSmallIntegerField(default=12)
    interest = models.FloatField(blank=False, null=False, default=0.00)

    def __str__(self):
        return '{0}: {1}% INTEREST'.format(self.name, (self.interest * 100))


class SpotOption(models.Model):
    discount = models.FloatField(blank=False, null=False, default=0.15)

    def __str__(self):
        return 'Spot | {0}% OFF'.format(self.discount * 100)


class Promo(models.Model):
    code = models.CharField(max_length=256, blank=False, null=False)
    lot_price = models.FloatField(blank=False, null=False, default=0.00)
    care_fund = models.FloatField(blank=False, null=False, default=0.00)

    start_date = models.DateField(blank=False, null=False, default=date.today)
    end_date = models.DateField(blank=False, null=False, default=date.today)

    def __str__(self):
        return self.code


class Contract(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)

    number = models.CharField(max_length=256, blank=False, null=False)
    date = models.DateField(null=False, blank=False, default=date.today)
    buyer_type = models.CharField(max_length=32, blank=False, null=False, choices=BUYER_TYPES, default='PRE-NEED')

    status = models.CharField(max_length=64, blank=False, null=False, choices=CONTRACT_STATUSES, default='NEW')
    remarks = models.CharField(max_length=256, blank=True, null=True)

    reservation = models.FloatField(default=0.00)
    promo = models.ForeignKey(Promo, blank=True, null=True, on_delete=models.SET_NULL)

    payment_terms = models.CharField(max_length=256, blank=False, null=False, choices=PAYMENT_TERMS, default='SPOT')
    spot_option = models.ForeignKey(SpotOption, blank=True, null=True, on_delete=models.SET_NULL)
    downpayment_option = models.ForeignKey(DownpaymentOption, blank=True, null=True, on_delete=models.SET_NULL)
    installment_option = models.ForeignKey(InstallmentOption, blank=True, null=True, on_delete=models.SET_NULL)

    lot = models.OneToOneField(Lot, null=False, blank=False, related_name='lot_contract', on_delete=models.CASCADE)
    client = models.ForeignKey(Client, null=False, blank=False, related_name='client_contracts', on_delete=models.CASCADE)

    # Commission = 7%
    sales_agent = models.ForeignKey(Agent, null=True, blank=True, related_name='sales_agent_contracts', on_delete=models.SET_NULL)
    # Commission = 1%
    unit_manager = models.ForeignKey(Agent, null=True, blank=True, related_name='unit_manager_contracts', on_delete=models.SET_NULL)
    # Commission = 1%
    sales_leader = models.ForeignKey(Agent, null=True, blank=True, related_name='sales_leader_contracts', on_delete=models.SET_NULL)
    # Referral
    referral = models.ForeignKey(Agent, null=True, blank=True, related_name='referral_contracts', on_delete=models.SET_NULL)

    # Scenario helpers
    sold_by = models.CharField(max_length=32, blank=False, null=False, choices=AGENT_TYPES, default='SALES_AGENT')

    def __str__(self):
        return '{0} - {1}'.format(str(self.client), str(self.lot))

    @property
    def installment_amount(self):
        # base = self.lot.price + self.care_fund
        installment = self.lot.price * 0.8
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
        # base = self.lot.price + self.care_fund
        downpayment = self.lot.price * 0.2
        if self.downpayment_option:
            downpayment = downpayment - (downpayment * self.downpayment_option.discount)

        return downpayment

    @property
    def downpayment_monthly(self):
        monthly = self.downpayment_amount
        if self.downpayment_option:
            monthly = self.downpayment_amount / (self.downpayment_option.split)

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
        lot_price = self.lot.price
        care_fund = self.lot.care_fund

        if self.promo:
            lot_price = self.promo.lot_price
            care_fund = self.promo.care_fund

        if self.buyer_type == 'IN-NEED':
            ### IN-NEED ###
            return lot_price + (self.lot.price * 0.5) + care_fund
        else:
            ### PRE-NEED ###
            if self.contract_type == 'SPOT':
                discount = 0
                if self.spot_option:
                    discount = self.lot.price * self.spot_option.discount
                return lot_price + care_fund - discount
            else:
                return self.downpayment_amount + self.installment_amount + self.care_fund

    @property
    def commissionable_amount(self):
        if self.contract_type == 'SPOT':
            discount = self.lot.price * self.spot_cash.discount

            gross = self.lot.price - discount - self.care_fund
            vat = gross - (gross / 1.12)
            net = gross - vat

            gross_commission = net * 0.07
            net_commission = gross_commission - (gross_commission * 0.1)

            return net_commission
        else:
            discount = 0
            if self.downpayment_option:
                discount = self.lot.price * self.downpayment_option.discount

            gross = self.lot.price - discount - self.care_fund
            vat = gross - (gross / 1.12)
            net = gross - vat

            gross_commission = net * 0.07
            net_commission = gross_commission - (gross_commission * 0.1)

            return net_commission

    @property
    def commission_monthly(self):
        monthly = self.commissionable_amount
        if self.installment_plan:
            monthly = self.downpayment_amount / (self.installment_plan.split)

        return monthly

    def get_commissions(self):
        base = self.commissionable_amount
        commissions = {
                'sales_agent': 0,
                'unit_manager': 0,
                'sales_leader': 0,
                'referral': 0
            }

        if self.sold_by == 'SALES_AGENT':
            # Scenario 1
            if self.unit_manager is not None:
                commissions = {
                    'sales_agent': base * 0.07,
                    'unit_manager': base * 0.01,
                    'sales_leader': base * 0.01,
                    'referral': 0
                }
            # Scenario 4
            else:
                commissions = {
                    'sales_agent': base * 0.07,
                    'unit_manager': 0,
                    'sales_leader': base * 0.01 + base * 0.01,
                    'referral': 0
                }
        # Scenario 2
        elif self.sold_by == 'UNIT_MNGR':
            commissions = {
                'sales_agent': 0,
                'unit_manager': base * 0.07 + base * 0.01,
                'sales_leader': base * 0.01,
                'referral': 0
            }
        # Scenario 3
        elif self.sold_by == 'SALES_LEADER':
            commissions = {
                'sales_agent': 0,
                'unit_manager': 0,
                'sales_leader': base * 0.07 + base * 0.01 + base * 0.01,
                'referral': 0
            }
        # Scenario 5
        elif self.sold_by == 'REFERRAL':
            commissions = {
                'sales_agent': base * 0.01,
                'unit_manager': 0,
                'sales_leader': 0,
                'referral': base * 0.07
            }

        return commissions

    def get_monthly_commissions(self):
        commissions = self.get_commissions()
        if self.installment_plan:
            for key in list(commissions.keys()):
                commissions[key] = commissions[key] / self.installment_plan.downpayment.split

        return commissions


class Service(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    date = models.DateField(null=False, blank=False, default=date.today)
    amount = models.FloatField(default=0.00)
    service_type = models.CharField(max_length=256, blank=True, null=True, choices=SERVICE_TYPES, default='INTERMENT')
    remarks = models.CharField(max_length=256, blank=True, null=True)

    contract = models.ForeignKey(Contract, null=False, blank=False, related_name='downpayments', on_delete=models.CASCADE)

    def __str__(self):
        return '{0} {1}'.format(self.service_type, self.amount)


class Bill(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    start = models.DateField(null=False, blank=False, default=date.today)
    end = models.DateField(null=False, blank=False, default=date.today)

    # 5 days before contract date
    issue_date = models.DateField(null=False, blank=False, default=date.today)
    # Same day as contract date
    due_date = models.DateField(null=False, blank=False, default=date.today)

    amount_due = models.FloatField(default=0.00)
    remarks = models.CharField(max_length=256, blank=True, null=True)

    contract = models.ForeignKey(Contract, null=False, blank=False, related_name='bills', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('contract', 'issue_date')

    def __str__(self):
        return '{0}: {1} - {2}'.format(str(self.contract),
                                       self.start.strftime('%b %d, %Y'),
                                       self.end.strftime('%b %d, %Y'))

    @property
    def is_paid(self):
        paid = 0
        for payment in self.payments.all():
            paid = paid + payment.amount
        if paid < self.amount_due:
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
    def interest(self):
        interest = 0

        bills = self.contract.bills.filter(issue_date__lt=self.issue_date)
        last_bill = bills.order_by('-issue_date').first()

        if last_bill.is_overdue:
            interest = last_bill.total_amount_due * 0.02

        return interest

    @property
    def total_amount_due(self):
        return self.amount_due + self.interest


class Payment(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    number = models.CharField(max_length=256, blank=False, null=False)
    date = models.DateField(null=False, blank=False, default=date.today)
    amount = models.FloatField(null=False, blank=False, default=0.00)
    payment_type = models.CharField(max_length=256, blank=True, null=True, choices=PAYMENT_TYPES, default='DOWNPAYMENT')
    remarks = models.CharField(max_length=256, blank=True, null=True)

    bill = models.ForeignKey(Bill, null=False, blank=False, related_name='payments', on_delete=models.CASCADE)

    def __str__(self):
        return self.number

