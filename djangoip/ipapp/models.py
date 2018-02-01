from django.db import models
from django.utils.timezone import now

class GeoIP(models.Model):
    ip_address = models.CharField(max_length=200, unique=True)
    city = models.CharField(max_length=200, blank=True)
    province = models.CharField(max_length=200, blank=True)
    country_code = models.CharField(max_length=2, blank=True)
    zip_code = models.CharField(max_length=20, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(default=now)

    def __str__(self):
        return u"%s" % (self.ip_address)

    class Meta:
        ordering = ("ip_address", )
