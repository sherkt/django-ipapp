from datetime import datetime

from django.template import Library
from django.template.defaultfilters import date as date_filter


def date_string(value, arg=None):
    if isinstance(value, str):
        try:
            value = datetime.strptime(value[:-1], "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            pass
    return date_filter(value, arg)


register = Library()
register.filter('date_string', date_string)
