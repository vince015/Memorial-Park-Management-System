from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save

from memorial_park_mgmnt_app import models

@receiver(pre_save, sender=models.Lot)
def lot_pre_save(sender, instance, raw, using, update_fields, **kwargs):

    if not hasattr(instance, 'lot_contract'):
        instance.price = instance.lot_type.price

@receiver(post_save, sender=models.LotType)
def lot_type_post_save(sender, instance, created, **kwargs):

    for lot in instance.lot_set.all():
        if not hasattr(lot, 'lot_contract'):
            lot.price = instance.price
            lot.save()

# @receiver(post_save, sender=models.Contract)
# def contract_post_save(sender, instance, created, **kwargs):

#     if created and instance.payment_terms == 'SPOT':
#         # Create a single bill
#         models.Bill.objects.create(amount_due=instance.contract_price,
#                                    contract=instance,
#                                    remarks='For spot cash payment')