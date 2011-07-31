from django.contrib import admin
from powerscourt.wggateway.models import Address, Client, Person, GroupOfPeople, LLC, SippProvider, SippAdminPerson, Sipp, OldAddress
from powerscourt.wggateway.models import Syndicate, ProductProvider, Product, PurchaseForm, Currency, Purchase, Rent

class GroupOfPeopleAdmin(admin.ModelAdmin):
    filter_horizontal = ('people',)
    list_display = ('code', 'address',)

class LLCAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'address',)

admin.site.register(Address)
admin.site.register(Client)
admin.site.register(Currency)
admin.site.register(GroupOfPeople, GroupOfPeopleAdmin)
admin.site.register(LLC, LLCAdmin)
admin.site.register(OldAddress)
admin.site.register(Person)
admin.site.register(ProductProvider)
admin.site.register(Product)
admin.site.register(PurchaseForm)
admin.site.register(Purchase)
admin.site.register(Rent)
admin.site.register(SippProvider)
admin.site.register(SippAdminPerson)
admin.site.register(Sipp)
admin.site.register(Syndicate)
