from django.conf.urls import url
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    url(r'^$', views.get_device_ids, name='get_device_ids'),
    url(r'^login$', views.login, name='login'), #PO
    url(r'^authview$', views.authview, name='authview'), #PO
    url(r'^logout$', views.logout, name='logout'), #PO
    url(r'^loggedin$', views.loggedin, name='loggedin'), #PO
    url(r'^invalidlogin$', views.invalidlogin, name='invalidlogin'), #PO

    url(r'^(?P<watch_id>\d+)$', views.analyze_device, name='analyze_device'),
    #url(r'^$', views.get_device_ids, name='get_device_ids'),

    # url(r'^demo$', views.demo, name='demo'),

    url(r'^live/(?P<watch_id>\d+)$', views.live, name='live'),

    static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
]
