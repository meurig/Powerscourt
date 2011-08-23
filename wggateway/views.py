from django.shortcuts import render_to_response
from django.db.models import Q
from wggateway.models import Client
from wggateway.forms import ClientSearchForm, ProductForm

def clientsearch(request):
    if request.method == 'POST':
        form = ClientSearchForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if (cd['post_code'] != '' or cd['email'] != ''):
                clients=Client.objects.filter(
                        Q(code__icontains=cd['client_code']),
                        Q(address__postcode__icontains=cd['post_code']),
                        Q(address__email1__icontains=cd['email'])|
                        Q(address__email2__icontains=cd['email']))
            else:
                clients=Client.objects.filter(
                        Q(code__icontains=cd['client_code']))
            return render_to_response('search_results.html',
                    { 'clients': clients })
    else:
        form = ClientSearchForm()
    return render_to_response('search_form.html', {'form': form})

def product(request):
    form = ProductForm()
    return render_to_response('product_form.html', {'form': form})
