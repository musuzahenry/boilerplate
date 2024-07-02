from django.urls import path
from  stores . views import *



urlpatterns =[
    #user view urls
    path("", Index.index_views, name="index"),
    #path("register-client", FrontDesk.frontdesk_dashboard, name="frontdesk-dashboard"),
]