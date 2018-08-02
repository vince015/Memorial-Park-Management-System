from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class Branch(models.Model):
    name = models.CharField(max_length=128, null=False, blank=False)
    address = models.CharField(max_length=512, null=True, blank=True)

    def __str__(self):
        return self.name


class Unit(models.Model):
    block = models.CharField(max_length=32, blank=False, null=False)
    lot = models.CharField(max_length=32, blank=False, null=False)
    price = models.DecimalField(max_digits=15, decimal_places=2, null=True, default=0.01)
    branch = models.ForeignKey(Branch, null=True, blank=True, related_name='units', on_delete=models.SET_NULL)

    def __str__(self):
        return 'Block {0} Lot {1}'.format(self.block, self.lot)


def scanned_id_directory_path(instance, filename):
    ext  = os.path.splitext(filename)[1]
    return '{model}_id/{pk}_{name}{ext}'.format(model=type(instance).lower(),
                                                pk=instance.id,
                                                name=str(instance).title().replace(' ', ''),
                                                ext=ext)

class Client(models.Model):
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

    def clean(self):
        if not self.mobile and not self.phone:
            raise ValidationError(_('Input at least one contact number.'))


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

    def clean(self):
        if not self.mobile and not self.phone:
            raise ValidationError(_('Input at least one contact number.'))
