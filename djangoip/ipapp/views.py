from django.shortcuts import render, redirect
from django.http import HttpResponse

from .forms import IpForm
from .utils import get_info

# Create your views here.
def home(request):
    if request.method == 'POST':
        form = IpForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            ip_address = cd.get('ip')
            geoip = save_results(request, ip_address)

            # page, error = get_page(cd["url"])
            # if error:
            #     return render(request, 'ipapp/home.html', dict(
            #         form=form, error=error
            #     ))
            # else:
            #     result = save_results(request, cd, page)

            # return redirect('results')
        # else:
            # return HttpResponse("In valid")
    else:
        form = IpForm()

    if request.session.get('queries'):
        print("GOT HERE 2")
        queries = []
    else:
        queries = None
    queries = {
        '70.50.132.61':{'city':'Kanata','province':'Ontario'},
        '70.51.86.38':{'city':'Kanata','province':'Ontario'},
        '174.95.4.182':{'city':'Kanata','province':'Ontario'},
        '174.95.5.131':{'city':'Kanata','province':'Ontario'},
        '174.92.70.244':{'city':'Kanata','province':'Ontario'},
        '65.95.139.12':{'city':'Kanata','province':'Ontario'},
        '64.231.105.123':{'city':'Kanata','province':'Ontario'},
    }
    return render(request, 'ipapp/home.html', {'form': form, 'queries': queries})
