from django.conf.urls import url
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    url(r'^$', views.get_device_ids, name='get_device_ids'),
    url(r'^(?P<watch_id>\d+)$', views.analyze_device, name='analyze_device'),
    # url(r'^demo$', views.demo, name='demo'),
    url(r'^live/(?P<watch_id>\d+)$', views.live, name='live'),
    url(r'^live-with-date/(?P<watch_id>\d+)/$', views.live_with_date_range, name='live_with_date_range'),

    static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
]
