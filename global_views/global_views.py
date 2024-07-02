
from sysadmin.models import Employee, Rights, SystemRoles, RoleRights, SystemSetings
from sacco import settings
from django.contrib import messages
from django.shortcuts import render, redirect



class GlobalView:

    def set_dashboard_header_and_footer(self, request, dashboard_request):
        app_name = dashboard_request.split(":")[0]
        role = SystemRoles.objects.get(module_settings = app_name)

        request.session["current_dashboard"] = role.user_friendly_name
        request.session["dashboard"] = role.role_name
        request.session["current_header"] = app_name+"/header.html"
        request.session["current_footer"] = app_name+"/footer.html"


    
    def save_business_info(self, obj, current_employee):
        obj.businessID = current_employee.businessID
        obj.stationID = current_employee.stationID
        return obj

        




    def get_sys_info(self, request):
        #get system info
        sys_info = SystemSetings.objects.get(id=1)
        request.session["app_name"] = sys_info.app_name
        request.session["app_logo"] = str(sys_info.app_logo)
        request.session["app_footer"] = sys_info.app_footer

        return sys_info




    def initialize_app(self, request):
        #do things you want on login
        
        #work on sessions
        #=================================================
        request.session["DEBUG"] = True if settings.DEBUG else False
        
        #get current employee
        current_employee = self.get_current_user_info(request)

        request.session["station_name"] = current_employee.stationID.station_name
        try:
           request.session["station_logo"] = current_employee.stationID.logo.url
        except:
          pass
        return current_employee




    def get_current_user_info(self, request):

        current_employee = Employee.objects.get(userID = request.user)
        
        if current_employee.is_system_user and not(current_employee.deleted):
            return current_employee
        else:
            from sysadmin.index import Index
            
            Index.logoout(request)
            messages.warning(request, "Sorry, you are not a system user")
            return redirect("systmadmin:index")
        return current_employee




    def check_current_user_rights(self, request, right_name = None):
        #allow_to_pass allows or diallows a person from paassinf depending on its value
        #==============================================================================
        access_object = {"is_logged_in":False, "allow_to_pass" : False, "current_employee" : None,}

        #secure app for only logged users
        current_employee = None
        is_logged_in = False
        allow_to_pass = False

        if request.user.is_authenticated:
            is_logged_in = True
            pass #let to pass
        else:
            messages.warning(request, "Please login first")
            #redirect to login page
            return redirect("sysadmin:index")

        #get current use info
        #==============================================================================
        current_employee = self.get_current_user_info(request)


        if (right_name == None): 
            allow_to_pass = True          

        else:          
            rightID = Rights.objects.get(settings_name = right_name)
            #if right exists
            if RoleRights.objects.filter(rightID = rightID, roleID=current_employee.system_roleID).exists():
                allow_to_pass = True
                
            elif current_employee.system_roleID.module_settings == "administrator":  #administrator can always pass 
                allow_to_pass = True
            else:
                allow_to_pass = False

        
        if allow_to_pass == False:
            messages.warning(request, "Sorry, you have no access to this resource")

        access_object = {"is_logged_in":is_logged_in, "current_employee":current_employee, "allow_to_pass":allow_to_pass} 
        return access_object
        
  

    