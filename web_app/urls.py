from django.conf.urls import url
from . import views
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    url(r'^$', views.build_dashboard, name='build_dashboard'),
    url(r'^(?P<watch_id>\d+)$', views.analyze_device, name='analyze_device'),

    url(r'^live-accel/(?P<watch_id>[\w\+%_& ]+)$', views.build_accel_api, name='build_accel_api'),
    url(r'^live-accel-date/(?P<watch_id>[\w\+%_& ]+)/$', views.build_accel_api_with_date, name='build_accel_api_with_date'),

    url(r'^live-battery/(?P<watch_id>[\w\+%_& ]+)$', views.build_battery_api, name='build_battery_api'),
    url(r'^live-battery-date/(?P<watch_id>[\w\+%_& ]+)/$', views.build_battery_api_with_date, name='build_battery_api_with_date'),

    static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
]
