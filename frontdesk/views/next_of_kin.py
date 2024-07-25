from django.shortcuts import render, redirect, reverse
from django.views.generic import CreateView, UpdateView, ListView
from finance.models import ClientNextOKin, Client
from frontdesk.forms import ClientNextOKinForm
from django.contrib import messages
from global_views . global_views import GlobalView


GLOBAL_DEFS = GlobalView()



class NextOfKinViews:
    def update_client_kin(request, id):
        access_obj = GLOBAL_DEFS.check_current_user_rights(              
                                                           request, 
                                                           right_name ="manage-clients",
                                                          )
        if access_obj["is_logged_in"] and access_obj["allow_to_pass"]:
            pass
        else:
            return redirect("main:index")
        
        kin = ClientNextOKin.objects.get(id = int(id))
        clientID = kin.clientID
        if request.POST.get("next_of_kin_full_name"):
            kin.clientID = clientID
            kin.next_of_kin_full_name = request.POST.get("next_of_kin_full_name")
            kin.next_of_kin_contacts = request.POST.get("next_of_kin_contacts")
            kin.next_of_kin_address = request.POST.get("next_of_kin_address")
            kin.next_of_kin_relation =  request.POST.get("next_of_kin_relation") 
            if request.FILES.get("next_of_kin_image"):
               kin.next_of_kin_image = request.FILES.get("next_of_kin_image") 
            kin.save()
            messages.info(request, "Success, record saved")
        return render(
                      request,
                      template_name ="frontdesk//next_of_kin_update.html",
                      context ={
                        "clientID":clientID,
                        "kin":kin,
                      }
                      )




    def creat_next_of_kin(request, id):     
        access_obj = GLOBAL_DEFS.check_current_user_rights(              
                                                           request, 
                                                           right_name ="manage-clients",
                                                          )
        if access_obj["is_logged_in"] and access_obj["allow_to_pass"]:
            pass
        else:
            return redirect("main:index")
        
        clientID = Client.objects.get(id = int(id))
        list_of_kins = ClientNextOKin.objects.filter(clientID = clientID)
        if request.POST.get("next_of_kin_full_name"):
            kin = ClientNextOKin()
            clientID = Client.objects.get(id = int(id))
            kin.clientID = clientID
            kin.next_of_kin_full_name = request.POST.get("next_of_kin_full_name")
            kin.next_of_kin_contacts = request.POST.get("next_of_kin_contacts")
            kin.next_of_kin_address = request.POST.get("next_of_kin_address")
            kin.next_of_kin_relation =  request.POST.get("next_of_kin_relation") 
            if request.POST.get("next_of_kin_image"):
               kin.next_of_kin_image = request.POST.get("next_of_kin_image") 
            kin.save()
            messages.info(request, "Success, record saved")
        return render(
                      request,
                      template_name ="frontdesk/next_of_kin_create.html",
                      context ={
                        "form":ClientNextOKinForm,
                        "clientID":clientID,
                        "list_of_kins":list_of_kins,
                      }
                      )



