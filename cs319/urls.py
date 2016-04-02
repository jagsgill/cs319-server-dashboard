    """cs319 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import include, url
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [

    url(r'^$', views.login, name='login'), #PO
    url(r'^dashboard$', views.authview, name='dashboard'), #PO
    url(r'^logout$', views.logout, name='logout'), #PO
    url(r'^loggedin$', views.loggedin, name='loggedin'), #PO
    url(r'^invalidlogin$', views.invalidlogin, name='invalidlogin'), #PO

    url(r'^dashboard/', include('web_app.urls')),
    url(r'^admin/', admin.site.urls),
    static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
]