from django.urls import path
from django.contrib.auth.views  import LogoutView
from sysadmin.views import *


urlpatterns =[
    #user view urls
    path("", Index.index_views, name="index"),
    path("system-admin-dashboard", Index.system_admin_dashboard, name="system-admin-dashboard"),
    path("logout", Index.logoout, name="logout"),
]