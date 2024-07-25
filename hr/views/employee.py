from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from sysadmin.models import Employee, Position
from finance.models import PersonTypes
from hr.forms import EmployeeForm
from django.contrib import messages
from global_views . global_views import GlobalView
from finance.views import CashBookActions, ItemType, Item,  PaymentMethod, ItemCategory, CashBook
from sysadmin.models import Station



#our constals
GLOBAL_DEFS = GlobalView()


class EmployeeListView(ListView):
    model = Employee
    template_name = 'hr/employee_list.html'
    access_obj = None
    stationID = None

    #define a post method
    def post(self, *args, **kwargs):
        if self.request.POST.get("stationID-id"):
            self.stationID = Station.objects.get(id = int(self.request.POST.get("stationID-id")))
        return super().get(self.request, *args, **kwargs)

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

    def get_queryset(self, **kwargs):

        current_employee = self.access_obj["current_employee"]

        rights_name_list = self.access_obj["rights_name_list"]

        if "allow_to_view_other_stations" in rights_name_list:
            if self.stationID:
                query_set = Employee.objects.filter(stationID = self.stationID,  deleted=False)
            else:
                query_set = Employee.objects.filter(businessID = current_employee.businessID,  deleted=False)
        else:
            query_set = Employee.objects.filter(stationID = current_employee.stationID,  deleted=False)

        return query_set

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)     
        context["count"] = self.get_queryset().count() 
        context["pay_methods"] = PaymentMethod.objects.all() 
        #get a list of all stations
        all_stations = Station.objects.filter(businessID = self.access_obj["current_employee"].businessID)

        if self.stationID: 
           context["staionID_id"] = self.stationID.id
           context["station_name"] = self.stationID.station_name
        
        context["all_stations"] = all_stations
         
        #now return the context
        return context




class EmployeeCreateView(CreateView):
    model = Employee
    form_class = EmployeeForm
    access_obj = None
    
    template_name = 'hr/create_employee.html'
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
        self.success_message = "Your item was successfully created!"
        context["positions"] = positions
        return context

    def get_success_url(self):   
        return  reverse("hr:employee-list")

    def form_valid(self, form_class):

        new_employee = form_class.save(commit=False)        
        current_employee = GLOBAL_DEFS.get_current_user_info(self.request)
        new_employee.businessID = current_employee.businessID
        new_employee.stationID = current_employee.stationID
        new_employee.object = form_class.save()
        return super().form_valid(form_class)





class EmployeeUpdateView(UpdateView):
    model = Employee
    form_class = EmployeeForm
    success_message = "Sucess, record updated"

    template_name = "hr/employee_update.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()      
        if self.request.session["dashboard"] == "sysadmin":
            self.request.session["current_employeeID"] = self.object.id
            return redirect("sysadmin:index")

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["employee"] = self.object
        return context
        
    def get_success_url(self):   
         return '/hr/update-employee/{}'.format(self.object.pk)



class EmployeeDetailView(DetailView):
    model = Employee
    template_name = 'hr/employee_detail.html'  # Specify your template







