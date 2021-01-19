
from django.conf import settings # import the settings file
def context(request):
    # return the value you want as a dictionnary. you may add multiple values in there.
    from .signals import render_started
    
    render_started.send(sender=request)    
    """
    BASE_URL=settings.BASE_URL
    BASE_URL_CLEAN=settings.BASE_URL_CLEAN
    
   

    if request.META['REMOTE_ADDR']!="127.0.0.1" and settings.DEBUG:
    	BASE_URL=settings.PROTOCOL+settings.PRIVATE_HOST#request.META['REMOTE_ADDR']+"/"
    if request.META['REMOTE_ADDR']!="127.0.0.1" and settings.DEBUG:
    	BASE_URL_CLEAN=settings.PRIVATE_HOST
    """
    
    data={'BASE_URL': request.scheme+"://"+request.get_host()+settings.BASE_URL,
    'ASENZOR_URL': request.scheme+"://"+request.get_host()+settings.ASENZOR_URL,
    'MEDIA_URL': request.scheme+"://"+request.get_host()+settings.MEDIA_URL}
    data.update(settings.MENUS)
    return data