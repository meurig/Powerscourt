from django.conf.urls.defaults import *
from wggateway import views
from django.views.generic import DetailView, ListView, TemplateView
from wggateway.models import Client, GroupOfPeople

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

    url(r'^product/$', views.product, name='product'),
    url(r'^home/$', TemplateView.as_view(template_name="home.html"), name="home"),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^clients/(?P<page>[0-9]*)$', ListView.as_view(
        queryset=Client.objects.all().select_subclasses(),
        template_name="client_list.html",
        paginate_by=25,
        ), name="clients"),
    url(r'^client/(?P<pk>\w+)/$', DetailView.as_view(
        #model=Client,
        queryset=Client.objects.all().select_subclasses(),
        template_name="client_detail.html",
        )),
    url(r'^clientsearch/$', views.clientsearch),
    url(r'^group/(?P<pk>\w+)/$', DetailView.as_view(
        model=GroupOfPeople,
        template_name="group_detail.html",
        )),
)
