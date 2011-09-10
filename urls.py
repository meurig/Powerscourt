from django.conf.urls.defaults import *
from wggateway import views
from django.views.generic import DetailView, ListView, TemplateView
from wggateway.models import Client, GroupOfPeople, Sipp, Product, Purchase, ProductProvider

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^wggateway/', include('wggateway.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    url(r'^chaining/', include('smart_selects.urls')),

    url(r'^product/$', views.product, name='product'),
    url(r'^home/$', TemplateView.as_view(template_name="home.html"), name="home"),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^clients/(?P<page>[0-9]*)$', ListView.as_view(
        queryset=Client.objects.all().select_subclasses(),
        context_object_name="client_list",
        template_name="client_list.html",
        paginate_by=25,
        ), name="clients"),
    url(r'^clients/people/(?P<page>[0-9]*)$', ListView.as_view(
        queryset=GroupOfPeople.objects.all(),
        context_object_name="client_list",
        template_name="client_list.html",
        paginate_by=25,
        ), name="clients_people"),
    url(r'^clients/sipps/(?P<page>[0-9]*)$', ListView.as_view(
        queryset=Sipp.objects.all(),
        context_object_name="client_list",
        template_name="client_list.html",
        paginate_by=25,
        ), name="clients_sipps"),
    url(r'^clients/other/(?P<page>[0-9]*)$', ListView.as_view(
        queryset=filter((lambda x: not isinstance(x, GroupOfPeople) and not isinstance(x, Sipp)), Client.objects.all().select_subclasses()),
        context_object_name="client_list",
        template_name="client_list.html",
        paginate_by=25,
        ), name="clients_other"),
    url(r'^client/(?P<pk>\w+)/$', DetailView.as_view(
        queryset=Client.objects.all().select_subclasses(),
        context_object_name="client",
        template_name="client_detail.html",
        ), name="client"),
    url(r'^clientsearch/$', views.clientsearch),
    url(r'^products/(?P<page>[0-9]*)$', ListView.as_view(
        queryset=Product.objects.all(),
        template_name="product_list.html",
        paginate_by=25,
        ), name="products"),
    url(r'^product/(?P<pk>\w+)/$', DetailView.as_view(
        queryset=Product.objects.all(),
        template_name="product_detail.html",
        )),
    url(r'^product_provider/(?P<pk>\w+)/$', DetailView.as_view(
        queryset=ProductProvider.objects.all(),
        template_name="product_provider_detail.html",
        ), name="product_provider"),
    url(r'^purchases/(?P<page>[0-9]*)$', ListView.as_view(
        queryset=Purchase.objects.all(),
        template_name="purchase_list.html",
        paginate_by=25,
        ), name="purchases"),
    url(r'^purchase/(?P<pk>\w+)/$', DetailView.as_view(
        queryset=Purchase.objects.all(),
        template_name="purchase_detail.html",
        ), name="purchase"),
)
