from django.contrib import admin

from import_export import resources
from import_export.admin import ImportExportModelAdmin

from expense_report import models

class ExpenseResource(resources.ModelResource):


    class Meta:
        model = models.Expense
        fields = ('id',
                  'date',
                  'reference_number',
                  'payee',
                  'amount',
                  'category',
                  'description')


class ExpenseAdmin(ImportExportModelAdmin):
    list_display  = ('id',
                     'date',
                     'reference_number',
                     'payee',
                     'amount',
                     'category')
    list_display_links = ('id',
                          'date')
    list_filter = ('category',)
    search_fields = ('id',
                     'date',
                     'reference_number',
                     'payee')
    list_per_page = 50
    resource_class = ExpenseResource

admin.site.register(models.Expense, ExpenseAdmin)

class TransactionResource(resources.ModelResource):


    class Meta:
        model = models.Transaction
        fields = ('id',
                  'timestamp',
                  'payee',
                  'amount',
                  'description',
                  'transaction_type')


class TransactionAdmin(ImportExportModelAdmin):
    list_display  = ('id',
                     'timestamp',
                     'payee',
                     'description',
                     'amount')
    list_display_links = ('id',
                          'timestamp')
    search_fields = ('id',
                     'payee')
    list_per_page = 50
    resource_class = TransactionResource

admin.site.register(models.Transaction, TransactionAdmin)
