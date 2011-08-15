from django.conf.urls.defaults import *
from wggateway import views
#from django.views.generic import list_detail
from django.views.generic import ListView
from django.views.generic import DetailView
from wggateway.models import Client, GroupOfPeople

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

client_info = {
            "queryset" : Client.objects.all(),
            "template_name" : "client_list.html",
            "template_object_name" : "client",
            }

urlpatterns = patterns('',
    # Example:
    # (r'^wggateway/', include('wggateway.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    (r'^search/$', views.search),
    (r'^contact/$', views.contact),
    (r'^product/$', views.product),
    (r'^clients/(?P<page>[0-9]*)$', ListView.as_view(
        #model=Client,
        queryset=Client.objects.all().select_subclasses(),
        template_name="client_list.html",
        paginate_by=30,
        )),
    (r'^client/(?P<pk>\w+)/$', DetailView.as_view(
        #model=Client,
        queryset=Client.objects.all().select_subclasses(),
        template_name="client_detail.html",
        )),
    (r'^clientsearch/$', views.clientsearch),
    (r'^group/(?P<pk>\w+)/$', DetailView.as_view(
        model=GroupOfPeople,
        template_name="group_detail.html",
        )),
)
