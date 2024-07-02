from django.urls import path
from django.contrib.auth.views  import LogoutView
from main.views import *



urlpatterns =[
    #user view urls
    path("", Index.index_views, name="index"),
]