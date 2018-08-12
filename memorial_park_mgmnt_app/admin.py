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


class LotResource(resources.ModelResource):


    class Meta:
        model = models.Lot
        fields = ('id',
                  'block',
                  'lot',
                  'unit',
                  'branch')


class LotAdmin(ImportExportModelAdmin):
    list_display = ('id',
                    'block',
                    'lot',
                    'unit',
                    'branch')
    list_display_links = ('id',)
    list_filter = ('branch',)
    search_fields = ('id',
                     'block',
                     'lot',
                     'unit')
    list_per_page = 50
    resource_class = LotResource

admin.site.register(models.Lot, LotAdmin)


class ClientAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'last_name',
                    'first_name',
                    'contact_number',
                    'address')
    list_display_links = ('id',)
    search_fields = ('id',
                     'last_name',
                     'first_name')
    list_per_page = 50

    def contact_number(self, instance):
        return instance.contact_number()

    def address(self, instance):
        return instance.main_address()

admin.site.register(models.Client, ClientAdmin)


class AgentAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'last_name',
                    'first_name',
                    'contact_number',
                    'address')
    list_display_links = ('id',)
    search_fields = ('id',
                     'last_name',
                     'first_name')
    list_per_page = 50

    def contact_number(self, instance):
        return instance.contact_number()

    def address(self, instance):
        return instance.main_address()

admin.site.register(models.Agent, AgentAdmin)


class ContractAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'date',
                    'client',
                    'lot',
                    'buyer_type')
    list_display_links = ('id',)
    list_filter = ('buyer_type',)
    search_fields = ('id',
                     'client__last_name',
                     'client__first_name',
                     'lot__block',
                     'lot__lot'
                     'lot__unit')
    list_per_page = 50

admin.site.register(models.Contract, ContractAdmin)


class DownpaymentAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'date',
                    'amount',
                    'get_client',
                    'get_lot')
    list_display_links = ('id',)
    search_fields = ('id',
                     'contract__client__last_name',
                     'contract__client__first_name',
                     'contract__lot__block',
                     'contract__lot__lot'
                     'contract__lot__unit')
    list_per_page = 50

    def get_client(self, obj):
        return str(obj.contract.client)
    get_client.admin_order_field  = 'contract__client__last_name'
    get_client.short_description = 'Client Name'

    def get_lot(self, obj):
        return str(obj.contract.lot)
    get_lot.admin_order_field  = 'contract__lot__block'
    get_lot.short_description = 'Lot'

admin.site.register(models.Downpayment, DownpaymentAdmin)


class CommissionAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'date',
                    'amount',
                    'get_client',
                    'get_lot')
    list_display_links = ('id',)
    search_fields = ('id',
                     'contract__client__last_name',
                     'contract__client__first_name',
                     'contract__agent__last_name',
                     'contract__agent__first_name')
    list_per_page = 50

    def get_client(self, obj):
        return str(obj.contract.client)
    get_client.admin_order_field  = 'contract__client__last_name'
    get_client.short_description = 'Client Name'

    def get_lot(self, obj):
        return str(obj.contract.lot)
    get_lot.admin_order_field  = 'contract__lot__block'
    get_lot.short_description = 'Lot'

admin.site.register(models.Commission, CommissionAdmin)
