from django.contrib import admin
from powerscourt.wggateway.models import Address, Client, Person, GroupOfPeople, LLC, SippProvider, SippAdminPerson, Sipp, OldAddress
from powerscourt.wggateway.models import Syndicate, ProductProvider, Product, PurchaseForm, Currency, Purchase, Rent, SippAdminPersonAddress
from powerscourt.wggateway.models import ClientAddress

class ClientAddressInline(admin.StackedInline):
    model = ClientAddress

class GroupOfPeopleAdmin(admin.ModelAdmin):
    filter_horizontal = ('people',)
    inlines = [ClientAddressInline,]
    list_display = ('code',)

class ClientAdmin(admin.ModelAdmin):
    inlines = [ClientAddressInline,]

class LLCAdmin(admin.ModelAdmin):
    list_display = ('code', 'name',)

class ProductAdmin(admin.ModelAdmin):
    list_filter = ('provider',)

class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('code', 'notional',)
    #list_display = ('code', 'client', 'product', 'notional', 'notional_currency',)
    list_filter = ('product__provider', 'product')
    #fields = (
        #'client',
        #'product',
        #'code',
        #'active',
        #'password',
        #'start_date',
        #'form',
        #'notional',
        #'notional_currency',
        #'duration',
        #'signature_date',
        #'syndicate',
        #'date_funds_to_syndicate',
        #'shares_no',
        #'shares_value',
        #'shares_currency',
        #'shares_cert_date',
        #'shares_cert_sent_date',
        #'notes',)

class SippAdminPersonAddressInLine(admin.StackedInline):
    model = SippAdminPersonAddress

class SippAdminPersonAdmin(admin.ModelAdmin):
    inlines = [SippAdminPersonAddressInLine,]

class SippAdminPersonInLine(admin.TabularInline):
    model = SippAdminPerson

class SippProviderAdmin(admin.ModelAdmin):
    inlines = [SippAdminPersonInLine,]

class SippAdmin(admin.ModelAdmin):
    list_filter = ('company',)

admin.site.register(Address)
admin.site.register(Client, ClientAdmin)
admin.site.register(Currency)
admin.site.register(GroupOfPeople, GroupOfPeopleAdmin)
admin.site.register(LLC, LLCAdmin)
admin.site.register(OldAddress)
admin.site.register(Person)
admin.site.register(ProductProvider)
admin.site.register(Product, ProductAdmin)
admin.site.register(PurchaseForm)
admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(Rent)
admin.site.register(SippProvider, SippProviderAdmin)
admin.site.register(SippAdminPerson,SippAdminPersonAdmin)
admin.site.register(Sipp,SippAdmin)
admin.site.register(Syndicate)
