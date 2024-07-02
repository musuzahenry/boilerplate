
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate
from . global_views import GlobalView
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import Employee, SystemRoles



#our constals
GLOBAL_DEFS = GlobalView()


class ManageUsers:

    def create_user(request):
        if request.method == "POST":
            form = RegistrationForm(request.POST)

            if request.is_valid():
                form.save()
                return redirect("login")
            else:
                form = RegistrationForm()
        return render(request, template_name="systmadmin/registration_form.html", context={"form":form})

