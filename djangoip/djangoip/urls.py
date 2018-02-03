from django.contrib import admin
from django.urls import path

from ipapp import views


handler404 = views.page_not_found
handler500 = views.server_error

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
]
