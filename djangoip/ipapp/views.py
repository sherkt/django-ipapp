from django.core.exceptions import ValidationError
from django.core.validators import validate_ipv46_address
from django.shortcuts import render, redirect, reverse

from .forms import IpForm
from .models import GeoIP
from .utils import (get_or_set_cache, get_recent,
                    maps_api_key, maps_url, weather_url)


def home(request):
    data = None
    ip_address = ''

    if request.method == 'POST':
        form = IpForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            ip_address = cd.get('ip')

            data = get_or_set_cache(request, ip_address)
            return redirect(reverse('home') + "?ip=" + ip_address)
        else:
            ip_address = request.POST.get('ip')
    else:
        form = IpForm()
        if request.GET.get('ip'):
            ip_address = request.GET.get('ip')
            try:
                validate_ipv46_address(ip_address)
            except ValidationError:
                return redirect('home')
            geoip = GeoIP.objects.filter(ip_address__iexact=ip_address).first()
            if geoip:
                data = get_or_set_cache(request, ip_address)
        else:
            if request.META.get('HTTP_X_FORWARDED_FOR'):
                ip_address = request.META.get('HTTP_X_FORWARDED_FOR').split(",")[0].strip()
            else:
                ip_address = request.META.get('REMOTE_ADDR')

    queries = get_recent(request)
    if data:
        maps_key = maps_api_key()
        maps_link = maps_url(data.location)
        weather_link = weather_url(data.location)
    else:
        maps_key = maps_link = weather_link = ''

    return render(request, 'ipapp/home.html', {
        'data': data, 'form': form, 'queries': queries,
        'ip_address': ip_address,
        'maps_api_key': maps_key,
        'maps_link': maps_link,
        'weather_link': weather_link,
    })
