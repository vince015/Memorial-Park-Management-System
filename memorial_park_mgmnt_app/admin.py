from django.contrib import admin

from memorial_park_mgmnt_app import models


class BranchAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'name',
                    'address')
    list_display_links = ('id',
                          'name')
    search_fields = ('id',
                     'name')
    list_per_page = 50

admin.site.register(models.Branch, BranchAdmin)


class UnitAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'block',
                    'lot',
                    'price',
                    'branch')
    list_display_links = ('id',)
    list_filter = ('branch',)
    search_fields = ('id',
                     'block',
                     'lot')
    list_per_page = 50

admin.site.register(models.Unit, UnitAdmin)


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
