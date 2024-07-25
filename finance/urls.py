from django.urls import path
from  finance . views import *



urlpatterns =[
    #user view urls
    path("", Index.index_views, name="index"),
    path("list-cashbook", CashbookViews.list_cashbook, name="list-cashbook"),
]