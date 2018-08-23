import os
import uuid

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db.models import Sum

# Constants
BUYER_TYPES = (('PRE-NEED', 'Pre-Need'),
               ('IN-NEED', 'In-Need'))

AGENT_TYPES = (('SALES_AGENT', 'Sales Agent'),
               ('UNIT_MNGR', 'Unit Manager'),
               ('SALES_LEADER', 'Sales Leader'),
               ('REFERRAL', 'Referral'))

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

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Branches'


class Lot(models.Model):
    block = models.CharField(max_length=32, blank=False, null=False)
    lot = models.CharField(max_length=32, blank=False, null=False)
    unit = models.CharField(max_length=32, blank=False, null=False)
    branch = models.ForeignKey(Branch, null=True, blank=True, related_name='lots', on_delete=models.SET_NULL)

    def __str__(self):
        return 'B{0}-LOT{1}{2}'.format(self.block, self.lot, self.unit)


class Agent(models.Model):
    last_name = models.CharField(max_length=56, blank=False, null=False)
    first_name = models.CharField(max_length=56, blank=False, null=False)
    middle_name = models.CharField(max_length=56, blank=True, null=True)

    # Address
    house_number = models.CharField(max_length=8, blank=True, null=True)
    street = models.CharField(max_length=128, blank=True, null=True)
    barangay = models.CharField(max_length=128, blank=False, null=False)
    town = models.CharField(max_length=128, blank=False, null=False)
    province = models.CharField(max_length=128, blank=False, null=False)

    contact_number = models.CharField(max_length=16, blank=True, null=True)
    valid_id = models.FileField(upload_to=valid_id_directory_path, blank=False, null=False)
    birthdate = models.DateField(blank=True, null=True)

    other_address = models.CharField(max_length=512, blank=True, null=True)
    business_name = models.CharField(max_length=512, blank=True, null=True)
    business_address = models.CharField(max_length=512, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        fullname = '{0} {1}'.format(self.last_name, self.first_name)
        if self.middle_name:
            fullname = '{0} {1} {2}'.format(self.last_name, self.first_name, self.middle_name)
        return fullname

    def main_address(self):
        addr = '{barangay}, {town}, {province}'.format(barangay=self.barangay, town=self.town, province=self.province)
        if self.street:
            addr = '{street}, {address}'.format(street=self.street, address=addr)
        if self.house_number:
            addr = '{house_number} {address}'.format(house_number=self.house_number, address=addr)

        return addr


class Client(models.Model):
    last_name = models.CharField(max_length=56, blank=False, null=False)
    first_name = models.CharField(max_length=56, blank=False, null=False)
    middle_name = models.CharField(max_length=56, blank=True, null=True)

    # Address
    house_number = models.CharField(max_length=8, blank=True, null=True)
    street = models.CharField(max_length=128, blank=True, null=True)
    barangay = models.CharField(max_length=128, blank=False, null=False)
    town = models.CharField(max_length=128, blank=False, null=False)
    province = models.CharField(max_length=128, blank=False, null=False)

    contact_number = models.CharField(max_length=16, blank=True, null=True)
    valid_id = models.FileField(upload_to=valid_id_directory_path, blank=False, null=False)
    birthdate = models.DateField(blank=True, null=True)

    other_address = models.CharField(max_length=512, blank=True, null=True)
    business_name = models.CharField(max_length=512, blank=True, null=True)
    business_address = models.CharField(max_length=512, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

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


class Contract(models.Model):
    date = models.DateField(null=False, blank=False, default=timezone.now)
    buyer_type = models.CharField(max_length=32, blank=False, null=False, choices=BUYER_TYPES, default='PRE-NEED')
    lot_price = models.FloatField(default=0.00)
    care_fund = models.FloatField(default=0.00)

    # Discounts
    discount_spot_cash = models.FloatField(default=0.00)
    discount_spot_dp = models.FloatField(default=0.00)

    # Interset
    interest_on_installment = models.FloatField(default=0.00)

    # Fees
    certificate_of_ownership = models.FloatField(default=0.00)
    change_of_title = models.FloatField(default=0.00)
    interment = models.FloatField(default=0.00)

    # Others
    reservation_loi = models.FloatField(default=0.00)
    spot_cash_payment = models.FloatField(default=0.00)

    # Misc
    remarks = models.CharField(max_length=256, blank=True, null=True)

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
    def contract_price(self):
        return self.lot_price + self.care_fund - self.discount_spot_cash - self.discount_spot_dp + self.interest_on_installment

    @property
    def installment_amount(self):
        return ((self.lot_price + self.care_fund) * 0.8) + self.interest_on_installment

    @property
    def downpayment_amount(self):
        return ((self.lot_price + self.care_fund) * 0.2) - self.reservation_loi

    @property
    def installment_downpayment_balance(self):
        balance = self.downpayment_amount - self.discount_spot_dp
        downpayments = self.downpayments.aggregate(Sum('amount')).get('amount__sum', 0.00)
        if downpayments is not None:
            balance = balance - downpayments

        return balance

    @property
    def installment_balance(self):
        balance = self.installment_amount - self.spot_cash_payment

        downpayments = self.downpayments.aggregate(Sum('amount')).get('amount__sum', 0.00)
        if downpayments is not None:
            balance = balance - downpayments

        return balance

    @property
    def unpaid_balance(self):
        return self.installment_downpayment_balance + self.installment_balance - self.discount_spot_cash

    @property
    def total_commissionable_amount(self):
        lot_price_less_discount = self.lot_price - self.discount_spot_cash - self.discount_spot_dp
        net_vat = lot_price_less_discount / 1.12 # Net of 12% VAT
        gross_commission = net_vat * 0.09 # Gross 9% Commission
        return gross_commission * 0.9

    @property
    def total_commission_paid(self):
        commissions = self.commissions.aggregate(Sum('amount')).get('amount__sum', 0.00)
        if commissions is None:
            commissions = 0.00

        return commissions

    @property
    def commission_balance(self):
        return self.total_commissionable_amount - self.total_commission_paid

    @property
    def total_payment(self):
        # Fees
        total = self.certificate_of_ownership + self.change_of_title + self.interment
        # Others
        total = total + self.reservation_loi + self.spot_cash_payment
        # Downpayments
        downpayments = self.downpayments.aggregate(Sum('amount')).get('amount__sum', 0.00)
        if downpayments is not None:
            total = total + downpayments

        return total

    def get_commissions(self):
        base = self.total_commissionable_amount
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


class Downpayment(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    date = models.DateField(null=False, blank=False, default=timezone.now)
    amount = models.FloatField(default=0.00)
    remarks = models.CharField(max_length=256, blank=True, null=True)

    contract = models.ForeignKey(Contract, null=False, blank=False, related_name='downpayments', on_delete=models.CASCADE)


class Commission(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    date = models.DateField(null=False, blank=False, default=timezone.now)
    amount = models.FloatField(default=0.00)
    remarks = models.CharField(max_length=256, blank=True, null=True)

    contract = models.ForeignKey(Contract, null=False, blank=False, related_name='commissions', on_delete=models.CASCADE)
