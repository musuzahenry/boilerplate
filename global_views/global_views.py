
from sysadmin.models import Employee, Rights, SystemRoles, RoleRights, SystemSetings
from sacco import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from datetime import datetime, timedelta





class GlobalView:

    def get_date1_and_date2(self, request):

        today = datetime.today()
        year= today.year
        month = today.month
        day = today.day
        today_date = datetime.strptime(str(year)+"-"+str(month)+"-"+str(day)+ " 00:00:00+03:00","%Y-%m-%d %H:%M:%S%z")
        tomorrow_date = today_date + timedelta(days = 1)

        date1 = today_date
        date2 = tomorrow_date
        
        if not request.POST:
            date1 = today_date
            date2 = tomorrow_date
            orig_date1 = str(today_date).split(" ")[0]
            orig_date2 = str(today_date).split(" ")[0]
        elif request.POST.get("date1") and request.POST.get("date2"): 
            date1 = request.POST.get("date1")
            date2 = self.set_date2(request.POST.get("date2"))
            orig_date1 = str(request.POST.get("date1")).split(" ")[0]
            orig_date2 = str(request.POST.get("date2")).split(" ")[0]
        else:
            date1 = today_date
            date2 = tomorrow_date
            orig_date1 = str(today_date).split(" ")[0]
            orig_date2 = str(today_date).split(" ")[0]


        return {"date1":date1, "date2":date2, "orig_date1": orig_date1, "orig_date2":orig_date2}




    def set_date2(self, second_date):
        date2_str = datetime.strptime(second_date, '%Y-%m-%d')+ timedelta(days=1)
        date2_obj = str(date2_str).split("-")
        date2 = date2_obj[0]+"-"+date2_obj[1]+"-"+date2_obj[2]
        return date2 




    def set_dashboard_header_and_footer(self, request, dashboard_request):
        app_name = dashboard_request.split(":")[0]
        role = SystemRoles.objects.get(module_settings = app_name)

        request.session["current_dashboard"] = role.user_friendly_name
        request.session["dashboard"] = role.module_settings
        request.session["dashboard_ui_name"] = role.role_name
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



    
    def set_current_client_details(self, request, clientID):
        request.session["current_clientID_id"] = clientID.id
        return redirect ("frontdesk:index")




    def get_current_user_info(self, request):

        if not (request.user.is_authenticated):
           messages.warning(request, "Please login first")
           return redirect("main:index")

        current_employee = Employee.objects.get(userID = request.user)
        
        if current_employee.is_system_user and not(current_employee.deleted):
            return current_employee
        else:
            from sysadmin.index import Index
            
            Index.logoout(request)
            messages.warning(request, "Sorry, you are not a system user")
            return redirect("systmadmin:index")

            current_employee_obj ={"current_employee":current_employee, }
        return current_employee




    def check_current_user_rights(self, request, right_name = None):
        #allow_to_pass allows or diallows a person from paassinf depending on its value
        #==============================================================================
        access_object = {"is_logged_in":False, "allow_to_pass" : False, "current_employee" : None, "rights_name_list":None}

        #secure app for only logged users
        current_employee = None
        is_logged_in = False
        allow_to_pass = False
        all_role_rights = None

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

        
        rights_name_list = []


        #messages.info(request, str(rights_name_list))
        if (right_name == None): 
            allow_to_pass = True          

        else:          
            #if right exists
            #if RoleRights.objects.filter(rightID = rightID, roleID=current_employee.system_roleID).exists():
            if right_name in rights_name_list:
                allow_to_pass = True
                #all current_user_rights
                all_role_rights =  RoleRights.objects.filter(roleID=current_employee.system_roleID, stationID = current_employee.stationID)
                for role_right in all_role_rights:
                   rights_name_list.append(role_right.rightID.settings_name)
                
            elif current_employee.system_roleID.module_settings == "administrator" or \
                 current_employee.system_roleID.module_settings == "sysadmin":  #administrator can always pass 
                 
                allow_to_pass = True
                #all current_user_rights
                all_rights =  Rights.objects.filter(stationID = current_employee.stationID)
                for right in all_rights:
                   rights_name_list.append(right.settings_name)
            else:
                allow_to_pass = False

        
        if allow_to_pass == False:
            messages.warning(request, "Sorry, you have no access to this resource")

        access_object = {"is_logged_in":is_logged_in, "current_employee":current_employee, "allow_to_pass":allow_to_pass, "rights_name_list":rights_name_list} 
        
        return access_object
        




    