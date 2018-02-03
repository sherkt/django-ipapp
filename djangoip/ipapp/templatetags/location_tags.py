from django.template import Library

register = Library()


@register.filter(name="location_string")
def location_string(location):
    s = [location.get('city'), location.get('region_code'),
         location.get('country_name')]
    return ', '.join([x for x in s if x])
