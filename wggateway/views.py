from django.shortcuts import render_to_response
from django.db.models import Q
from models import Client
from forms import ClientSearchForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView, TemplateView

@login_required
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
                    { 'client_list': clients.select_subclasses() })
    else:
        form = ClientSearchForm()
    return render_to_response('search_form.html', {'form': form})

class DetailViewLocked(DetailView):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(DetailViewLocked, self).dispatch(*args, **kwargs)

class ListViewLocked(ListView):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ListViewLocked, self).dispatch(*args, **kwargs)

class TemplateViewLocked(TemplateView):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TemplateViewLocked, self).dispatch(*args, **kwargs)
