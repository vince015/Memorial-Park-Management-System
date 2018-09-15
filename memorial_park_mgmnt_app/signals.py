from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save

from memorial_park_mgmnt_app import models

@receiver(pre_save, sender=models.Lot)
def lot_presave_save(sender, instance, created, **kwargs):

    if not hasattr(instance, 'lot_contract'):
        instance.price = instance.lot_type.price
