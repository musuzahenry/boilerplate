from django.shortcuts import render

# Create your views here.

from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from .forms import RegistrationForm, LoginForm
from django.contrib import messages
from .models import SystemSetings

from global_views . global_views import GlobalView



#our constals
GLOBAL_DEFS = GlobalView()

class Index:

    def register(request):
        if request.method == "POST":
            form = RegistrationForm(request.POST)

            if request.is_valid():
                form.save()
                return redirect("login")
            else:
                form = RegistrationForm()
        return render(request, template_name="systmadmin/registration_form.html", context={"form":form})



    def index_views(request):

        sys_info = GLOBAL_DEFS.get_sys_info(request)

        if request.method == "POST":
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
                    current_employee = GLOBAL_DEFS.initialize_app(request)
                    messages.info(request, "Success, you are now logged in")

                    return redirect (current_employee.system_roleID.module_settings)
                    
                else:
                    messages.info(request, "Invalid username or password")

        else:
                form = LoginForm()
            
        return render (request, template_name="systmadmin/index.html", context={"form":form, "sys_info":sys_info,})



    def logoout(request):
        logout(request)
        return redirect("login")


