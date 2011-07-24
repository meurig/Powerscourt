from django.contrib import admin
from powerscourt.wggateway.models import Address, Client, Person, GroupOfPeople, SippProvider, SippAdminPerson, Sipp, OldAddress
from powerscourt.wggateway.models import Syndicate, ProductProvider, Product, PurchaseForm, Currency, Purchase, Rent

admin.site.register(Address)
admin.site.register(Client)
admin.site.register(Person)
admin.site.register(GroupOfPeople)
admin.site.register(SippProvider)
admin.site.register(SippAdminPerson)
admin.site.register(Sipp)
admin.site.register(OldAddress)
admin.site.register(Syndicate)
admin.site.register(ProductProvider)
admin.site.register(Product)
admin.site.register(PurchaseForm)
admin.site.register(Currency)
admin.site.register(Purchase)
admin.site.register(Rent)
