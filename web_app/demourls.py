from django.conf.urls import url
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    url(r'^$', views.demo, name='demo'),
    url(r'^live$', views.liveData, name='liveData'),
    static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
    ]
