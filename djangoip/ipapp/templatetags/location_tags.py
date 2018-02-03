from django.template import Library


def location_string(location):
    s = [location.get('city'), location.get('region_code'), location.get('country_name')]
    return ', '.join([x for x in s if x])

register = Library()
register.filter('location_string', location_string)
