import requests

from .models import GeoIP


def get_info(ip):
    data = requests.get('http://freegeoip.net/json/' + ip)
    if data.status_code == 200:
        return data.json()
    else:
        return None


def get_recent(request):
    queries = []
    if request.session.get('queries'):
        for key, value in request.session.get('queries').items():
            geoip = GeoIP.objects.filter(pk=value).first()
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

    if not geoip.country_code:
        json = get_info(ip)
        if json:
            geoip.city = json.get('city')
            geoip.province = json.get('region_name')
            geoip.country_code = json.get('country_code')
            geoip.zip_code = json.get('zip_code')
            geoip.save()

    if request.session.get('queries'):
        request.session["queries"][ip] = geoip.pk
        request.session.modified = True
    else:
        request.session["queries"] = {ip: geoip.pk}

    return geoip
