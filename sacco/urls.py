"""
URL configuration for sacco project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import  static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('main.urls', "main"), namespace="main")),
    path("sysadmin/", include(("sysadmin.urls", "sysadmin"), namespace="sysadmin")),
    path('frontdesk/', include(('frontdesk.urls', "frontdesk"), namespace="frontdesk")),
    path('finance/', include(('finance.urls', "finance"), namespace="finance")),
    path('hr/', include(('hr.urls', "hr"), namespace="hr")),
    path('administrator/', include(('administrator.urls', "administrator"), namespace="administrator")),
    path('procurement/', include(('procurement.urls', "procurement"), namespace="procurement")),
    path('stores/', include(('stores.urls', "stores"), namespace="stores")),
    path('qm/', include(('qm.urls', "qm"), namespace="qm")),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)


