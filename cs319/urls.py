

from django.conf.urls import include, url
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [

    url(r'^$', views.login, name='login'), #PO
    url(r'^dashboard$', views.authview, name='dashboard'), #PO
    url(r'^logout$', views.logout, name='logout'), #PO
    url(r'^invalidlogin$', views.invalidlogin, name='invalidlogin'), #PO

    url(r'^dashboard/', include('web_app.urls')),
    url(r'^admin/', admin.site.urls),
    static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
]