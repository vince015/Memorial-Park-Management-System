from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db.models import Sum

# Constants
BUYER_TYPES = (('PRE-NEED', 'Pre-Need'),
               ('IN-NEED', 'In-Need'))

def scanned_id_directory_path(instance, filename):
    ext  = os.path.splitext(filename)[1]
    return '{model}_ids/{pk}_{name}{ext}'.format(model=type(instance).lower(),
                                                 pk=instance.id,
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

    birthdate = models.DateField(blank=False, null=False)

    # Cannot be both blank/null
    mobile = models.CharField(max_length=16, blank=True, null=True)
    phone = models.CharField(max_length=16, blank=True, null=True)

    # Address
    house_number = models.CharField(max_length=8, blank=True, null=True)
    street_name = models.CharField(max_length=128, blank=True, null=True)
    barangay = models.CharField(max_length=128, blank=False, null=False)
    town = models.CharField(max_length=128, blank=False, null=False)
    province = models.CharField(max_length=128, blank=False, null=False)

    scanned_id = models.FileField(upload_to=scanned_id_directory_path, blank=False, null=False)

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
            addr = '{house_number}, {address}'.format(house_number=self.house_number, address=addr)

        return addr

    def contact_number(self):
        return self.mobile or self.phone

    def clean(self):
        if not self.mobile and not self.phone:
            raise ValidationError(_('Input at least one contact number.'))


class Client(models.Model):
    last_name = models.CharField(max_length=56, blank=False, null=False)
    first_name = models.CharField(max_length=56, blank=False, null=False)
    middle_name = models.CharField(max_length=56, blank=True, null=True)

    birthdate = models.DateField(blank=False, null=False)

    # Cannot be both blank/null
    contact_number = models.CharField(max_length=16, blank=True, null=True)

    # Address
    house_number = models.CharField(max_length=8, blank=True, null=True)
    street = models.CharField(max_length=128, blank=True, null=True)
    barangay = models.CharField(max_length=128, blank=False, null=False)
    town = models.CharField(max_length=128, blank=False, null=False)
    province = models.CharField(max_length=128, blank=False, null=False)

    scanned_id = models.FileField(upload_to=scanned_id_directory_path, blank=False, null=False)

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
            addr = '{house_number}, {address}'.format(house_number=self.house_number, address=addr)

        return addr


class Contract(models.Model):
    date = models.DateField(null=False, blank=False, default=timezone.now)
    buyer_type = models.CharField(max_length=32, blank=False, null=False, choices=BUYER_TYPES, default='PRE-NEED')
    lot_price = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    care_fund = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

    # Discounts
    discount_spot_cash = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    discount_spot_dp = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

    # Interset
    interest_on_installment = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

    # Fees
    certificate_of_ownership = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    change_of_title = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    interment = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

    # Others
    reservation_loi = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    spot_cash_payment = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

    # Misc
    remarks = models.CharField(max_length=256, blank=True, null=True)

    lot = models.OneToOneField(Lot, null=False, blank=False, related_name='lot_contract', on_delete=models.CASCADE)
    client = models.ForeignKey(Client, null=False, blank=False, related_name='client_contracts', on_delete=models.CASCADE)
    agent = models.ForeignKey(Agent, null=True, blank=True, related_name='agent_contracts', on_delete=models.CASCADE)

    def __str__(self):
        return '{0} - {1}'.format(str(self.client), str(self.lot))

    def contract_price(self):
        return self.lot_price + self.care_fund - self.discount_spot_cash - self.discount_spot_dp + self.interest_on_installment

    def installment_amount(self):
        return ((self.lot_price + self.care_fund) * 0.8) + self.interest_on_installment

    def downpayment_amount(self):
        return ((self.lot_price + self.care_fund) * 0.2) - self.reservation_loi

    def installment_downpayment_balance(self):
        return ((self.lot_price + self.care_fund) * 0.2) - self.reservation_loi

    def installment_balance(self):
        return self.installment_amount() - self.spot_cash_payment - self.downpayments.aggregate(Sum('amount'))

    def unpaid_balance(self):
        return self.installment_downpayment_balance() + self.installment_balance() - self.discount_spot_cash

    def total_commissionable_amount(self):
        lot_price_less_discount = self.lot_price - self.discount_spot_cash - self.discount_spot_dp
        net_vat = lot_price_less_discount / 1.12 # Net of 12% VAT
        gross_commission = net_vat * 0.09 # Gross 9% Commission
        return gross_commission * 0.9

    def total_commission_paid(self):
        return self.commissions.aggregate(Sum('amount'))

    def commission_balance(self):
        return self.total_commissionable_amount() - self.total_commission_paid()

    def total_payment(self):
        # Fees
        total = self.certificate_of_ownership + self.change_of_title + self.interment
        # Others
        total = total + self.reservation_loi + self.spot_cash_payment
        # Downpayments
        total = total + self.downpayments.aggregate(Sum('amount'))

        return total


class Downpayment(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    date = models.DateField(null=False, blank=False, default=timezone.now)
    amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

    contract = models.ForeignKey(Contract, null=False, blank=False, related_name='downpayments', on_delete=models.CASCADE)


class Commission(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    date = models.DateField(null=False, blank=False, default=timezone.now)
    amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

    contract = models.ForeignKey(Contract, null=False, blank=False, related_name='commissions', on_delete=models.CASCADE)
