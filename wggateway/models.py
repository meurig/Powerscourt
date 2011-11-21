# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models
from django.db.models import Sum
from model_utils.managers import InheritanceManager
from smart_selects.db_fields import ChainedForeignKey
import locale
from django.core import urlresolvers
import datetime

class AddressBase(models.Model):
    TYPE_CHOICES = (
        ('personal', 'Personal'),
        ('business', 'Business'),
    )
    type = models.CharField(max_length=8, choices=TYPE_CHOICES)
    address1 = models.CharField(max_length=384)
    address2 = models.CharField(max_length=384, blank=True)
    address3 = models.CharField(max_length=384, blank=True)
    city = models.CharField(max_length=384)
    county = models.CharField(max_length=384, blank=True)
    postcode = models.CharField(max_length=30)
    COUNTRY_CHOICES = (
        ('UK', 'United Kingdom'),
        ('US', 'United States'),
    )
    country = models.CharField(max_length=3, choices=COUNTRY_CHOICES)
    phone1 = models.CharField(max_length=32, blank=True)
    phone2 = models.CharField(max_length=32, blank=True)
    email1 = models.EmailField(blank=True)
    email2 = models.EmailField(blank=True)

    def get_details(self):
        return [("Address", self.address1),
                ("", self.address2),
                ("", self.address3),
                ("", self.city),
                ("", self.county),
                ("", self.postcode),
                ("", self.country),
                ]

    def __unicode__(self):
        return u'%s, %s' % (self.postcode, self.address1)

    class Meta:
        abstract = True

class Address(AddressBase):

    class Meta:
        verbose_name_plural="addresses"

class Client(models.Model):
    code = models.CharField(max_length=18, unique=True)
    #address = models.ForeignKey(Address)
    #address = models.OneToOneField(ClientAddress)
    objects = InheritanceManager()

    def get_description(self):
        return "Generic client object, no type assigned"

    def __unicode__(self):
        return self.code

    def get_absolute_url(self):
        return "/client/%i/" % self.id

    def get_admin_change_url(self):
        return urlresolvers.reverse('admin:wggateway_client_change', args=(self.id,))

    def get_type(self):
        return self.__class__.__name__

class ClientAddress(AddressBase):
    client = models.OneToOneField(Client, primary_key=True)

    class Meta:
        verbose_name_plural="client addresses"

class OldAddress(AddressBase):
    client = models.ForeignKey(Client)
    deprication_date = models.DateField()

    def __unicode__(self):
        return u'%s, %s' % (self.postcode, self.address1)

    class Meta:
        verbose_name_plural="old addresses"

class Person(models.Model):
    title = models.CharField(max_length=48)
    firstname = models.CharField(max_length=192)
    middlename = models.CharField(max_length=192, blank=True)
    lastname = models.CharField(max_length=192)

    def get_readable_name(self):
        return self.title + ". " + self.firstname + " " + self.lastname

    def __unicode__(self):
        return u'%s, %s' % (self.lastname, self.firstname)

    class Meta:
        verbose_name_plural="people"

class GroupOfPeople(Client):
    people = models.ManyToManyField(Person, blank=True)

    def get_names(self):
        names=[]
        for person in self.people.all():
            names.append(person.get_readable_name())
        return names

    def get_description(self):
        names=self.get_names()
        return ', '.join(names)

    def get_details(self):
        return [("ClientCode", self.code),
                ("Type", self.get_type),
                ("People", self.get_description)] + self.address.get_details()

    def get_admin_change_url(self):
        return urlresolvers.reverse('admin:wggateway_groupofpeople_change', args=(self.id,))

    def __unicode__(self):
        return self.code

    class Meta:
        verbose_name_plural="groups of people"

class SippProvider(models.Model):
    name = models.CharField(max_length=384)

    def __unicode__(self):
        return self.name

class SippAdminPerson(models.Model):
    company = models.ForeignKey(SippProvider)
    title = models.CharField(max_length=48)
    firstname = models.CharField(max_length=192)
    middlename = models.CharField(max_length=192, blank=True)
    lastname = models.CharField(max_length=192)

    def __unicode__(self):
        return u'%s %s' % (self.firstname, self.lastname)

    class Meta:
        verbose_name_plural="sipp admin people"

class SippAdminPersonAddress(AddressBase):
    sippadminperson = models.OneToOneField(SippAdminPerson, primary_key=True)

    class Meta:
        verbose_name_plural="admin person addresses"

