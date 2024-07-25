

from django.shortcuts import render, redirect
from django.contrib import messages
from sysadmin.models import  Rights
from global_views . global_views import GlobalView


GLOBAL_DEFS = GlobalView()


class RightViews:
    def list_rights(request):

        #check if user is logged in or redirect to login page 
        access_obj = GLOBAL_DEFS.check_current_user_rights(request)      
        if access_obj["is_logged_in"] and access_obj["allow_to_pass"]:
            pass
        else:
            return redirect("main:index")
        
        current_employee =  access_obj["current_employee"]


        rights_list = Rights.objects.filter(stationID = current_employee.stationID) 


        return render(request, 
                      template_name = "sysadmin/list_rights.html", 
                      context={
                        "rights_list":rights_list,
                      }
                      )

