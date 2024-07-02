
from django.shortcuts import render, redirect
from global_views . global_views import GlobalView




#our constals
GLOBAL_DEFS = GlobalView()

class Index:

    def index_views(request):

        return render(
                    request, 
                    #template_name="main/cashier_dashboard.html",
                    template_name="frontdesk/index.html",
                    context={
                        
                    })

    


    
    def employee(request):
        
        
        return render(
                    request, 
                    #template_name="main/cashier_dashboard.html",
                    template_name="employee/index.html",
                    context={
                        
                    })