from datetime import datetime
import pytz

from django.template import Library


def date_string(value):
    utc = pytz.utc
    if isinstance(value, str):
        try:
            value = datetime.strptime(value[:-1], "%Y-%m-%dT%H:%M:%S")
            value = value.replace(tzinfo=utc)
        except ValueError:
            pass
    return value


register = Library()
register.filter('date_string', date_string)
