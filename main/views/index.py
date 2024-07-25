from django.shortcuts import render, redirect
from django.contrib import messages
from global_views.global_views import GlobalView

# Create your views here.

GLOBAL_DEFS = GlobalView()
class Index:
    #views that are common to all apps

    def index_views(request):
        #dashboard redirections
        #Triggered from main/header
        #===============================================
        if request.user.is_authenticated:
            pass
        else:
            return redirect("sysadmin:index")

        if request.POST.get("dashboard-redirect"):
            if request.POST.get("dashboard-redirect") == "NA":
               pass
            else:

                #check if user is allowed to access these resources
                access_obj = GLOBAL_DEFS.check_current_user_rights(              
                                                                request, 
                                                                right_name =request.POST.get("dashboard-redirect").split(":")[0]
                                                                 )
                if access_obj["allow_to_pass"] and access_obj["is_logged_in"]:   
                    #set the header before reirection and foooter
                    GLOBAL_DEFS.set_dashboard_header_and_footer(request, request.POST.get("dashboard-redirect"))
                    return redirect (request.POST.get("dashboard-redirect"))

                else:
                    return redirect(access_obj["current_employee"].system_roleID.module_settings+":index")




            

        return render(request, template_name="main/index.html")