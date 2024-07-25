from django.shortcuts import render, redirect
from global_views . global_views import GlobalView
from finance . models import Client




#our constals
GLOBAL_DEFS = GlobalView()

class Index:
    def index_views(request):
        clientID = None


        try:
            clientID = Client.objects.get(id = int(request.session["current_clientID_id"]))
        except:
            pass
        
        

        return render(
                      request,
                      template_name = "frontdesk/index.html",
                      context ={
                       "clientID":clientID,
                      }
                     )