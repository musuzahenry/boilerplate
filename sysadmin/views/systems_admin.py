from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from sysadmin.models import Employee, SystemRoles
from global_views . global_views import GlobalView



GLOBAL_DEFS = GlobalView()

class SystemsAdminViews:

    def system_admin_dashboard(request):
               
        user_employee=None
        role_list = None
        current_user = ""

        access_obj = GLOBAL_DEFS.check_current_user_rights(request, "sysadmin")      
        if access_obj["is_logged_in"] and access_obj["allow_to_pass"]:
            pass
        else:
            return redirect("main:index")
        
        current_employee =  access_obj["current_employee"]

        try:
            user_employee = Employee.objects.get(id = int(request.session["current_employeeID"]))
        except:
            user_employee = Employee.objects.filter(businessID = current_employee.businessID).order_by("-id")[0]

    

        #get rolses list
        role_list = SystemRoles.objects.filter(stationID = current_employee.stationID)
                
        try:
            current_user = user_employee.userID
        except:
            pass
        
        if request.POST.get("add-new-user"):
            if user_employee is None:
                messages.warning(request, "Please first load employee into window")
                return redirect(request.path)

            username = request.POST.get("add-username")
            password = request.POST.get("passw")
            confirm_password = request.POST.get("confirm-passw")
            roleID = request.POST.get("roleID")

            sys_admin_action = SystemAdminActions()
            userID = user_employee.userID
            sys_admin_action.add_user(request, userID, user_employee, username, password, confirm_password)
        
        
        if request.POST.get("is-system-user"):
            if user_employee is None:
                messages.warning(request, "Please first load employee into window")
                return redirect(request.path)
            if request.POST.get("is-system-user") =="Yes":
                is_system_user = True
                is_active = True
            else:
                is_system_user = False
                is_active = False

            sys_admin_action = SystemAdminActions()
            
            roleID = request.POST.get("system-roleID")
            sys_admin_action.make_system_user(request, user_employee, is_system_user, is_active, roleID)  

        return render(request, 
                      template_name="sysadmin/system_admin_dashboard.html",
                      context ={
                        "user_employee":user_employee,  
                        "current_user":current_user, 
                        "role_list":role_list,                  
                      }
                      )






class SystemAdminActions:
    def add_user(self, request, userID, employee, username, passsord, confirm_password):
          

        if not(passsord == confirm_password):
            messages.warning(request, "Passwords don't match please try again")
            return redirect(request.path)

        if userID is None:
             new_user = User()
             new_user.username = username
             new_user.password = make_password(passsord)
             new_user.is_active = True
             new_user.save()

             employee.userID = new_user
             
             employee.save()

             messages.info(request, "Success, new user added!")
        else:
             userID.passsord = userID.set_password(passsord)
             userID.save()
             employee.save()

             messages.info(request, "Success, password updated!")

             return redirect(request.path)





    def make_system_user(self, request, employee,  is_system_user, is_active,  roleID):

        if employee.userID is None:
            messages.warning(request, "Please first create a username and password for this person")
            return redirect(request.path)

        employee.is_system_user = is_system_user
        employee.userID.is_active = is_active
        employee.system_roleID = SystemRoles.objects.get(id=int(roleID))
        try:
           employee.positionID = employee.positionID
        except:
            pass

        employee.userID.save()
        employee.save()
        messages.info(request, "Success, user updated")

        
