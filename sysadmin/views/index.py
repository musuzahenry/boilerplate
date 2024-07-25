from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from sysadmin.forms import RegistrationForm, LoginForm
from django.contrib import messages
from sysadmin.models import SystemSetings
from global_views . global_views import  GlobalView





#our constals
GLOBAL_DEFS = GlobalView()

class Index:

    def index_views(request):

        sys_info = GLOBAL_DEFS.get_sys_info(request)

        if request.method == "POST" and not request.user.is_authenticated:
            form = LoginForm(request.POST)
        
            if form.is_valid():
                #clean the data
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                #now authenticate user
                user = authenticate(request, username=username, password=password)

                if user is not None:
                    login(request, user)

                    #initialize app
                    current_employee = GLOBAL_DEFS.initialize_app(request)#returns an employee obj
                    messages.info(request, "Success, you are now logged in")

                    #set dashboard header and footer before redirect
                    GLOBAL_DEFS.set_dashboard_header_and_footer(
                                                              request,
                                                              current_employee.system_roleID.module_settings+":index"
                                                              )
                    #then redirect to that dashboard
                    return redirect(current_employee.system_roleID.module_settings+":index")
                    
                else:
                    messages.info(request, "Invalid username or password")

        else:
                form = LoginForm()
             
        #if user is already logged in, just redirect to the sys admin dahboard
        if request.user.is_authenticated:
          return redirect ("sysadmin:system-admin-dashboard")
            
        return render (request, template_name="sysadmin/index.html", context={"form":form, "sys_info":sys_info,})




    def logoout(request):
        logout(request)
        return redirect("sysadmin:index")




