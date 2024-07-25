
from django.shortcuts import render, redirect
from django.contrib import messages
from sysadmin.models import SystemRoles, Rights, RoleRights, Employee
from global_views . global_views import GlobalView

GLOBAL_DEF = GlobalView()



class RoleRightsViews:

    def list_role_rights(request, id):
         
        access_obj = GLOBAL_DEF.check_current_user_rights(request)
        #access_object = {"is_logged_in":False, "allow_to_pass" : False, "current_employee" : None, 
        # "rights_name_list":None}

        if access_obj["is_logged_in"] and access_obj["allow_to_pass"]:
            pass
        else:
            return redirect("main:index")

        current_employee = access_obj["current_employee"]

        current_role = SystemRoles.objects.get(id=int(id), stationID = current_employee.stationID)

        rights_list = RoleRights.objects.filter(roleID = current_role, stationID = current_employee.stationID)


        user_rights_list = [used_right.rightID.id for used_right in rights_list]
        un_used_rights_list = Rights.objects.filter(stationID = 
                              current_employee.stationID).exclude(id__in=user_rights_list).order_by("settings_name")
        
        if request.POST.get("add-role-rights"):
            add_role_right = RoleRightActions()
            add_role_right.add_role_right_action(request, current_employee, current_role)
            return redirect(request.path)
        

        if request.POST.get("del-rightID"):
            del_role = RoleRights.objects.get(id =int(request.POST.get("del-rightID")))
            del_role_right = RoleRightActions()
            del_role_right.delete_role_right(request, del_role)
            return redirect(request.path)

        return render(
                      request,
                      template_name="sysadmin/list_role_rights.html", 
                      context={
                        "current_role":current_role,
                        "rights_list":rights_list,
                        "un_used_rights_list":un_used_rights_list,
                      }
                      )





class RoleRightActions:

    def add_role_right_action(self, request, current_employee, current_role):

        all_rights = Rights.objects.filter(stationID = current_employee.stationID)

        for rightx in all_rights:

            if request.POST.get(rightx.settings_name):

                new_role_right = RoleRights()
                new_role_right.roleID = current_role
                new_role_right.rightID = rightx
                new_role_right.stationID = current_employee.stationID
                new_role_right.businessID = current_employee.businessID
                new_role_right.mandatory = rightx.mandatory
                new_role_right.save()
        
        messages.info(request, "Succes, rights added")

    

    def delete_role_right(self, request, rightID):
        rightID.delete()
        messages.info(request, "Success, deleted")



