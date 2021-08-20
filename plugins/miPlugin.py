"""
Este es un plugin de prueba para probar la gestion de plugin de asenzor
"""
__title__="Mi Plugin"
__authors__="Jesus Zerpa"
__version__="0.0.1"
import django,json
from django.conf import settings
from asenzor.lib.plugins import Plugin
from django.http import JsonResponse
from asenzor.lib.ResourceView import ResourceView
from django.test import Client

class CalendlyCrud(ResourceView):
	model="asenzor.Post",

	def index(self,request):
		from asenzor.lib.helpers.html import App,Button,Div,Section,Script
		btn=Button("Presiona aqui")
		btn.addClass("btn")
		btn["@click"]=f"$api.get('/plugins/calendly/')"
		app=Div()
		app=App(scripts=["/static/asenzor/dist/devtools.js"])
		card=app.get("card.content")
		app.get("card.title").add("Esto es una aplicacion de prueba")
		card.add(btn)
		
		return self.html(request,{
			"block_head":app.head(),
			"block_content":app.body()
			},template="asenzor/dashboard/template.html")

def calendly_api(request):
	token=settings.private.calendly_token
	c=Client()
	req=c.get("https://api.calendly.com/me",
		headers={"Autorization":"Bear "+token})
	
	if req.status_code==200:
		data=req.json()
		organization=data["resources"]["current_organization"]
		uri=data["resources"]["uri"]




class Plugin(Plugin):
	"""docstring for Plugin"""
	#lista de url de plugins que deben estar instalados para que este pueda funcionar
	# "https://zerpatechnology.com.ve/products/asenzor/plugins/<id>"
	# o ("https://zerpatechnology.com.ve/products/asenzor/plugins/<id>","necesary")
	# si es obligatorio estar instalado
	depenencies=[]
	views=[CalendlyCrud]
	def __init__(self,*args,**kwargs):
		super(Plugin, self).__init__(*args,**kwargs)
		

	def load_hooks(self):
		self.add_signal("señal_prueba",django.dispatch.Signal(providing_args=["book", "author"]))
		self.add_action("señal_prueba",lambda sender,**kwargs:print("Señal enviada"))
		self.add_filter("prueba",lambda content:content+" modificado desde un filtro")
		self.add_shortcode("shortcode-prueba",lambda *args, **kwargs: "")
	
	def load_api(self,urlpattern):
		"""
		Se añaden las apis
		"""
		urlpattern.append(
			path("miplugin/",lambda request:JsonResponse({})),
			path("calendly/",calendly_api)
			)

	def load_views(self,urlpattern):
		"""
		Se añaden la views
		"""
		CalendlyCrud("calendly/",urlpattern)

	def add_menus(self,menus):
		menus["ADMIN_MENU"].append(
			["Calendly",settings.ASENZOR_URL+"calendly/",
			 [CalendlyCrud,"index"],"web",[]],
			)

	