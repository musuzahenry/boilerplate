
from django.shortcuts import render, redirect
from django.contrib import messages
from sysadmin.models import SystemRoles, Employee
from global_views . global_views import GlobalView

GLOBAL_DEFS = GlobalView()


class SystemRoleViews:

    def list_system_roles(request):
        
        #check if user is logged in or redirect to login page 
        access_obj = GLOBAL_DEFS.check_current_user_rights(request)      
        if access_obj["is_logged_in"] and access_obj["allow_to_pass"]:
            pass
        else:
            return redirect("main:index")
        
        current_employee =  access_obj["current_employee"]

        if request.POST.get("add-new-role"):
            role_name = request.POST.get("role-name")
            user_friendly_name = request.POST.get("role-name")
            new_role_action = SystemRoleActions()
            new_role_action.add_role(request, current_employee, role_name, user_friendly_name)
            messages.info(request, "Sucess role added")
            return redirect(request.path)

        if request.POST.get("edit-roleID"):
            role = SystemRoles.objects.get(id = int(request.POST.get("edit-roleID")))
            role_name = request.POST.get("edit-role-name")
            user_friendly_name = request.POST.get("edit-role-name")

            edit_role_action = SystemRoleActions()
            edit_role_action.edit_role(request, role, role_name, user_friendly_name)
            return redirect(request.path)

        if request.POST.get("del-roleID"):
            del_role = SystemRoles.objects.get(id = int(request.POST.get("del-roleID")))

            del_role_action = SystemRoleActions()
            del_role_action.delete_role(request, del_role)

        #
        #Below is a list of roless for this particular school
        #=============================================================================

        roles_list = SystemRoles.objects.filter(stationID = current_employee.stationID, deleted=False)

        return render(
               request, 
               template_name="sysadmin/list_system_roles.html",
               context={
                "roles_list":roles_list,
               })




class SystemRoleActions:
    def add_role(self, request, current_emploee, role_name, user_friendly_name):
        new_role = SystemRoles()
        new_role.businessID= current_emploee.businessID
        new_role.stationID = current_emploee.stationID
        new_role.role_name = role_name
        new_role.user_friendly_name = user_friendly_name
        new_role.save()


    def edit_role(self, request, role, role_name, user_friendly_name):
        if role.module_settings == "" or role.module_settings is None:
            role.role_name = role_name
            role.user_friendly_name = user_friendly_name
            role.save()
            messages.info(request, "Sucess role edited")
        else:
            messages.warning(request, "Inbuilt role can't be edited")

    
    def delete_role(self, request, role):

        count_employees_with_role = Employee.objects.filter(system_roleID = role).count()



        if int(count_employees_with_role) > 0:
            messages.warning(request, "Role is being used by some users, can't be deleted")
            return None 
        else:
            if role.module_settings == "" or role.module_settings is None:
                role.deleted = True
                role.save()
                messages.info(request, "Success, role deleted")
            else:
                messages.warning(request, "Inbuilt role can't be deleled")

    

