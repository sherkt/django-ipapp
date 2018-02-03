import requests

from django.conf import settings
from django.core.cache import cache
from django.utils.timezone import now

from eventregistry import (EventRegistry, QueryArticles,
                           RequestArticlesInfo, ReturnInfo)

from .models import GeoIP
from .templatetags import location_tags

TIMEOUT = 3600


def call_api(url, method='GET'):
    if method == 'POST':
        response = requests.post(url)
    else:
        response = requests.get(url)
    return response.json() if response.status_code == 200 else None


def get_location(ip):
    url = 'http://freegeoip.net/json/' + ip
    return call_api(url)


def get_weather(city, country_code):
    key = getattr(settings, 'OPENWEATHER_KEY', '')
    if country_code == 'US':
        units = 'imperial'
        symbol = 'F'
    else:
        units = 'metric'
        symbol = 'C'

    url = ('http://api.openweathermap.org/data/2.5/weather?'
           'q=' + city + ',' + country_code + '&'
           'units=' + units + '&'
           'APPID=' + key + '')
    response = call_api(url)
    if response:
        response['symbol'] = symbol
    return response


def get_newsapi(country_code):
    """Calls newsapi.org API which isn't as advanced as EventRegistry.org"""
    key = getattr(settings, 'NEWSAPI_KEY', '')
    url = ('https://newsapi.org/v2/top-headlines?'
           'country=' + country_code + '&'
           'pageSize=5&'
           'apiKey=' + key + '')
    return call_api(url)


def get_news(country, city):
    """Calls EventRegistry.org API"""
    key = getattr(settings, 'EVENTREGISTRY_KEY', '')
    er = EventRegistry(apiKey=key)
    q = QueryArticles(
        locationUri=er.getLocationUri(city),
        keywords=country,
    )
    q.setRequestedResult(
        RequestArticlesInfo(page=1, count=5, sortBy='date',
                            sortByAsc=False, returnInfo=ReturnInfo())
    )
    response = er.execQuery(q)
    return response


def maps_api_key():
    return getattr(settings, 'MAPSAPI_KEY', '')


def maps_url(location):
    if location.get('city'):
        s = location_tags.location_string(location)
        return 'https://www.google.ca/maps/?q=' + s
    elif location.get('longitude'):
        return 'https://www.google.ca/maps/@%s,%s,6z' % (location.get('latitude'), location.get('longitude'))
    else:
        return 'https://www.google.ca/maps/?q=' + location.get('country_name')

def weather_url(location):
    base = 'https://www.theweathernetwork.com/'
    url = base + '%s/weather/%s/%s' % (location.get('country_code'), location.get('region_name'), location.get('city'))
    return url


def get_recent(request):
    queries = []
    if request.session.get('queries'):
        for key, value in request.session.get('queries').items():
            queries.append({
                'ip_address': key,
                'date': value.get('date'),
                'city': value.get('city'),
                'country_code': value.get('country_code'),
            })
    return queries


def get_or_set_cache(request, ip_address):
    data = cache.get(ip_address)
    if not data:
        data = save_results(request, ip_address)
        data.last_updated = now()
        cache.set(ip_address, data, TIMEOUT)

    update_session(request, ip_address, data.location)

    return data


def update_session(request, ip_address, location):
    cache_data = {'date': now().isoformat(),
                  'city': location.get('city'),
                  'country_code': location.get('country_code'), }

    if request.session.get('queries'):
        request.session["queries"][ip_address] = cache_data
        request.session.modified = True
    else:
        request.session["queries"] = {ip_address: cache_data}

    return cache_data


def save_results(request, ip):
    geoip = GeoIP.objects.filter(ip_address__iexact=ip).first()

    if not geoip:
        geoip = GeoIP.objects.create(ip_address=ip)

    weather = news = None

    location = get_location(ip)
    if location:
        geoip.city = location.get('city')
        geoip.province = location.get('region_name')
        geoip.country_code = location.get('country_code')
        geoip.zip_code = location.get('zip_code')
        geoip.save()

    if geoip.country_code and geoip.city:
        weather = get_weather(geoip.city, geoip.country_code)

    news = get_news(location.get('country'), geoip.city)

    geoip.location = location
    geoip.weather = weather
    geoip.news = news

    return geoip
