from django.contrib import admin

from import_export import resources
from import_export.admin import ImportExportModelAdmin

from memorial_park_mgmnt_app import models


class BranchResource(resources.ModelResource):

    class Meta:
        model = models.Branch
        fields = ('id',
                  'name',
                  'address')


class BranchAdmin(ImportExportModelAdmin):
    list_display = ('id',
                    'name',
                    'address')
    list_display_links = ('id',
                          'name')
    search_fields = ('id',
                     'name')
    list_per_page = 50
    resource_class = BranchResource

admin.site.register(models.Branch, BranchAdmin)


class LotTypeResource(resources.ModelResource):

    class Meta:
        model = models.LotType
        fields = ('id',
                  'lot_type',
                  'price',
                  'vat',
                  'care_fund')


class LotTypeAdmin(ImportExportModelAdmin):
    list_display = ('id',
                    'lot_type',
                    'price',
                    'vat',
                    'care_fund')
    list_display_links = ('id',)
    list_filter = ('lot_type',)
    search_fields = ('id',)
    list_per_page = 50
    resource_class = LotTypeResource

admin.site.register(models.LotType, LotTypeAdmin)


class LotResource(resources.ModelResource):

    class Meta:
        model = models.Lot
        fields = ('id',
                  'block',
                  'lot',
                  'unit',
                  'lot_type',
                  'branch')


class LotAdmin(ImportExportModelAdmin):
    list_display = ('id',
                    'block',
                    'lot',
                    'unit',
                    'price',
                    'lot_type',
                    'branch')
    list_display_links = ('id',)
    list_filter = ('branch',
                   'lot_type')
    search_fields = ('id',
                     'block',
                     'lot',
                     'unit')
    list_per_page = 50
    resource_class = LotResource

admin.site.register(models.Lot, LotAdmin)


class ClientResource(resources.ModelResource):

    class Meta:
        model = models.Client
        fields = ('id',
                  'last_name',
                  'first_name',
                  'middle_name',
                  'house_number',
                  'street',
                  'barangay',
                  'town',
                  'province',
                  'contact_number',
                  'branch')


class ClientAdmin(ImportExportModelAdmin):
    list_display = ('id',
                    'last_name',
                    'first_name',
                    'contact_number',
                    'main_address',
                    'branch')
    list_display_links = ('id',)
    list_filter = ('branch',)
    search_fields = ('id',
                     'last_name',
                     'first_name')
    list_per_page = 50
    resource_class = ClientResource

admin.site.register(models.Client, ClientAdmin)


class AgentResource(resources.ModelResource):

    class Meta:
        model = models.Agent
        fields = ('id',
                  'last_name',
                  'first_name',
                  'middle_name',
                  'rank',
                  'house_number',
                  'street',
                  'barangay',
                  'town',
                  'province',
                  'contact_number')


class AgentAdmin(ImportExportModelAdmin):
    list_display = ('id',
                    'last_name',
                    'first_name',
                    'contact_number',
                    'main_address')
    list_display_links = ('id',)
    list_filter = ('rank',)
    search_fields = ('id',
                     'last_name',
                     'first_name')
    resource_class = AgentResource
    list_per_page = 50

admin.site.register(models.Agent, AgentAdmin)


class DownpaymentPromoResource(resources.ModelResource):

    class Meta:
        model = models.DownpaymentPromo
        fields = ('id',
                  'name',
                  'start_date',
                  'end_date',
                  'split',
                  'discount')


class DownpaymentPromoAdmin(ImportExportModelAdmin):
    list_display = ('id',
                    'name',
                    'split',
                    'discount',
                    'start_date',
                    'end_date')
    list_display_links = ('id',
                          'name')
    search_fields = ('id',
                     'name')
    resource_class = DownpaymentPromoResource
    list_per_page = 50

admin.site.register(models.DownpaymentPromo, DownpaymentPromoAdmin)