class EmployeeViews:

    def delete_employee(request, id):
        
        access_obj = GLOBAL_DEFS.check_current_user_rights(              
                                                           request, 
                                                           right_name ="manage-employees",
                                                          )
        if access_obj["is_logged_in"] and access_obj["allow_to_pass"]:
            pass
        else:
            return redirect("main:index")

        del_employee = Employee.objects.get(id= int(id))
        del_employee.is_system_user = False
        del_employee. deleted = True

        try:
            del_employee.userID.is_active = False
            del_employee.userID.save()
        except:
            pass
    
        del_employee.save()
        messages.info(request, "Success, record  deleted")
        return redirect("hr:employee-list")



    def restore_employee(request, id):

        access_obj = GLOBAL_DEFS.check_current_user_rights(              
                                                           request, 
                                                           right_name ="manage-employees",
                                                          )
        if access_obj["is_logged_in"] and access_obj["allow_to_pass"]:
            pass
        else:
            return redirect("main:index")
        
        restored_employee = Employee.objects.get(id= int(id))
        restored_employee.is_system_user = True
        restored_employee.deleted = False

        try:
            restored_employee.userID.is_active = True
            restored_employee.userID.save()
        except:
            pass 

        restored_employee.save()
        messages.info(request, "Success, record  deleted")
        return redirect("hr:employee-list")





    def deleted_employees(request):

        access_obj = GLOBAL_DEFS.check_current_user_rights(              
                                                           request, 
                                                           right_name ="manage-employees",
                                                          )
        if access_obj["is_logged_in"] and access_obj["allow_to_pass"]:
            pass
        else:
            return redirect("main:index")

        current_employee = access_obj["current_employee"]
        rights_name_list = access_obj["rights_name_list"]
        all_stations = Station.objects.filter(businessID = current_employee.businessID)

        if "allow_to_view_other_stations" in rights_name_list:
           if request.POST.get("stationID-id"):
              stationID = Station.objects.get(id = int(request.POST.get("stationID-id")))
              deteled_list = Employee.objects.filter(stationID = stationID, deleted=True)
           else:
              deteled_list = Employee.objects.filter(businessID = current_employee.businessID, deleted=True)
        else:
           deteled_list = Employee.objects.filter(stationID = current_employee.stationID)


        return render(
                      request,
                      template_name = "hr/deleted_employees.html",
                      context={
                        "deteled_list":deteled_list, 
                        "all_stations":all_stations
                        }
                      )




    def make_emp_payments(request):

        access_obj = GLOBAL_DEFS.check_current_user_rights(request, right_name="pay-employees")

        if access_obj["is_logged_in"] and access_obj["allow_to_pass"]:
            pass
        else:
            return redirect("main:index")
     
                    
        def make_payment(current_employee, this_employee, person_typeID, item_typeID, payID_NO, \
                             itemID, item_name, item_categoryID, amount_paid):
            #Adding to cashbook
            #=========================================
            add_to_cashbook = CashBookActions() 
            add_to_cashbook.add_to_cashbook(
                                            request, 
                                            current_employee = current_employee,
                                            item_typeID=item_typeID, 
                                            item_categoryID = item_categoryID, 
                                            itemID = itemID,
                                            pay_methodID=pay_methodID, 
                                            person_typeID=person_typeID, 
                                            personID_id=this_employee.id, 
                                            particulars=this_employee.fullname, 
                                            item_name= item_name, 
                                            payID_NO = payID_NO,
                                            quantity=1, 
                                            income_received=0, 
                                            expense_made = amount_paid, 
                                            ) 
       

        

        def set_payment(current_employee, this_employee, person_typeID, item_typeID,  pay_methodID, payID_NO):
            if request.POST.get("custom-employee-payment") and request.POST.get("custom-payment"): 
                    itemID = Item.objects.get(settings_name = "custom-employee-payment", stationID = current_employee.stationID)
                    item_categoryID = itemID.item_categoryID
                    item_name = request.POST.get("custom-employee-payment")
                    amount_paid = float(request.POST.get("custom-payment"))*(int(request.POST.get("percentage-pay"))/100)
                    #make this payment                 
                    make_payment(current_employee, this_employee, person_typeID, item_typeID, payID_NO, \
                        itemID, item_name, item_categoryID, amount_paid)
    
            if request.POST.get("net-salary"):
                    itemID = Item.objects.get(settings_name = "net-salary", stationID = current_employee.stationID)
                    item_categoryID = itemID.item_categoryID
                    amount_paid = float(this_employee.net_salary)*(int(request.POST.get("percentage-pay"))/100)
                    #make this payment
                    make_payment(current_employee, this_employee, person_typeID, item_typeID, payID_NO, \
                        itemID, itemID.item_name, item_categoryID, amount_paid)

            if request.POST.get("nssf"):
                    itemID = Item.objects.get(settings_name = "nssf", stationID = current_employee.stationID)
                    item_categoryID = itemID.item_categoryID
                    amount_paid = float(this_employee.nssf)*(int(request.POST.get("percentage-pay"))/100)
                    #make this payment
                    make_payment(current_employee, this_employee, person_typeID, item_typeID, payID_NO, \
                        itemID, itemID.item_name, item_categoryID, amount_paid)
    

            if request.POST.get("paye"):
                    itemID = Item.objects.get(settings_name = "paye", stationID = current_employee.stationID)
                    item_categoryID = itemID.item_categoryID
                    amount_paid = float(this_employee.PAYE)*(int(request.POST.get("percentage-pay"))/100)
                    #make this payment
                    make_payment(current_employee, this_employee, person_typeID, item_typeID, payID_NO, \
                        itemID, item_categoryID, amount_paid)




        person_typeID = PersonTypes.objects.get(settings_name = "employee")
        item_typeID = ItemType.objects.get(settings_name = request.POST.get("item-type"))
        pay_methodID = PaymentMethod.objects.get(settings_name = request.POST.get("pay-method"))
        payID_NO = request.POST.get("payID-NO")
        current_employee = access_obj["current_employee"]
        
        if request.POST.get("pay-for-one"):                  
            this_employee = Employee.objects.get(id = int(request.POST.get("personID")))
            set_payment(current_employee, this_employee, person_typeID, item_typeID,  pay_methodID, payID_NO)
                
        if request.POST.get("pay-selected"):        
            all_employess = Employee.objects.filter(stationID = current_employee.stationID)
            for this_employee in all_employess:
                if request.POST.get(str(this_employee.id)+"-checked"):
                    set_payment(current_employee, this_employee, person_typeID, item_typeID,  pay_methodID, payID_NO)


        return redirect ("hr:employee-payments")





    def employee_payments(request):
        
        access_obj = GLOBAL_DEFS.check_current_user_rights(request)

        if access_obj["is_logged_in"] and access_obj["allow_to_pass"]:
            pass
        else:
            return redirect("main:index")

        current_employee = access_obj["current_employee"] 
        rights_name_list = access_obj["rights_name_list"]
        person_typeID = person_typeID = PersonTypes.objects.get(settings_name = "employee")
        all_stations = Station.objects.filter(businessID = current_employee.businessID)

        #lets clean our posted dates
        #======================================================================
        date_obj = GLOBAL_DEFS.get_date1_and_date2(request)
        

        if "allow_to_view_other_stations" in rights_name_list:
            #is user allowed to view all stations

            if request.POST.get("stationID-id"):
                stationID = Station.objects.get(id = int(request.POST.get("stationID-id")))
                query_set = CashBook.objects.filter(
                                                businessID = current_employee.businessID,
                                                record_date__gte=date_obj["date1"],
                                                record_date__lte=date_obj["date2"],
                                                person_typeID = person_typeID,
                                                stationID = stationID,
                                                deleted=False
                                                )
            else:
               query_set = CashBook.objects.filter(
                                                businessID = current_employee.businessID,
                                                record_date__gte=date_obj["date1"],
                                                record_date__lte=date_obj["date2"],
                                                person_typeID = person_typeID,
                                                is_deleted = False,
                                                )
        else:
            query_set = CashBook.objects.filter(
                                                stationID = current_employee.stationID,
                                                record_date__gte=date_obj["date1"],
                                                record_date__lte=date_obj["date2"],
                                                person_typeID = person_typeID,
                                                is_deleted = False,
                                                )

        count = query_set.count()




        return render(request,
                     template_name = "hr/eployee_payments.html",
                     context={
                       "object_list":query_set,
                       "orig_date1":date_obj["orig_date1"],
                       "orig_date2":date_obj["orig_date2"],
                       "count":count,
                       "all_stations":all_stations,
                       }
                    )




        

