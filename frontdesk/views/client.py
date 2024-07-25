from django . shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views.generic import ListView, UpdateView, CreateView, DetailView
from finance.models import Client, ClientNextOKin
from sysadmin.models import Station, Position
from frontdesk.forms import ClientForm
from django.contrib import messages
from global_views . global_views import GlobalView



GLOBAL_DEFS = GlobalView()



class ClientListView(ListView):
    model = Client
    template_name = "frontdesk/list_clients.html"
    access_obj = None
    stationID = None
    date1 = None
    date2 = None
    search_str = None

    def post(self, *args, **kwargs):
        if self.request.POST.get("stationID-id"):
            self.stationID = Station.objects.get(id = int(self.request.POST.get("stationID-id")))
        
        if not self.request.POST.get("search_str"):
            date_object = GLOBAL_DEFS.get_date1_and_date2(self.request)
            self.date1 = date_object["date1"]
            self.date2 = date_object["date2"]    
        else:
            self.search_str =  self.request.POST.get("search_str")   
        return super().get(self.request, *args, **kwargs)


    def get(self, *args, **kwargs):
        date_object = GLOBAL_DEFS.get_date1_and_date2(self.request)
        self.date1 = date_object["date1"]
        self.date2 = date_object["date2"]    
        return super().get(self.request, *args, **kwargs)


    def dispatch(self, request, *args, **kwargs):
        self.access_obj = GLOBAL_DEFS.check_current_user_rights(self.request, "manage-clients")

        if self.access_obj["is_logged_in"] and self.access_obj["allow_to_pass"]:
            pass
        else:
            return redirect("main:index")
        return super().dispatch(request, *args, **kwargs)


    def get_queryset(self, **kwargs):
        current_employee = self.access_obj["current_employee"]
        rights_name_list= self.access_obj["rights_name_list"]

        if not self.search_str:
            
            if "allow_to_view_other_stations" in rights_name_list:          
                if self.stationID:
                    query_set = Client.objects.filter(
                                                      stationID = self.stationID, 
                                                      record_date__gte =self.date1, 
                                                      record_date__lte =self.date2, 
                                                      deleted=False,
                                                      )
                else:
                    query_set = Client.objects.filter(
                                                     businessID = current_employee.businessID, 
                                                     record_date__gte =self.date1, 
                                                     record_date__lte =self.date2, 
                                                     deleted=False,
                                                     )
            else:
                query_set = Client.objects.filter(
                                                 stationID = current_employee.stationID, 
                                                 record_date__gte =self.date1, 
                                                 record_date__lte =self.date2, 
                                                 deleted=False,
                                                 )
        else:
            if "allow_to_view_other_stations" in rights_name_list: 
                query_set = Client.objects.filter(
                                                  search_string__icontains = self.search_str,
                                                  businessID = current_employee.businessID, 
                                                  deleted=False,
                                                  )
            else:
                query_set = Client.objects.filter(
                                                 stationID = current_employee.stationID, 
                                                 search_string__icontains = self.search_str, 
                                                 deleted=False,
                                                 )
    
        return query_set

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_employee = self.access_obj["current_employee"]
        context["all_stations"] = Station.objects.filter(businessID = current_employee.businessID)
        context["count"] = self.get_queryset().count()
        return context






class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    access_obj = None
    
    template_name = 'frontdesk/create_client.html'
    success_message = "Your record saved"

    def dispatch(self, request, *args, **kwargs):
        self.access_obj = GLOBAL_DEFS.check_current_user_rights(              
                                                           self.request, 
                                                           right_name ="manage-employees",
                                                          )
        if self.access_obj["is_logged_in"] and self.access_obj["allow_to_pass"]:
            pass
        else:
            return redirect("main:index")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        current_employee = GLOBAL_DEFS.get_current_user_info(self.request)
        positions = Position.objects.filter(stationID = current_employee.stationID)

        context["positions"] = positions
        context["form"] = self.form_class
        new_of_kins = ClientNextOKin.objects.filter(clientID = self.object)
        context["new_of_kins"] = new_of_kins
        return context

    def get_success_url(self):   
        return  "client-update/{}".format(self.object.pk)

    def form_valid(self, form_class):
        messages.info(self.request, self.success_message)
        new_client = form_class.save(commit=False)        
        current_employee = GLOBAL_DEFS.get_current_user_info(self.request)
        new_client.businessID = current_employee.businessID
        new_client.stationID = current_employee.stationID
        new_client.object = form_class.save()
        return super().form_valid(form_class)




class ClientUpdateView(UpdateView):
    model = Client
    form_class= ClientForm
    success_message = "Sucess, record updated"
    template_name = "frontdesk/client_update.html"

    def get(self, request, *args, **kwargs):
        self.access_obj = GLOBAL_DEFS.check_current_user_rights(self.request, "manage-clients")
        if self.access_obj["is_logged_in"] and self.access_obj["allow_to_pass"]:
            pass
        else:
            return redirect("main:index")

        self.object = self.get_object()
        return super().get(request, *args, *kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["client"] = self.object
        context["next_of_kins"] = ClientNextOKin.objects.filter(clientID = self.object)
        return context
    
    def get_success_url(self):   
         return '/frontdesk/client-update/{}'.format(self.object.pk)




class ClientDetailView(DetailView):
    model = Client
    template_name = "frontdesk/client_detail.html"




class ClientViews:
    def delete_client(request, id):
        
        access_obj = GLOBAL_DEFS.check_current_user_rights(request, "manage-clients")

        if access_obj["is_logged_in"] and access_obj["allow_to_pass"]:
            pass
        else:
            return redirect("main:index")

        
        del_client = Client.objects.get(id = int(id))
        del_client.deleted = True
        del_client.save()
        messages.info(request, "Success, record deleted")

        return redirect("frontdesk:list-clients")



    def set_current_client_by_click(request, id):
        request.session["current_clientID_id"] = id
        return redirect("frontdesk:index")

    
    def set_current_client(self, request, id):
        request.session["current_clientID_id"] = id
        return redirect("frontdesk:index")




