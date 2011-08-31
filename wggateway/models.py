# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models
from model_utils.managers import InheritanceManager
from smart_selects.db_fields import ChainedForeignKey
import locale
from django.core import urlresolvers

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

#class ClientAddress(AddressBase):

    #class Meta:
        #verbose_name_plural="client addresses"

class Client(models.Model):
    code = models.CharField(max_length=18, unique=True)
    address = models.ForeignKey(Address)
    objects = InheritanceManager()
    #clientaddress = models.OneToOneField(ClientAddress)

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
    clients = models.ManyToManyField(Client)

    def __unicode__(self):
        return self.name

class ProductProvider(models.Model):
    name = models.CharField(max_length=64)

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
        return u'%s - %s' % (self.code, self.name)

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
    notional_currency = models.ForeignKey(Currency, related_name="purchase_notional_currency")
    duration = models.IntegerField(blank=True)
    signature_date = models.DateField()
    syndicate = models.ForeignKey(Syndicate, blank=True)
    date_funds_to_syndicate = models.DateTimeField()
    shares_no = models.IntegerField()
    shares_value = models.IntegerField()
    shares_currency = models.ForeignKey(Currency, related_name="purchase_shares_currency")
    shares_cert_date = models.DateField()
    shares_cert_sent_date = models.DateField()
    notes = models.TextField()

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
    base_currency = models.ForeignKey(Currency, related_name="rent_base_currency")
    base_amount = models.IntegerField()
    fixed_fee_added_currency = models.ForeignKey(Currency, related_name="rent_fixed_fee_added_currency")
    fixed_fee_added_amount = models.IntegerField()
    variable_fee_added_rate_bps = models.IntegerField()
    variable_fee_added_amount = models.IntegerField()
    fixed_fee_deducted_currency = models.ForeignKey(Currency, related_name="rent_fixed_fee_deducted_currency")
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

    class Meta:
        verbose_name_plural="rent"

#class UserInput(models.Model):
    #createddate = models.DateTimeField()
    #createdby_id = models.IntegerField()
    #updateddate = models.DateTimeField()
    #updatedby_id = models.IntegerField()
