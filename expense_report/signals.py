from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save

from expense_report import models

@receiver(post_save, sender=models.Expense)
def expense_post_save(sender, instance, created, **kwargs):

    if instance.category == 'Petty Cash Replenishment':
        models.Transaction.objects.create(payee=instance.payee,
                                          amount=instance.amount,
                                          description=instance.category,
                                          transaction_type=models.CREDIT)

@receiver(pre_save, sender=models.Transaction)
def transaction_pre_save(sender, instance, raw, using, update_fields, **kwargs):

    instance.value = instance.amount * instance.transaction_type
