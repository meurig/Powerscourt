# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

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

    def __unicode__(self):
        return u'%s, %s' % (self.postcode, self.address1)

    class Meta:
        abstract = True

class Address(AddressBase):

    class Meta:
        verbose_name_plural="addresses"

class Client(models.Model):
    code = models.CharField(max_length=18, unique=True)
    address = models.ForeignKey(Address)

    def __unicode__(self):
        return self.code

class Person(models.Model):
    title = models.CharField(max_length=48)
    firstname = models.CharField(max_length=192)
    middlename = models.CharField(max_length=192, blank=True)
    lastname = models.CharField(max_length=192)

    def __unicode__(self):
        return u'%s, %s' % (self.lastname, self.firstname)

    class Meta:
        verbose_name_plural="people"

class GroupOfPeople(Client):
    people = models.ManyToManyField(Person, blank=True)

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
    address = models.ForeignKey(Address)

    def __unicode__(self):
        return u'%s %s' % (self.firstname, self.lastname)

    class Meta:
        verbose_name_plural="sipp admin people"

class Sipp(Client):
    company = models.ForeignKey(SippProvider)
    reference = models.CharField(max_length=64)
    admin_person = models.ForeignKey(SippAdminPerson)

    def __unicode__(self):
        return u'%s %s' % (self.company, self.reference)

class LLC(Client):
    name = models.CharField(max_length=64)

    def __unicode__(self):
        return u'%s' % (self.name)

class OldAddress(AddressBase):
    client = models.ForeignKey(Client)
    deprication_date = models.DateField()

    def __unicode__(self):
        return u'%s, %s' % (self.postcode, self.address1)

    class Meta:
        verbose_name_plural="old addresses"

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

#class UserInput(models.Model):
    #createddate = models.DateTimeField()
    #createdby_id = models.IntegerField()
    #updateddate = models.DateTimeField()
    #updatedby_id = models.IntegerField()
