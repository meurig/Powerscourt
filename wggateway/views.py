from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail
from django.shortcuts import render_to_response
from wggateway.models import Client
from wggateway.forms import ContactForm, ClientSearchForm

def search(request):
    if request.method == 'POST':
    #if 'q' in request.GET:
        q = request.GET['q']
        #if not q:
            #error = True
        #else:
            #clients = Client.objects.filter(code__icontains=q)
            #return render_to_response('search_results.html',
                    #{'clients': clients, 'query': q})
    else:
        form = ClientSearchForm()
    return render_to_response('search_form.html', {'form': form})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            send_mail(
                    cd['subject'],
                    cd['message'],
                    cd.get('email', 'noreply@email.com'),
                    ['me@meurig.com'],
                    )
            return HttpResponseRedirect('/contact/thanks/')
    else:
        form = ContactForm()
    return render_to_response('contact_form.html', {'form': form})
