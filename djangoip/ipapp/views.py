from django.core.exceptions import ValidationError
from django.core.validators import validate_ipv46_address
from django.shortcuts import render, redirect, reverse

from .forms import IpForm
from .models import GeoIP
from .utils import save_results, get_recent


def home(request):
    data = None
    ip_address = ''
    if request.method == 'POST':
        form = IpForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            ip_address = cd.get('ip')
            geoip = save_results(request, ip_address)

            data = geoip

            return redirect(reverse('home') + "?ip=" + ip_address)

            # page, error = get_page(cd["url"])
            # if error:
            #     return render(request, 'ipapp/home.html', dict(
            #         form=form, error=error
            #     ))
            # else:
            #     result = save_results(request, cd, page)
        else:
            ip_address = request.POST.get('ip')
    else:
        form = IpForm()
        if request.GET.get('ip'):
            ip_address = request.GET.get('ip')
            try:
                validate_ipv46_address(ip_address)
                geoip = GeoIP.objects.filter(ip_address=ip_address).first()
                if geoip:
                    data = geoip
            except ValidationError:
                return redirect('home')
        else:
            ip_address = request.META.get('REMOTE_ADDR')

    # IPs for testing:
    # 70.50.132.61, 70.51.86.38, 174.95.4.182, 174.95.5.131
    # 174.92.70.244, 65.95.139.12, 64.231.105.123

    queries = get_recent(request)
    return render(request, 'ipapp/home.html', {
        'data': data, 'form': form, 'queries': queries,
        'ip_address': ip_address,
    })