class Sipp(Client):
    company = models.ForeignKey(SippProvider)
    reference = models.CharField(max_length=64)
    admin_person = ChainedForeignKey(
            SippAdminPerson,
            chained_field="company",
            chained_model_field="company", 
            show_all=False, 
            auto_choose=True
            )

    def get_admin_change_url(self):
        return urlresolvers.reverse('admin:wggateway_sipp_change', args=(self.id,))

    def get_description(self):
        return self.company.name + ": " + self.reference

    def get_details(self):
        return [("ClientCode", self.code),
                ("Type", self.get_type),
                ("Provider", self.company),
                ("Reference", self.reference),
                ("Admin Person", self.admin_person)] + self.address.get_details()

    def __unicode__(self):
        return u'%s %s' % (self.company, self.reference)

class LLC(Client):
    name = models.CharField(max_length=64)

    def get_admin_change_url(self):
        return urlresolvers.reverse('admin:wggateway_llc_change', args=(self.id,))

    def __unicode__(self):
        return u'%s' % (self.name)

class Syndicate(models.Model):
    name = models.CharField(max_length=32)

    def get_absolute_url(self):
        return "/syndicate/%i/" % self.id

    def get_admin_change_url(self):
        return urlresolvers.reverse('admin:wggateway_syndicate_change', args=(self.id,))

    def __unicode__(self):
        return self.name

class ProductProvider(models.Model):
    name = models.CharField(max_length=64)

    def get_absolute_url(self):
        return "/product_provider/%i/" % self.id

    def __unicode__(self):
        return self.name

class Product(models.Model):
    provider = models.ForeignKey(ProductProvider)
    name = models.CharField(max_length=64)
    prefix = models.CharField(max_length=6)
    increment = models.IntegerField()
    display_order = models.IntegerField()

    def get_absolute_url(self):
        return "/product/%i/" % self.id

    def get_active_purchases(self):
        return self.purchase_set.filter(active=1)

    def get_inactive_purchases(self):
        return self.purchase_set.filter(active=0)

    def get_invested_currencies(self):
        return Currency.objects.filter(purchase_notional_currency__product__id = self.id)

    def get_amounts_invested(self):
        currency_amounts={}
        for currency in self.get_invested_currencies():
            currency_amounts[currency.code] = self.purchase_set.filter(notional_currency__code=currency.code, active=1).aggregate(Sum('notional'))['notional__sum']
        return currency_amounts

    def get_returns(self):
        """
        Returns an ordered list of pairs, where each pair is made up of a date and a dictionary, and each dictionary has currencies as its keys and amounts as its values
        """
        dated_returns = {}
        for rent in Rent.objects.filter(purchase__product__id = self.id):
            if rent.due_date not in dated_returns:
                dated_returns[rent.due_date] = {}
            for currency, amount in rent.get_total_amounts():
                if currency not in dated_returns[rent.due_date]:
                    dated_returns[rent.due_date][currency] = 0
                dated_returns[rent.due_date][currency] += amount
        dated_returns_list=dated_returns.items()
        dated_returns_list.sort()
        return dated_returns_list

    def get_future_returns(self):
        """
        As for get_returns, but only where the date >= today.
        """
        returns_list = self.get_returns()
        future_returns = []
        for date, returns in returns_list:
            if date >= datetime.date.today():
                #returns_list.remove((date, returns)) seems to cause problems removing from list while iterating over it?
                future_returns.append((date, returns))
        return future_returns

    def get_total_future_returns(self):
        """
        Returns a sorted list of currency,amount tuples listing the total future returns for this product
        """
        total_returns = {}
        for currency in self.get_invested_currencies():
            total_returns[currency.code] = 0
        for date, returns in self.get_future_returns():
            for currency, amount in returns.items():
                total_returns[currency.code] += amount
        return total_returns.items()

    #def get_active_client_purchase_info(self):
    #    clients={}
    #    for purchase in self.purchase_set.all():
    #        client = purchase.client
    #        if purchase.active == 1:
    #            if client.id not in clients:
    #                clients[client.id] = purchase.notional
    #            else:
    #                clients[client.id] += purchase.notional
    #    return clients

    def __unicode__(self):
        return self.name

class PurchaseForm(models.Model):
    code = models.CharField(max_length=32)

    def __unicode__(self):
        return self.code

class Currency(models.Model):
    code = models.CharField(max_length=8, primary_key=True)
    name = models.CharField(max_length=32)

    def __unicode__(self):
        return u'%s' % (self.code)

    class Meta:
        verbose_name_plural="currencies"

