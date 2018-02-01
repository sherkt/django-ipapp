import requests

from .models import GeoIP

def get_info():
    return "Success"

def save_results(request, ip):
    geoip = GeoIP.objects.filter(
        ip_address__iexact=ip
    ).first()

    if not geoip:
        geoip = GeoIP.objects.create(
            ip_address=ip.lower(),
        )

    geoip.city = 'Ottawa'
    geoip.province = 'Ontario'
    geoip.country_code = 'CA'
    geoip.save()

    request.session["queries"][ip] = geoip.pk

    return geoip
