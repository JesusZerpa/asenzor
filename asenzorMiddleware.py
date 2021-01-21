from django.conf import settings
from .models import Site
from django.http import HttpResponseRedirect
class AsenzorMiddleware(object):
    # Check if client IP address is allowed
    def __init__(self, get_response):
        
        self.get_response = get_response
        
    def process_request(self, request): 
        # If IP address is allowed we don't do anything
        pass


        
    def __call__(self, request):
        from .signals import render_started
        from django.apps import apps
        if not len(Site.objects.all())\
            and request.get_full_path()!=settings.ASENZOR_URL+"install/" and not request.get_full_path().startswith("/admin"):

            return HttpResponseRedirect(
             settings.ASENZOR_URL+"install"
            )
	
        if "menus" not in apps.get_app_config("asenzor").loadeds:
            settings.MENUS={"ADMIN_MENU":[],
               "PRIMARY_MENU":[],
               "SECUNDARY_MENU":[],
               "ADMIN_NAVBAR":[]}
        render_started.send(sender=request)
	
        return self.get_response(request)
