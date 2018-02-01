from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import IpForm
from .utils import get_info, save_results, get_recent

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

    # IPs for testing:
    # 70.50.132.61, 70.51.86.38, 174.95.4.182, 174.95.5.131
    # 174.92.70.244, 65.95.139.12, 64.231.105.123

    queries = get_recent(request)
    return render(request, 'ipapp/home.html', {'form': form, 'queries': queries})
