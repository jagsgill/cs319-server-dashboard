from django.conf.urls import url
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    #url(r'^$', views.index, name='index'),
    url(r'^$', views.getDevices, name='getDevices'),
    url(r'^demo$', views.demo, name='demo'),
    url(r'^live$', views.live, name='live'),
    static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    ]
