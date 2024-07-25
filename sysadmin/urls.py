from django.urls import path
from django.contrib.auth.views  import LogoutView
from sysadmin.views import *


urlpatterns =[
    #user view urls
    path("", Index.index_views, name="index"),
    path("system-admin-dashboard", SystemsAdminViews.system_admin_dashboard, name="system-admin-dashboard"),
    path("list-system-roles",  SystemRoleViews.list_system_roles, name="list-system-roles"),
    path("list-role-rights/<int:id>", RoleRightsViews.list_role_rights, name="list-role-rights"),
    path("list-rights",RightViews.list_rights, name="list-rights"),
    path("logout", Index.logoout, name="logout"),
]