class Purchase(models.Model):
    client = models.ForeignKey(Client)
    product = models.ForeignKey(Product)
    code = models.CharField(max_length=8)
    active = models.IntegerField()
    password = models.CharField(max_length=32, blank=True)
    start_date = models.DateTimeField()
    form = models.ForeignKey(PurchaseForm)
    notional = models.DecimalField(decimal_places=2, max_digits=16)
    notional_currency = models.ForeignKey(Currency, related_name="purchase_notional_currency", default="GBP")
    duration = models.IntegerField(blank=True)
    signature_date = models.DateField()
    syndicate = models.ForeignKey(Syndicate, blank=True)
    date_funds_to_syndicate = models.DateTimeField()
    shares_no = models.IntegerField()
    shares_value = models.IntegerField()
    shares_currency = models.ForeignKey(Currency, related_name="purchase_shares_currency", default="GBP")
    shares_cert_date = models.DateField()
    shares_cert_sent_date = models.DateField()
    notes = models.TextField()

    def get_client_subclass(self):
        return Client.objects.select_subclasses().get(pk=self.client.id)

    def get_notional(self):
        return self.notional / 100

    def get_absolute_url(self):
        return "/purchase/%i/" % self.id

    def get_active(self):
        if self.active == 1:
            return "Yes"
        else:
            return "No"

    def __unicode__(self):
        return self.code

class Rent(models.Model):
    purchase = models.ForeignKey(Purchase)
    due_date = models.DateField()
    paid = models.IntegerField()
    paid_date = models.DateField()
    base_rate_bps = models.IntegerField()
    base_currency = models.ForeignKey(Currency, related_name="rent_base_currency", default="GBP")
    base_amount = models.IntegerField()
    fixed_fee_added_currency = models.ForeignKey(Currency, related_name="rent_fixed_fee_added_currency", default="GBP")
    fixed_fee_added_amount = models.IntegerField()
    variable_fee_added_rate_bps = models.IntegerField()
    variable_fee_added_amount = models.IntegerField()
    fixed_fee_deducted_currency = models.ForeignKey(Currency, related_name="rent_fixed_fee_deducted_currency", default="GBP")
    fixed_fee_deducted_amount = models.IntegerField()
    variable_fee_deducted_rate_bps = models.IntegerField()
    variable_fee_deducted_amount = models.IntegerField()
    TYPE_CHOICES = (
        ('coupon', 'Coupon'),
        ('principal', 'Principal'),
    )
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)

    def get_paid(self):
        if self.paid == 1:
            return "Yes"
        else:
            return "No"

    #def get_calculated_amount(self):
        #"""
        #This assumes all amounts are in the same currency which is often not the case.
        #"""
        #return self.base_amount + self.fixed_fee_added_amount + self.variable_fee_added_amount - self.fixed_fee_deducted_amount - self.variable_fee_deducted_amount

    def get_total_amounts(self):
        """
        Returns an ordered list of (currency, amount) tuples representing the total amount for this 'rent'
        """
        amounts={self.base_currency: self.base_amount + self.variable_fee_added_amount - self.variable_fee_deducted_amount}
        if self.fixed_fee_added_currency not in amounts:
            amounts[self.fixed_fee_added_currency] = 0
        amounts[self.fixed_fee_added_currency] += self.fixed_fee_added_amount
        if self.fixed_fee_deducted_currency not in amounts:
            amounts[self.fixed_fee_deducted_currency] = 0
        amounts[self.fixed_fee_deducted_currency] -= self.fixed_fee_deducted_amount
        amounts_list = amounts.items()
        amounts_list.sort()
        return amounts_list

    def get_fees_deducted(self):
        """
        Returns a list of currency,amount pairs representing the fees deducted from this 'rent'
        """
        fees_deducted={}
        if self.variable_fee_deducted_amount > 0:
            fees_deducted[self.base_currency.code] = self.variable_fee_deducted_amount
        if self.fixed_fee_deducted_amount > 0:
            if self.fixed_fee_deducted_currency == self.base_currency:
                if self.variable_fee_deducted_amount > 0:
                    fees_deducted[self.base_currency.code] += self.fixed_fee_deducted_amount
                else:
                    fees_deducted[self.base_currency.code] = self.fixed_fee_deducted_amount
            else:
                fees_deducted[self.fixed_fee_deducted_currency.code] = self.fixed_fee_deducted_amount
        return sorted(fees_deducted.items())

    def get_fees_added(self):
        """
        Returns a list of currency,amount pairs representing the fees added to this 'rent'
        """
        fees_added={}
        if self.variable_fee_added_amount > 0:
            fees_added[self.base_currency.code] = self.variable_fee_added_amount
        if self.fixed_fee_added_amount > 0:
            if self.fixed_fee_added_currency == self.base_currency:
                if self.variable_fee_added_amount > 0:
                    fees_added[self.base_currency.code] += self.fixed_fee_added_amount
                else:
                    fees_added[self.base_currency.code] = self.fixed_fee_added_amount
            else:
                fees_added[self.fixed_fee_added_currency.code] = self.fixed_fee_added_amount
        return sorted(fees_added.items())


    class Meta:
        verbose_name_plural="rent"

#class UserInput(models.Model):
    #createddate = models.DateTimeField()
    #createdby_id = models.IntegerField()
    #updateddate = models.DateTimeField()
    #updatedby_id = models.IntegerField()
