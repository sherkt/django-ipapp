from django.contrib import admin

from .models import GeoIP

class GeoIPAdmin(admin.ModelAdmin):
    list_display = ['ip_address', 'city', ]
    readonly_fields = ['date_created', 'last_activity', ]
admin.site.register(GeoIP, GeoIPAdmin)