class InstallmentPromoResource(resources.ModelResource):

    class Meta:
        model = models.InstallmentPromo
        fields = ('id',
                  'name',
                  'months',
                  'interest',
                  'start_date',
                  'end_date')


class InstallmentPromoAdmin(ImportExportModelAdmin):
    list_display = ('id',
                    'name',
                    'months',
                    'interest',
                    'start_date',
                    'end_date')
    list_display_links = ('id',
                          'name')
    search_fields = ('id',
                     'name')
    resource_class = InstallmentPromoResource
    list_per_page = 50

admin.site.register(models.InstallmentPromo, InstallmentPromoAdmin)


class SpotPromoResource(resources.ModelResource):

    class Meta:
        model = models.SpotPromo
        fields = ('id',
                  'discount',
                  'start_date',
                  'end_date')


class SpotPromoAdmin(ImportExportModelAdmin):
    list_display = ('id',
                    'discount',
                    'start_date',
                    'end_date')
    list_display_links = ('id',)
    search_fields = ('id',)
    resource_class = SpotPromoResource
    list_per_page = 50

admin.site.register(models.SpotPromo, SpotPromoAdmin)


class ContractResource(resources.ModelResource):

    class Meta:
        model = models.Contract
        fields = ('id',
                  'date',
                  'buyer_type',
                  'payment_terms',
                  'client',
                  'lot')


class ContractAdmin(ImportExportModelAdmin):
    list_display = ('id',
                    'date',
                    'client',
                    'lot',
                    'payment_terms',
                    'buyer_type')
    list_display_links = ('id',)
    list_filter = ('buyer_type',
                   'payment_terms',
                   'lot__branch')
    search_fields = ('id',
                     'client__last_name',
                     'client__first_name',
                     'lot__block',
                     'lot__lot',
                     'lot__unit')
    resource_class = ContractResource
    list_per_page = 50

    def client(self, obj):
        return str(obj.client)
    client.short_description = 'Client'
    client.admin_order_field = ['client__last_name',
                                'client__first_name']

    def lot(self, obj):
        return str(obj.lot)
    lot.short_description = 'Lot'
    lot.admin_order_field = ['lot__block',
                             'lot__lot',
                             'lot__unit']

admin.site.register(models.Contract, ContractAdmin)


class ServiceResource(resources.ModelResource):

    class Meta:
        model = models.Service
        fields = ('id',
                  'date',
                  'amount',
                  'service_type',
                  'contract')


class ServiceAdmin(ImportExportModelAdmin):
    list_display = ('id',
                    'date',
                    'amount',
                    'service_type')
    list_display_links = ('id',)
    list_filter = ('service_type',)
    search_fields = ('id',)
    resource_class = ServiceResource
    list_per_page = 50

admin.site.register(models.Service, ServiceAdmin)


class BillResource(resources.ModelResource):

    class Meta:
        model = models.Bill
        fields = ('id',
                  'start',
                  'end',
                  'issue_date',
                  'due_date',
                  'amount_due',
                  'contract')


class BillAdmin(ImportExportModelAdmin):
    list_display = ('id',
                    'start',
                    'end',
                    'issue_date',
                    'due_date',
                    'amount_due')
    list_display_links = ('id',)
    search_fields = ('id',
                     'issue_date')
    resource_class = BillResource
    list_per_page = 50


admin.site.register(models.Bill, BillAdmin)


class PaymentResource(resources.ModelResource):

    class Meta:
        model = models.Payment
        fields = ('id',
                  'number',
                  'date',
                  'payment_type',
                  'bill')


class PaymentAdmin(ImportExportModelAdmin):
    list_display = ('id',
                    'number',
                    'date',
                    'payment_type',
                    'bill')
    list_display_links = ('id',
                          'number')
    list_filter = ('payment_type',)
    search_fields = ('id',
                     'number')
    resource_class = PaymentResource
    list_per_page = 50

admin.site.register(models.Payment, PaymentAdmin)
