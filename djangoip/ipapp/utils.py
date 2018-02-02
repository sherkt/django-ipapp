import requests

from .models import GeoIP


def get_info():
    data = requests.get('http')
    return data


def get_recent(request):
    queries = []
    if request.session.get('queries'):
        for key, value in request.session.get('queries').items():
            geoip = GeoIP.objects.get(pk=value)
            if geoip:
                queries.append({
                    'ip_address': geoip.ip_address,
                    'pk': geoip.pk,
                    'date': geoip.last_activity
                })

    return queries


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

    if request.session.get('queries'):
        request.session["queries"][ip] = geoip.pk
        request.session.modified = True
    else:
        request.session["queries"] = {ip: geoip.pk}

    return geoip
