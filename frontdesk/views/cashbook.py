from django.shortcuts import redirect, render
from django.views.generic import ListView, CreateView, UpdateView

from django.contrib import messages
from sysadmin.models import SystemSetings
from global_views . global_views import  GlobalView
from finance.models import CashBook, ItemCategory, Item, ItemType, MoneySource, PaymentMethod, MoneySource, PersonTypes 
from sysadmin.models import Station
from finance.forms import CashBookForm




#our constals
GLOBAL_DEFS = GlobalView()



class CashbookViews:

    def list_cashbook(request):

        access_obj = GLOBAL_DEFS.check_current_user_rights(request)

        if access_obj["is_logged_in"] and access_obj["allow_to_pass"]:
            pass
        else:
            return redirect("main:index")

        current_employee = access_obj["current_employee"] 
        rights_name_list = access_obj["rights_name_list"]
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
                                                stationID = stationID
                                                )
            else:
                
                query_set = CashBook.objects.filter(
                                                businessID = current_employee.businessID,
                                                record_date__gte=date_obj["date1"],
                                                record_date__lte=date_obj["date2"],
                                                )
        else:
            query_set = CashBook.objects.filter(
                                                stationID = current_employee.stationID,
                                                record_date__gte=date_obj["date1"],
                                                record_date__lte=date_obj["date2"],
                                                )

        count = query_set.count()
        closing_balance = None
        closing_balance_set = ""
        opening_balance = None
        opening_balance_set = ""


        try:
            #getting closing balance
            #================================================================           
           closing_balancex = query_set[count-1].running_total
           closing_balance = "{:,}".format(float(closing_balancex)) if float(closing_balancex) >=0  else "(" + "{:,}".format(-1*float(closing_balancex)) + ")"
        except:
            closing_balance_set = "Closing Balance Not Set"

        
        try: 
            #getting opening balance  
            #==============================================================
           try:
                opening_balance_obj = CashBook.objects.filter(id__lt = query_set[0].id, stationID = current_employee.stationID).order_by("-id")[0]
                opening_balancex = opening_balance_obj.running_total
           except:
              opening_balancex = 0

           opening_balance = "{:,}".format(float(opening_balancex)) if float(opening_balancex) >=0  else "(" + "{:,}".format(-1*float(opening_balancex)) + ")"
        except:
            opening_balance_set = "Opening Balance Not Set"


        return render(request,
                     template_name = "finance/list_cashbook.html",
                     context={
                       "object_list":query_set,
                       "orig_date1":date_obj["orig_date1"],
                       "orig_date2":date_obj["orig_date2"],
                       "count":count,
                       "closing_balance":closing_balance,
                       "closing_balance_set":closing_balance_set,
                       "opening_balance":opening_balance,
                       "opening_balance_set":opening_balance_set,
                       "all_stations":all_stations,
                       }
                    )




class CashBookActions:

    def add_to_cashbook(self, request, current_employee, businessID=None,
                        stationID = None, item_typeID = None,item_categoryID = None, money_sourceID = None,
                        pay_methodID = None,person_typeID = None, personID_id = 0, itemID = None, 
                        particulars = None, item_name = None, payID_NO = None, is_income = False, unit_cost = 0,
                        unit_price = 0, quantity = 1,income_received = 0,expense_made = 0,
                        net = 0,net_str = "",userID = None,user_fullname = None, is_deleted = False,
                        color_code = "transparent"
                        ):
       #saving into the cashbook
       #===================================================================================================
        new_cashbook = CashBook()
        new_cashbook.businessID = current_employee.businessID
        new_cashbook.stationID = current_employee.stationID

        new_cashbook.pay_methodID = pay_methodID
        new_cashbook.item_typeID = item_typeID

        new_cashbook.pseronID = personID_id
        new_cashbook.person_typeID = person_typeID
        new_cashbook.item_categoryID = item_categoryID
        
        new_cashbook.particulars = particulars
        new_cashbook.itemID = itemID
        new_cashbook.item_name = item_name
        new_cashbook.payID_NO = payID_NO
        new_cashbook.is_income = is_income
        new_cashbook.unit_cost = unit_cost
        new_cashbook.unit_price = unit_price
    
        new_cashbook.quantity = quantity
        new_cashbook.income_received = income_received
        new_cashbook.expense_made = expense_made

        new_cashbook.net = int(income_received) - int(expense_made)
        net_str =  "{:,}".format(float(net)) if net >=0  else "(" + "{:,}".format(-1*float(net)) + ")"
        new_cashbook.net_str = net_str   
        new_cashbook.userID = current_employee.userID
        new_cashbook.user_fullname = current_employee.fullname
        
        new_cashbook.is_deleted = is_deleted
        new_cashbook.color_code = color_code #but color code=red indicated refunded
        new_cashbook.save()


        running_total = self.get_running_total(new_cashbook)
        running_total_str =  "{:,}".format(float(running_total)) if running_total >=0  else "(" + "{:,}".format(-1*float(running_total)) + ")"

        new_cashbook.running_total = running_total

        new_cashbook.running_total_str = running_total_str 
        new_cashbook.save()



 
    def get_running_total(self, new_cashbook):
        #get running total
        #=================================================================================================
        try:
           prev_cashbook = CashBook.objects.filter(id__lt = int(new_cashbook.id),
                                                   stationID = new_cashbook.stationID).order_by("-id")[0]
           prev_running_total = prev_cashbook.running_total
        except:
            prev_running_total = 0
 
        running_total = float(new_cashbook.income_received) - float(new_cashbook.expense_made) + prev_running_total
        return running_total
