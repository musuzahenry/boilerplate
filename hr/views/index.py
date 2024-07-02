
from django.shortcuts import render, redirect, reverse
from django.shortcuts import HttpResponseRedirect
from global_views . global_views import GlobalView
from sysadmin.models import Employee



#our constals
GLOBAL_DEFS = GlobalView()

class Index:

    def index_views(request):

        current_employee = GLOBAL_DEFS.get_current_user_info(request)

        try:
            last_employee = Employee.objects.filter(stationID = current_employee.stationID).order_by("-id")[0]
            return HttpResponseRedirect(reverse('hr:employee-details', args=(last_employee.pk,)))
        except:    
            return render(
                        request, 
                        #template_name="main/cashier_dashboard.html",
                        template_name="hr/index.html",
                        context={
                            
                        })