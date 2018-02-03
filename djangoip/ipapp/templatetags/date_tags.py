from datetime import datetime
import pytz

from django.template import Library

register = Library()


@register.filter(name="date_string")
def date_string(value, arg=None):
    utc = pytz.utc
    if isinstance(value, str):
        try:
            value = datetime.strptime(value[:-1], arg)
            value = value.replace(tzinfo=utc)
        except ValueError:
            pass
    return value


@register.filter(name="utc_unix_string")
def utc_unix_string(value):
    utc = pytz.utc
    try:
        value = datetime.utcfromtimestamp(value)
        value = value.replace(tzinfo=utc)
    except ValueError:
        pass
    return value
