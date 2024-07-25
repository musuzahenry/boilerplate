from django.urls import path
from frontdesk . views import *



urlpatterns =[
    #user view urls
    path("", Index.index_views, name="index"),

    #client views
    path("add-client", ClientCreateView.as_view(), name="add-client"),
    path("list-clients", ClientListView.as_view(), name="list-clients"),
    path("set-current-client-by-click/<int:id>", ClientViews.set_current_client_by_click, name = "set-current-client-by-click"),
    path("client-update/<int:pk>/", ClientUpdateView.as_view(), name="client-update"),
    path("client-details/<int:pk>", ClientDetailView.as_view(), name="client-details"),
    path("delete-client/<int:id>/", ClientViews.delete_client, name="delete-client"),
    path("update-client-kin/<int:id>/", NextOfKinViews.update_client_kin, name="update-client-kin"),
    path("create-next-of-kin/<int:id>", NextOfKinViews.creat_next_of_kin, name="create-next-of-kin"),

    #path("register-client", FrontDesk.frontdesk_dashboard, name="frontdesk-dashboard"),
]